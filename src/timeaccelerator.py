import time
import math

class AdaptiveTimeChaser:
    """
    一个自适应的时间追赶器，使用指数增长和衰减公式控制追赶过程。
    """
    
    def __init__(self, tt):
        """
        初始化自适应时间追赶器。
        
        参数:
        tt (float): 起点时间（以秒为单位的时间戳）
        """
        self.tt = tt  # 初始时间参数
        self.rt = 0.0  # 实际运行时间，累计dt
        self.xt = 0.0  # 变换时间，初始为0
        self.st = time.time()  # 当前系统时间
        
        if self.st <= tt:
            raise ValueError("当前系统时间必须大于起点时间tt")
        
        self.phase = "accelerating"  # 初始阶段为加速
        self.txt = 0.0  # 加速阶段结束时的xt值
        self.yt = 0.0  # 减速阶段使用的变量
        self.last_update_time = time.time()  # 上次更新时间
        self.dt = 0.0  # 时间片
        
    def update(self):
        """
        执行单次时间更新。
                
        返回:
        dict: 包含当前状态信息的字典
        """
        current_time = time.time()
        self.dt = current_time - self.last_update_time
        self.last_update_time = current_time
        self.rt += self.dt  # 累计实际运行时间
        self.st = current_time  # 更新当前系统时间
        
        # 确保dt为正值
        if self.dt <= 0:
            return self._get_status()
        
        if self.phase == "accelerating":
            return self._update_accelerating()
        elif self.phase == "decelerating":
            return self._update_decelerating()
        else:
            return self._get_status()
    
    def _update_accelerating(self):
        """更新加速阶段 - 使用指数增长"""
        # 加速阶段公式: xt = tt + e^rt
        self.xt = self.tt + math.exp(self.rt)
        
        # 检查加速阶段是否过半
        if self.rt > math.log((self.st - self.tt) * 0.85):
            self.phase = "decelerating"
            self.txt = self.xt  # 保存加速阶段结束时的xt值
            # 初始化yt: yt = 1/(ln(ditt+1.2))，其中ditt = st - xt
            self.ditt = self.st - self.xt
            self.yt = 10 / math.log(self.ditt + 1.2) + 0.1 if self.ditt + 1.2 > 0 else 1.0
            print(f"进入减速阶段: xt={self.xt:.6f}, st={self.st:.6f}, 差值={self.ditt:.6f}, yt={self.yt:.6f}")

        return self._get_status()
    
    def _update_decelerating(self):
        """更新减速阶段 - 使用距离关系公式"""
        rate = self.ditt - math.exp(10 / self.yt) -1.2
        if rate + 1 < self.ditt:
            self.xt = self.txt +  rate + self.yt * 1.2
        else:
            self.xt = self.txt +self.ditt+ self.yt * 1.2
        # print(f"rate={rate:.6f}, yt={self.yt:.6f}, xt={self.xt:.6f}, st={self.st:.6f}, 差值={(self.st - self.xt):.6f}")
        # 更新yt和rt
        self.yt += self.dt
        self.rt += self.dt
        
        # 检查是否完成追赶
        if self.st - self.xt < 0.5:
            self.phase = "completed"
            print(f"追赶完成: xt={self.xt:.6f}, st={self.st:.6f}, 差值={(self.st - self.xt):.6f}")
            return self._get_status()
        
        return self._get_status()
    
    def _get_status(self):
        """获取当前状态信息"""
        return {
            "current_xt": self.xt,
            "current_rt": self.rt,
            "current_st": self.st,
            "difference": self.st - self.xt,
            "phase": self.phase,
            "dt": self.dt,
            "yt": self.yt,
        }
    
    def get_current_time(self):
        """
        获取当前的变换时间xt。
        
        返回:
        float: 当前的变换时间xt
        """
        return self.xt
    
    def get_phase(self):
        """
        获取当前追赶阶段。
        
        返回:
        str: 当前阶段('accelerating', 'decelerating', 'completed')
        """
        return self.phase
    
    def is_completed(self):
        """
        检查追赶是否完成。
        
        返回:
        bool: 如果追赶完成返回True，否则返回False
        """
        return self.phase == "completed"

# 测试代码
if __name__ == "__main__":
    # 创建自适应时间追赶器实例，起点设置为一年前
    tt_test = time.time() - 31536000
    #tt_test = time.time() - 60  # 起点时间设为60秒前，便于测试
    chaser = AdaptiveTimeChaser(tt_test)
    
    print(f"起点时间 tt: {tt_test:.6f}")
    print(f"初始系统时间: {chaser.st:.6f}")
    print()
    
    # 模拟更新循环
    max_steps = 1000
    update_count = 0
    
    while not chaser.is_completed() and update_count < max_steps:
        status = chaser.update()
        update_count += 1
    
        print(f"更新 {update_count}: "
                f"阶段={status['phase']}, "
                f"xt={status['current_xt']:.6f}, "
                f"rt={status['current_rt']:.6f}, "
                f"差值={status['difference']:.6f}",
                f"dt={status['dt']:.6f}, "
                f"yt={status['yt']:.6f}")
        
        # 控制更新频率
        time.sleep(1/30)
    
    # 打印最终结果
    final_status = chaser._get_status()
    print("\n追赶完成!" if chaser.is_completed() else "\n达到最大更新次数!")
    print(f"最终 xt: {final_status['current_xt']:.6f}")
    print(f"最终 rt: {final_status['current_rt']:.6f}")
    print(f"当前系统时间: {final_status['current_st']:.6f}")
    print(f"最终差值: {abs(final_status['difference']):.6f} 秒")