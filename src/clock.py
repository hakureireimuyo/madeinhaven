from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, StringProperty, ObjectProperty,ListProperty
# from src.evn import get_resource_path
from src.evn import get_resource_path

class AnalogClock(Widget):
    """模拟时钟部件，带有时针、分针和秒针，使用固定旋转中心点"""
    # 属性定义
    hour_angle = NumericProperty(0)
    minute_angle = NumericProperty(0)
    second_angle = NumericProperty(0)
    
    # 指针旋转中心点（相对于指针图像自身的归一化坐标，范围0-1）
    hour_pivot = ListProperty([0.1, 0.5])    # 通常时针旋转中心在底部附近
    minute_pivot = ListProperty([0.07, 0.5])  # 通常分针旋转中心在底部附近  
    second_pivot = ListProperty([0.02, 0.5])  # 通常秒针旋转中心在底部附近
    
    def __init__(self, **kwargs):
        super(AnalogClock, self).__init__(**kwargs)
        
        # 加载时钟图像
        self.clock_face_texture = CoreImage(get_resource_path("clock_face.png")).texture
        self.hour_hand_texture = CoreImage(get_resource_path("hour_hand.png")).texture
        self.minute_hand_texture = CoreImage(get_resource_path("minute_hand.png")).texture
        self.second_hand_texture = CoreImage(get_resource_path("second_hand.png")).texture

        # 存储原始纹理尺寸
        self.original_face_size = (self.clock_face_texture.width, self.clock_face_texture.height)
        self.original_hour_size = (self.hour_hand_texture.width, self.hour_hand_texture.height)
        self.original_minute_size = (self.minute_hand_texture.width, self.minute_hand_texture.height)
        self.original_second_size = (self.second_hand_texture.width, self.second_hand_texture.height)
        
        # 计算指针相对于钟盘的原始比例
        self.hour_scale_x = self.original_hour_size[0] / self.original_face_size[0]
        self.hour_scale_y = self.original_hour_size[1] / self.original_face_size[1]
        
        self.minute_scale_x = self.original_minute_size[0] / self.original_face_size[0]
        self.minute_scale_y = self.original_minute_size[1] / self.original_face_size[1]
        
        self.second_scale_x = self.original_second_size[0] / self.original_face_size[0]
        self.second_scale_y = self.original_second_size[1] / self.original_face_size[1]
        
        # 初始化旋转指令和矩形指令的引用
        self.hour_rotate = None
        self.minute_rotate = None
        self.second_rotate = None
        self.hour_rect = None
        self.minute_rect = None
        self.second_rect = None
        self.face_rect = None
        
        # 绑定尺寸变化事件
        self.bind(pos=self.update_rectangles, size=self.update_rectangles)
        
        # 初始绘制
        self.init_canvas()
    
    def calculate_clock_size(self):
        """计算保持长宽比的时钟实际显示尺寸"""
        # 获取可用空间
        available_width, available_height = self.size
        
        # 计算保持长宽比的最大正方形尺寸
        clock_size = min(available_width, available_height)
        
        # 计算居中位置
        clock_x = self.x + (available_width - clock_size) / 2
        clock_y = self.y + (available_height - clock_size) / 2
        
        return (clock_x, clock_y, clock_size, clock_size)
    
    def calculate_hand_size(self, scale_x, scale_y, clock_size):
        """根据比例计算指针的实际显示尺寸"""
        # 计算指针的显示尺寸（保持原始比例）
        hand_width = clock_size * scale_x
        hand_height = clock_size * scale_y
        
        return (hand_width, hand_height)
    
    def calculate_hand_position(self, hand_width, hand_height, clock_center_x, clock_center_y, pivot):
        """计算指针的位置（使用固定的旋转中心点）"""
        # 计算指针位置，使其指定的旋转中心点与钟盘中心对齐
        pivot_x = hand_width * pivot[0]  # 旋转中心点在指针图像中的x坐标
        pivot_y = hand_height * pivot[1]  # 旋转中心点在指针图像中的y坐标
        
        # 计算指针位置，使指定的旋转中心点对齐钟盘中心
        pos_x = clock_center_x - pivot_x
        pos_y = clock_center_y - pivot_y
        
        return (pos_x, pos_y)
    
    def init_canvas(self):
        """初始化画布，只执行一次"""
        self.canvas.clear()
        
        with self.canvas:
            # 计算保持长宽比的时钟尺寸和位置
            clock_x, clock_y, clock_width, clock_height = self.calculate_clock_size()
            clock_center_x = clock_x + clock_width / 2
            clock_center_y = clock_y + clock_height / 2
            
            # 绘制钟盘
            Color(1, 1, 1, 1)
            self.face_rect = Rectangle(
                texture=self.clock_face_texture,
                pos=(clock_x, clock_y),
                size=(clock_width, clock_height)
            )
            
            # 计算指针的显示尺寸和位置
            hour_size = self.calculate_hand_size(self.hour_scale_x, self.hour_scale_y, clock_width)
            hour_pos = self.calculate_hand_position(hour_size[0], hour_size[1], clock_center_x, clock_center_y, self.hour_pivot)
            
            minute_size = self.calculate_hand_size(self.minute_scale_x, self.minute_scale_y, clock_width)
            minute_pos = self.calculate_hand_position(minute_size[0], minute_size[1], clock_center_x, clock_center_y, self.minute_pivot)
            
            second_size = self.calculate_hand_size(self.second_scale_x, self.second_scale_y, clock_width)
            second_pos = self.calculate_hand_position(second_size[0], second_size[1], clock_center_x, clock_center_y, self.second_pivot)
            
            # 绘制时针 - 保存旋转指令和矩形指令的引用
            PushMatrix()
            self.hour_rotate = Rotate(origin=(clock_center_x, clock_center_y), angle=-self.hour_angle + 90)
            self.hour_rect = Rectangle(
                texture=self.hour_hand_texture,
                pos=hour_pos,
                size=hour_size
            )
            PopMatrix()
            
            # 绘制分针 - 保存旋转指令和矩形指令的引用
            PushMatrix()
            self.minute_rotate = Rotate(origin=(clock_center_x, clock_center_y), angle=-self.minute_angle + 90)
            self.minute_rect = Rectangle(
                texture=self.minute_hand_texture,
                pos=minute_pos,
                size=minute_size
            )
            PopMatrix()
            
            # 绘制秒针 - 保存旋转指令和矩形指令的引用
            PushMatrix()
            self.second_rotate = Rotate(origin=(clock_center_x, clock_center_y), angle=-self.second_angle + 90)
            self.second_rect = Rectangle(
                texture=self.second_hand_texture,
                pos=second_pos,
                size=second_size
            )
            PopMatrix()
    
    def update_rectangles(self, instance, value):
        """更新矩形位置和大小"""
        # 计算保持长宽比的时钟尺寸和位置
        clock_x, clock_y, clock_width, clock_height = self.calculate_clock_size()
        clock_center_x = clock_x + clock_width / 2
        clock_center_y = clock_y + clock_height / 2
        
        # 更新钟盘位置和大小
        if self.face_rect:
            self.face_rect.pos = (clock_x, clock_y)
            self.face_rect.size = (clock_width, clock_height)
        
        # 重新计算指针的显示尺寸和位置
        hour_size = self.calculate_hand_size(self.hour_scale_x, self.hour_scale_y, clock_width)
        hour_pos = self.calculate_hand_position(hour_size[0], hour_size[1], clock_center_x, clock_center_y, self.hour_pivot)
        
        minute_size = self.calculate_hand_size(self.minute_scale_x, self.minute_scale_y, clock_width)
        minute_pos = self.calculate_hand_position(minute_size[0], minute_size[1], clock_center_x, clock_center_y, self.minute_pivot)
        
        second_size = self.calculate_hand_size(self.second_scale_x, self.second_scale_y, clock_width)
        second_pos = self.calculate_hand_position(second_size[0], second_size[1], clock_center_x, clock_center_y, self.second_pivot)
        
        # 更新指针位置和大小
        if self.hour_rect:
            self.hour_rect.pos = hour_pos
            self.hour_rect.size = hour_size
        
        if self.minute_rect:
            self.minute_rect.pos = minute_pos
            self.minute_rect.size = minute_size
        
        if self.second_rect:
            self.second_rect.pos = second_pos
            self.second_rect.size = second_size
        
        # 更新旋转原点
        if self.hour_rotate:
            self.hour_rotate.origin = (clock_center_x, clock_center_y)
        
        if self.minute_rotate:
            self.minute_rotate.origin = (clock_center_x, clock_center_y)
        
        if self.second_rotate:
            self.second_rotate.origin = (clock_center_x, clock_center_y)
    
    def update_time(self, hours, minutes, seconds):
        """更新时间指针角度"""
        self.hour_angle = (hours % 12) * 30 + minutes * 0.5
        self.minute_angle = minutes * 6 + seconds * 0.1
        self.second_angle = seconds * 6
        
        # 只更新旋转角度，而不是重绘整个画布
        if self.hour_rotate:
            self.hour_rotate.angle = -self.hour_angle + 90
        
        if self.minute_rotate:
            self.minute_rotate.angle = -self.minute_angle + 90
        
        if self.second_rotate:
            self.second_rotate.angle = -self.second_angle + 90