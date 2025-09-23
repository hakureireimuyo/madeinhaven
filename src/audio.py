from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from src.evn import get_resource_path

class AudioPlayer:
    """音频播放器类，处理音频加速效果"""
    def __init__(self):
        self.tick_sound = SoundLoader.load(get_resource_path('tick_sound.wav'))
        self.catchup_sound = SoundLoader.load(get_resource_path('catchup_sound.wav'))
        self.crucified_sound = SoundLoader.load(get_resource_path('crucified.wav'))
        self.current_rate = 1.0
        
        # 淡出相关属性
        self.is_fading_out = False
        self.fade_out_event = None
    
    def play_tick(self, rate=1.0):
        """播放滴答声"""
        if self.tick_sound:
            self.tick_sound.rate = rate
            self.tick_sound.play()
            self.current_rate = rate
    
    def stop_tick(self):
        """停止滴答声"""
        if self.tick_sound and self.tick_sound.state == 'play':
            self.tick_sound.stop()
    
    def play_crucified(self):
        """播放被十字架打死声"""
        if self.crucified_sound:
            # 重置淡出状态
            self.is_fading_out = False
            if self.fade_out_event:
                Clock.unschedule(self.fade_out_event)
                self.fade_out_event = None
                
            # 重置音量并播放
            self.crucified_sound.volume = 1.0
            self.crucified_sound.play()
            self.current_rate = 1.0
    
    def stop_crucified(self):
        """停止被十字架打死声（带淡出效果）"""
        if (self.crucified_sound and 
            self.crucified_sound.state == 'play' and 
            not self.is_fading_out):
            
            self.is_fading_out = True
            self._start_fade_out()
    
    def _start_fade_out(self):
        """开始淡出过程"""
        # 淡出持续时间（秒）
        fade_duration = 5.0
        # 淡出步数
        fade_steps = 20
        # 每一步的时间间隔
        step_interval = fade_duration / fade_steps
        # 每一步的音量减少量
        volume_step = 1.0 / fade_steps
        
        # 当前音量
        current_volume = self.crucified_sound.volume
        
        def fade_step(dt):
            nonlocal current_volume
            if current_volume > 0:
                current_volume -= volume_step
                if current_volume < 0:
                    current_volume = 0
                
                self.crucified_sound.volume = current_volume
                
                # 如果音量已经为0，停止声音并重置状态
                if current_volume <= 0:
                    self.crucified_sound.stop()
                    self.is_fading_out = False
                    self.fade_out_event = None
                    return False  # 停止调度
            
            return True  # 继续调度
        
        # 开始淡出调度
        self.fade_out_event = Clock.schedule_interval(fade_step, step_interval)
    
    def play_catchup(self):
        """播放追赶音效"""
        if self.catchup_sound:
            self.catchup_sound.play()
    
    def stop_catchup(self):
        """停止追赶音效"""
        if self.catchup_sound and self.catchup_sound.state == 'play':
            self.catchup_sound.stop()
    
    def stop_all(self):
        """停止所有音效"""
        self.stop_tick()
        self.stop_catchup()
        
        # 对于crucified音效，如果正在淡出，则取消淡出并立即停止
        if self.fade_out_event:
            Clock.unschedule(self.fade_out_event)
            self.fade_out_event = None
        
        if self.crucified_sound and self.crucified_sound.state == 'play':
            self.crucified_sound.stop()
        
        self.is_fading_out = False