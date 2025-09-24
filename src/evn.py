import os
from kivy.resources import resource_find, resource_add_path

def get_resource_path(relative_path):
    """
    使用 Kivy 的资源查找机制获取资源路径。
    确保在打包前将资源所在路径添加到 Kivy 的资源系统中。
    """
    # 首先尝试直接查找（如果路径已通过 resource_add_path 添加过）
    result = resource_find(relative_path)
    if result:
        print(f"通过 resource_find 找到资源: {relative_path} -> {result}")
        return result
    else:
        # 如果未找到，可以尝试回退到基于当前目录的查找（主要用于开发环境）
        base_path = os.path.abspath(os.path.dirname(__file__))
        fallback_path = os.path.join(base_path, "..", "data", relative_path)
        fallback_path = os.path.abspath(fallback_path)
        
        print(f"尝试回退路径: {fallback_path}")
        print(f"回退路径存在: {os.path.exists(fallback_path)}")
        
        if os.path.exists(fallback_path):
            return fallback_path
        else:
            print(f"警告: 无法找到资源文件: {relative_path}")
            # 返回一个空字符串而不是 None，避免后续错误
            return ""

# 在应用初始化时，添加资源路径（重要！）
# 例如，在 main.py 的 App 类初始化或 build 方法中：
resource_add_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))

if __name__ == "__main__":
    # 测试资源路径查找
    print(get_resource_path("icon.png"))