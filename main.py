from datetime import datetime
from src.timeaccelerator import AdaptiveTimeChaser
from kivymd.app import MDApp
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from src.clock import AnalogClock
from src.audio import AudioPlayer
from src.data import TimeDataManager
from kivy.clock import Clock
from kivy.core.window import Window
import time
from src.panel import StatusPanel

class TimeCatchClockApp(MDApp):
    """主应用程序类"""
    # 属性定义
    is_catching_up = NumericProperty(0)  # 0:正常, 1:追赶中, 2:完成追赶
    
    def build(self):
        # 创建主布局
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 创建模拟时钟部件
        self.analog_clock = AnalogClock(size_hint=(1, 1))
        main_layout.add_widget(self.analog_clock)
        
        # 创建状态面板
        self.status_panel = StatusPanel()
        main_layout.add_widget(self.status_panel)
        
        # 初始化音频播放器
        self.audio_player = AudioPlayer()
        
        # 初始化时间数据管理器
        self.time_data_manager = TimeDataManager()
        
        # 加载时间数据
        self.time_data_manager.load_time_data()
        
        # 根据是否有保存的时间决定行为
        current_time = time.time()
        if abs(current_time - self.time_data_manager.user_time) > 1.0:
            self.start_catchup_mode()
        else:
            self.start_normal_mode()
        
        return main_layout
    
    def start_normal_mode(self):
        """启动正常时钟模式"""
        self.is_catching_up = 0
        self.status_panel.status_text = "normal mode"
        Clock.unschedule(self.update_catchup_time)
        Clock.schedule_interval(self.update_normal_time, 1)
        
        # 更新用户时间为当前时间
        self.time_data_manager.set_user_time()
    
    def start_catchup_mode(self):
        """启动时间追赶模式"""
        self.is_catching_up = 1
        
        # 使用保存的用户时间作为起点
        self.saved_time = self.time_data_manager.user_time
        self.current_display_time = self.saved_time
        
        # 初始化自适应时间追赶器
        self.time_chaser = AdaptiveTimeChaser(self.saved_time)
        
        self.status_panel.status_text = "追赶模式-加速阶段"
        
        # 开始加速追赶
        Clock.unschedule(self.update_normal_time)
        Clock.schedule_interval(self.update_catchup_time, 1/30)  # 30fps更新以获得平滑的动画
        #self.audio_player.play_catchup()
        Clock.schedule_once(lambda dt: self.audio_player.play_crucified(), 2)
        
        # 初始更新一次显示
        self.update_display_from_time(self.saved_time)
    
    def update_normal_time(self, dt):
        """更新正常时间显示"""
        now = datetime.now()
        hours, minutes, seconds = now.hour, now.minute, now.second
        
        # 更新模拟时钟
        self.analog_clock.update_time(hours, minutes, seconds)
        
        # 更新数字时钟
        self.status_panel.digital_time = now.strftime("%H:%M:%S")
        
        # 播放滴答声
        self.audio_player.play_tick()
    
    def update_catchup_time(self, dt):
        """更新追赶时间显示"""
        # 更新时间追赶器
        status = self.time_chaser.update()
        
        # 获取当前追赶时间
        self.current_display_time = status["current_xt"]
        
        # 更新显示
        display_dt = datetime.fromtimestamp(self.current_display_time)
        hours, minutes, seconds = display_dt.hour, display_dt.minute, display_dt.second
        self.analog_clock.update_time(hours, minutes, seconds)
        self.status_panel.digital_time = display_dt.strftime("%H:%M:%S")
        
        # 计算追赶速度（用于音效）
        if status["dt"] > 0:
            speed = (status["current_xt"] - self.last_display_time) / status["dt"] if hasattr(self, 'last_display_time') else 1
            self.status_panel.update_speed(speed)
            
            # 根据速度调整滴答声速率
            #self.audio_player.play_tick(min(max(speed, 0.5), 2.0))
            
        self.last_display_time = status["current_xt"]
        
        # 更新状态信息
        if status["phase"] == "accelerating":
            self.status_panel.status_text = f"追赶模式-加速中 速度: {speed:.1f}x"
        elif status["phase"] == "decelerating":
            self.status_panel.status_text = f"追赶模式-减速中 速度: {speed:.1f}x"
            self.audio_player.stop_crucified()
        
        # 检查是否完成追赶
        if self.time_chaser.is_completed():
            self.complete_catchup()
    
    def update_display_from_time(self, timestamp):
        """从时间戳更新显示"""
        display_dt = datetime.fromtimestamp(timestamp)
        hours, minutes, seconds = display_dt.hour, display_dt.minute, display_dt.second
        self.analog_clock.update_time(hours, minutes, seconds)
        self.status_panel.digital_time = display_dt.strftime("%H:%M:%S")
    
    def complete_catchup(self):
        """完成时间追赶"""
        self.is_catching_up = 2
        self.status_panel.status_text = "completed"
        Clock.unschedule(self.update_catchup_time)
        
        self.audio_player.stop_crucified()

        # 更新用户时间为当前时间
        self.time_data_manager.set_user_time()
        
        # 恢复正常时间更新
        Clock.schedule_once(lambda dt: self.start_normal_mode())
        
        # 停止追赶音效
        self.audio_player.stop_all()
    def on_start(self):
        """应用启动时的初始化"""
        Window.size = (800, 1000)
    def on_stop(self):
        """应用关闭时保存当前时间"""
        self.time_data_manager.save_time_data()
        self.audio_player.stop_all()


if __name__ == '__main__':
    TimeCatchClockApp().run()