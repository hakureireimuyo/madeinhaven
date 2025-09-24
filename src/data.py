import json
import os
import time
from datetime import datetime
from src.res import get_resource_path

class TimeDataManager:
    """时间数据管理器，处理时间数据的加载和保存"""
    
    def __init__(self, filename='time_data.json'):
        self.filename = get_resource_path(filename)
        self.user_time = 0  # 用户设定的时间戳
        self.last_open_time = 0  # 上次打开应用的时间戳
    
    def load_time_data(self):
        """从JSON文件加载保存的时间数据"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.user_time = data.get('user_time', 0)
                    self.last_open_time = data.get('last_open_time', 0)
                    return True
            else:
                # 如果文件不存在，初始化默认值
                self.user_time = time.time()
                self.last_open_time = time.time()
                self.save_time_data()
                return True
        except Exception as e:
            print(f"加载时间数据失败: {e}")
            # 出错时使用当前时间作为默认值
            self.user_time = time.time()
            self.last_open_time = time.time()
            return False
    
    def save_time_data(self):
        """保存当前时间数据到JSON文件"""
        try:
            # 更新最后打开时间为当前时间
            self.last_open_time = time.time()
            
            data = {
                'user_time': self.user_time,
                'last_open_time': self.last_open_time
            }
            
            with open(self.filename, 'w') as f:
                json.dump(data, f)
            
            return True
        except Exception as e:
            print(f"保存时间数据失败: {e}")
            return False
    
    def set_user_time(self, timestamp=None):
        """
        设置用户时间
        
        参数:
        timestamp (float, optional): 要设置的时间戳，如果为None则设置为当前时间
        
        返回:
        bool: 设置是否成功
        """
        try:
            if timestamp is None:
                self.user_time = time.time()
            else:
                self.user_time = float(timestamp)
            
            return self.save_time_data()
        except Exception as e:
            print(f"设置用户时间失败: {e}")
            return False
    
    def set_user_time_from_string(self, time_string, format="%Y-%m-%d %H:%M:%S"):
        """
        从字符串设置用户时间
        
        参数:
        time_string (str): 时间字符串
        format (str): 时间字符串的格式
        
        返回:
        bool: 设置是否成功
        """
        try:
            dt = datetime.strptime(time_string, format)
            self.user_time = dt.timestamp()
            return self.save_time_data()
        except Exception as e:
            print(f"从字符串设置用户时间失败: {e}")
            return False
    
    def set_user_time_delta(self, days=0, hours=0, minutes=0, seconds=0):
        """
        基于当前时间设置一个偏移量
        
        参数:
        days (int): 天数偏移
        hours (int): 小时偏移
        minutes (int): 分钟偏移
        seconds (int): 秒偏移
        
        返回:
        bool: 设置是否成功
        """
        try:
            current_time = time.time()
            offset = days * 86400 + hours * 3600 + minutes * 60 + seconds
            self.user_time = current_time + offset
            return self.save_time_data()
        except Exception as e:
            print(f"设置时间偏移失败: {e}")
            return False
    
    def get_user_time(self):
        """获取用户时间的时间戳"""
        return self.user_time
    
    def get_user_time_string(self, format="%Y-%m-%d %H:%M:%S"):
        """获取用户时间的格式化字符串"""
        return datetime.fromtimestamp(self.user_time).strftime(format)
    
    def get_last_open_time(self):
        """获取上次打开应用的时间戳"""
        return self.last_open_time
    
    def get_last_open_time_string(self, format="%Y-%m-%d %H:%M:%S"):
        """获取上次打开应用的格式化字符串"""
        return datetime.fromtimestamp(self.last_open_time).strftime(format)
    
    def get_time_difference(self):
        """获取当前时间与用户时间的差值（秒）"""
        return time.time() - self.user_time
    
    def get_time_difference_string(self):
        """获取当前时间与用户时间差值的可读字符串"""
        diff = self.get_time_difference()
        if diff < 0:
            return f"未来 {-diff:.0f} 秒"
        
        days = diff // 86400
        hours = (diff % 86400) // 3600
        minutes = (diff % 3600) // 60
        seconds = diff % 60
        
        if days > 0:
            return f"{int(days)}天 {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒前"
        elif hours > 0:
            return f"{int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒前"
        elif minutes > 0:
            return f"{int(minutes)}分钟 {int(seconds)}秒前"
        else:
            return f"{int(seconds)}秒前"


# 测试代码
if __name__ == "__main__":
    # 创建时间数据管理器实例
    time_manager = TimeDataManager("test_time_data.json")
    
    # 加载时间数据
    time_manager.load_time_data()
    
    print(f"当前用户时间: {time_manager.get_user_time_string()}")
    print(f"上次打开时间: {time_manager.get_last_open_time_string()}")
    print(f"时间差: {time_manager.get_time_difference_string()}")
    
    # 测试设置用户时间
    print("\n=== 测试设置用户时间 ===")
    
    # 方法1: 设置为当前时间
    time_manager.set_user_time()
    print(f"设置为当前时间: {time_manager.get_user_time_string()}")
    
    # 方法2: 设置为特定时间戳
    past_time = time.time() - 3600  # 1小时前
    time_manager.set_user_time(past_time)
    print(f"设置为1小时前: {time_manager.get_user_time_string()}")
    print(f"时间差: {time_manager.get_time_difference_string()}")
    
    # 方法3: 从字符串设置时间
    time_manager.set_user_time_from_string("2023-01-01 12:00:00")
    print(f"设置为2023年元旦: {time_manager.get_user_time_string()}")
    print(f"时间差: {time_manager.get_time_difference_string()}")
    
    # 方法4: 设置时间偏移
    time_manager.set_user_time_delta(days=-1, hours=-2)  # 1天2小时前
    print(f"设置为1天2小时前: {time_manager.get_user_time_string()}")
    print(f"时间差: {time_manager.get_time_difference_string()}")