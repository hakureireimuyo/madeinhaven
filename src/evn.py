import sys
import os
from pathlib import Path

def get_resource_path(relative_path=""):
    """
    获取资源的绝对路径，兼容开发环境和打包环境。
    
    参数:
        relative_path (str): 相对于资源根目录的路径，例如 'config.ini'
        
    返回:
        str: 资源的绝对路径字符串
    """
    # 判断是否处于打包环境
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # 打包环境：使用sys._MEIPASS获取基础路径
        base_path = Path(getattr(sys, '_MEIPASS', ''))
    else:
        # 开发环境：使用当前文件所在目录的父目录作为基础路径
        base_path = Path(__file__).parent.parent
    
    # 拼接并返回完整资源路径
    resource_path = base_path / "data" / relative_path
    return str(resource_path.resolve())  # 转换为字符串


# 使用示例
if __name__ == "__main__":
    # 获取data文件夹的路径
    data_dir = get_resource_path()
    print(f"Data目录: {data_dir}")
    
    # 获取data目录下特定文件的路径
    config_file = get_resource_path("config.ini")
    print(f"配置文件路径: {config_file}")
    
    # 获取data子目录中的资源路径
    image_file = get_resource_path("images/background.jpg")
    print(f"图片文件路径: {image_file}")

    print(get_resource_path("clock_face.png"))