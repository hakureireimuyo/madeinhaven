import os
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from kivy.graphics.texture import Texture
from kivy.logger import Logger
from kivy.resources import resource_find, resource_add_path

# 全局缓存字典
_texture_cache = {}
_sound_cache = {}
_resource_paths = {}

def initialize_resource_paths():
    """初始化资源路径，应该在应用启动时调用"""
    # 添加资源路径
    base_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "..", "data")
    
    if os.path.exists(data_path):
        resource_add_path(data_path)
        Logger.info(f"Added resource path: {data_path}")
    else:
        Logger.warning(f"Data path not found: {data_path}")

def get_resource_path(relative_path):
    """
    获取资源路径，使用Kivy的资源查找机制
    """
    Logger.debug(f"Getting resource path for: {relative_path}")
    # 首先检查缓存
    if relative_path in _resource_paths:
        return _resource_paths[relative_path]
    
    # 使用Kivy的资源查找
    path = resource_find(relative_path)
    
    # 如果Kivy找不到，尝试回退到基于当前目录的查找
    if path is None:
        base_path = os.path.abspath(os.path.dirname(__file__))
        fallback_path = os.path.join(base_path, "..", "data", relative_path)
        if os.path.exists(fallback_path):
            path = fallback_path
    
    # 缓存路径
    _resource_paths[relative_path] = path
    return path

def create_default_texture(width=64, height=64):
    """创建默认纹理"""
    # 创建一个简单的棋盘格纹理作为默认纹理
    texture = Texture.create(size=(width, height))
    buf = bytearray(width * height * 4)
    
    # 创建棋盘格图案
    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 4
            # 棋盘格图案
            if (x // 8 + y // 8) % 2 == 0:
                buf[idx] = 255    # R
                buf[idx+1] = 0    # G
                buf[idx+2] = 0    # B
                buf[idx+3] = 255  # A
            else:
                buf[idx] = 255    # R
                buf[idx+1] = 255  # G
                buf[idx+2] = 255  # B
                buf[idx+3] = 255  # A
    
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture

def create_missing_texture(width=64, height=64):
    """创建缺失资源提示纹理"""
    # 创建一个带有错误信息的纹理
    texture = Texture.create(size=(width, height))
    buf = bytearray(width * height * 4)
    
    # 填充红色背景
    for i in range(0, len(buf), 4):
        buf[i] = 255      # R
        buf[i+1] = 0      # G
        buf[i+2] = 0      # B
        buf[i+3] = 255    # A
    
    # 在中心添加一个白色十字
    center_x, center_y = width // 2, height // 2
    cross_size = min(width, height) // 4
    
    for y in range(center_y - cross_size, center_y + cross_size):
        for x in range(center_x - 2, center_x + 2):
            if 0 <= y < height and 0 <= x < width:
                idx = (y * width + x) * 4
                buf[idx] = 255      # R
                buf[idx+1] = 255    # G
                buf[idx+2] = 255    # B
    
    for y in range(center_y - 2, center_y + 2):
        for x in range(center_x - cross_size, center_x + cross_size):
            if 0 <= y < height and 0 <= x < width:
                idx = (y * width + x) * 4
                buf[idx] = 255      # R
                buf[idx+1] = 255    # G
                buf[idx+2] = 255    # B
    
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    return texture

def get_texture(relative_path, use_default=True):
    """
    获取纹理资源
    
    参数:
    relative_path (str): 资源相对路径
    use_default (bool): 如果资源不存在，是否使用默认纹理
    
    返回:
    Texture: 纹理对象
    """
    # 检查缓存
    if relative_path in _texture_cache:
        return _texture_cache[relative_path]
    
    # 获取资源路径
    resource_path = get_resource_path(relative_path)
    
    # 检查资源是否存在
    if resource_path is None or not os.path.exists(resource_path):
        if use_default:
            # 使用默认纹理
            default_texture = create_missing_texture()
            _texture_cache[relative_path] = default_texture
            Logger.warning(f"Using default texture for missing resource: {relative_path}")
            return default_texture
        else:
            Logger.error(f"Texture not found: {relative_path}")
            return None
    
    # 加载纹理
    try:
        texture = CoreImage(resource_path).texture
        _texture_cache[relative_path] = texture
        Logger.info(f"Loaded texture: {relative_path}")
        return texture
    except Exception as e:
        if use_default:
            # 使用默认纹理
            default_texture = create_missing_texture()
            _texture_cache[relative_path] = default_texture
            Logger.warning(f"Using default texture for failed load: {relative_path}, error: {e}")
            return default_texture
        else:
            Logger.error(f"Failed to load texture {relative_path}: {e}")
            return None

def get_sound(relative_path):
    """
    获取声音资源
    
    参数:
    relative_path (str): 资源相对路径
    
    返回:
    Sound: 声音对象，如果资源不存在则返回None
    """
    # 检查缓存
    if relative_path in _sound_cache:
        return _sound_cache[relative_path]
    
    # 获取资源路径
    resource_path = get_resource_path(relative_path)
    
    # 检查资源是否存在
    if resource_path is None or not os.path.exists(resource_path):
        Logger.error(f"Sound not found: {relative_path}")
        return None
    
    # 加载声音
    try:
        sound = SoundLoader.load(resource_path)
        if sound:
            _sound_cache[relative_path] = sound
            Logger.info(f"Loaded sound: {relative_path}")
        return sound
    except Exception as e:
        Logger.error(f"Failed to load sound {relative_path}: {e}")
        return None

def preload_resources(resource_list):
    """
    预加载一组资源
    
    参数:
    resource_list (list): 资源路径列表
    """
    for resource_path in resource_list:
        if resource_path.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            get_texture(resource_path)
        elif resource_path.endswith(('.wav', '.mp3', '.ogg', '.m4a')):
            get_sound(resource_path)

def clear_cache():
    """清空资源缓存"""
    global _texture_cache, _sound_cache, _resource_paths
    _texture_cache.clear()
    _sound_cache.clear()
    _resource_paths.clear()
    Logger.info("Cleared resource cache")

def list_cached_resources():
    """
    列出当前缓存中的所有资源
    
    返回:
    dict: 包含缓存资源的字典，按资源类型分类
    """
    from collections import defaultdict
    result = defaultdict(list)
    
    # 列出纹理缓存
    for path, texture in _texture_cache.items():
        result["Textures"].append({
            "path": path,
            "size": f"{texture.width}x{texture.height}" if hasattr(texture, 'width') else "Unknown"
        })
    
    # 列出声音缓存
    for path, sound in _sound_cache.items():
        result["Sounds"].append({
            "path": path,
            "state": sound.state if hasattr(sound, 'state') else "Unknown"
        })
    
    return dict(result)

def print_cached_resources():
    """打印当前缓存中的所有资源信息"""
    cached_resources = list_cached_resources()
    
    print("=" * 80)
    print("Cached Resources Report")
    print("=" * 80)
    
    total_resources = 0
    for resource_type, resources in cached_resources.items():
        print(f"\n{resource_type} ({len(resources)}):")
        print("-" * 40)
        
        for resource in resources:
            print(f"  {resource['path']}")
            for key, value in resource.items():
                if key != "path":
                    print(f"    {key}: {value}")
        
        total_resources += len(resources)
    
    print("=" * 80)
    print(f"Total Resources: {total_resources}")
    print("=" * 80)