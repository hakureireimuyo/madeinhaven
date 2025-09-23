from kivy.properties import NumericProperty, StringProperty, ObjectProperty,ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class StatusPanel(MDBoxLayout):
    """状态面板，包含数字时间标签和状态标签"""
    
    digital_time = StringProperty("00:00:00")
    status_text = StringProperty("Normal Mode")
    catchup_speed = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super(StatusPanel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.size_hint_y = None
        self.height = 100
        
        # 创建数字时间标签
        self.digital_label = MDLabel(
            text=self.digital_time,
            halign="center",
            size_hint=(1, None),
            height=50
        )
        self.add_widget(self.digital_label)
        
        # 创建状态标签
        self.status_label = MDLabel(
            text=self.status_text,
            halign="center",
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.status_label)
        
        # 绑定属性变化
        self.bind(digital_time=self.update_digital_time)
        self.bind(status_text=self.update_status_text)
    
    def update_digital_time(self, instance, value):
        """更新数字时间显示"""
        self.digital_label.text = value
    
    def update_status_text(self, instance, value):
        """更新状态文本"""
        self.status_label.text = value
    
    def update_speed(self, speed):
        """更新追赶速度显示"""
        self.catchup_speed = speed
        # 如果需要显示速度，可以在这里添加代码