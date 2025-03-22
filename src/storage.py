"""
故事存储模块
负责故事文件的读取、保存和管理
"""

import os
import json
import sys
import shutil
from datetime import datetime

# 导入配置和工具
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import STORIES_DIR, STATE_FILE, USE_ATOMIC_WRITE, BACKUP_COUNT
from utils.logger import get_logger, log_operation, log_exception

# 获取日志记录器
logger = get_logger('story_storage')

def create_story_path(language_code, region, category, story_type):
    """
    创建故事文件路径
    
    Args:
        language_code: 语言代码
        region: 地区
        category: 分类
        story_type: 故事类型
        
    Returns:
        path: 创建的路径
    """
    # 安全处理输入，避免路径注入
    language_code = language_code.replace('/', '_').replace('\\', '_')
    region = region.replace('/', '_').replace('\\', '_')
    category = category.replace('/', '_').replace('\\', '_')
    story_type = story_type.replace('/', '_').replace('\\', '_')
    
    # 创建目录结构
    base_dir = os.path.join(STORIES_DIR, f"{category}")
    language_dir = os.path.join(base_dir, f"{language_code}_{region}")
    type_dir = os.path.join(language_dir, f"{story_type}")
    
    # 确保目录存在
    for dir_path in [base_dir, language_dir, type_dir]:
        os.makedirs(dir_path, exist_ok=True)
        
    return type_dir

def generate_story_filename(title, language_code, story_number=None):
    """
    生成故事文件名
    
    Args:
        title: 故事标题
        language_code: 语言代码
        story_number: 故事编号
        
    Returns:
        filename: 生成的文件名
    """
    # 安全处理标题，移除不适合文件名的字符
    safe_title = "".join(c for c in title if c.isalnum() or c in [' ', '-', '_']).strip()
    safe_title = safe_title.replace(' ', '_')[:50]  # 截断长标题
    
    # 如果没有提供故事编号，则使用时间戳
    if not story_number:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        story_number = f"{timestamp}"
    
    return f"{language_code}{story_number}_{safe_title}.md"

def save_story(story_data, content):
    """
    保存故事到文件
    
    Args:
        story_data: 故事元数据
        content: 故事内容
        
    Returns:
        (success, filepath): 是否成功和保存的文件路径
    """
    try:
        # 提取必要信息
        language_code = story_data.get('language_code', 'XX')
        region = story_data.get('region', 'Unknown')
        category = story_data.get('category', 'traditional')
        story_type = story_data.get('type', 'general')
        title = story_data.get('title', 'Untitled Story')
        story_number = story_data.get('story_number')
        
        # 创建目录
        story_dir = create_story_path(language_code, region, category, story_type)
        
        # 生成文件名
        filename = generate_story_filename(title, language_code, story_number)
        filepath = os.path.join(story_dir, filename)
        
        # 检查文件是否已存在
        if os.path.exists(filepath):
            log_operation(logger, "保存故事", "警告", f"故事文件已存在: {filepath}")
            return False, filepath
        
        # 保存文件
        if USE_ATOMIC_WRITE:
            temp_filepath = filepath + ".tmp"
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            os.rename(temp_filepath, filepath)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        log_operation(logger, "保存故事", "成功", f"保存到: {filepath}")
        
        # 更新状态文件
        update_state_file(story_data, filepath)
        
        return True, filepath
        
    except Exception as e:
        log_exception(logger, e, f"保存故事失败: {title}")
        return False, None

def update_state_file(story_data, filepath):
    """
    更新状态文件
    
    Args:
        story_data: 故事数据
        filepath: 保存的文件路径
    """
    try:
        # 加载现有状态
        state = {}
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    state = json.load(f)
            except json.JSONDecodeError:
                state = {}
        
        # 确保stories列表存在
        if 'stories' not in state:
            state['stories'] = []
        
        # 添加新故事记录
        story_record = {
            'title': story_data.get('title', 'Untitled'),
            'language_code': story_data.get('language_code', 'XX'),
            'region': story_data.get('region', 'Unknown'),
            'category': story_data.get('category', 'traditional'),
            'type': story_data.get('type', 'general'),
            'filepath': filepath,
            'collected_at': datetime.now().isoformat()
        }
        
        state['stories'].append(story_record)
        state['last_updated'] = datetime.now().isoformat()
        
        # 保存状态文件
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            
        log_operation(logger, "更新状态文件", "成功")
        
    except Exception as e:
        log_exception(logger, e, "更新状态文件失败")

def get_existing_stories():
    """
    获取已存在的故事列表
    
    Returns:
        stories: 故事列表
    """
    stories = []
    
    try:
        # 从状态文件加载
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
                stories = state.get('stories', [])
        
        # 如果状态文件为空，则扫描目录
        if not stories:
            for root, dirs, files in os.walk(STORIES_DIR):
                for file in files:
                    if file.endswith('.md'):
                        filepath = os.path.join(root, file)
                        relative_path = os.path.relpath(filepath, STORIES_DIR)
                        parts = relative_path.split(os.sep)
                        
                        if len(parts) >= 3:
                            category = parts[0]
                            language_region = parts[1]
                            language_code = language_region.split('_')[0] if '_' in language_region else 'XX'
                            region = language_region.split('_')[1] if '_' in language_region else 'Unknown'
                            
                            story_record = {
                                'title': file[:-3],  # 移除.md后缀
                                'language_code': language_code,
                                'region': region,
                                'category': category,
                                'type': parts[2] if len(parts) > 3 else 'general',
                                'filepath': filepath,
                                'collected_at': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                            }
                            
                            stories.append(story_record)
        
        return stories
        
    except Exception as e:
        log_exception(logger, e, "获取现有故事列表失败")
        return []

def backup_file(filepath):
    """
    备份文件
    
    Args:
        filepath: 要备份的文件路径
        
    Returns:
        backup_path: 备份文件路径
    """
    try:
        if not os.path.exists(filepath):
            return None
            
        # 创建备份文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_path = f"{filepath}.{timestamp}.bak"
        
        # 复制文件
        shutil.copy2(filepath, backup_path)
        
        # 清理旧备份
        cleanup_old_backups(filepath)
        
        return backup_path
        
    except Exception as e:
        log_exception(logger, e, f"备份文件失败: {filepath}")
        return None

def cleanup_old_backups(filepath):
    """
    清理旧备份文件，只保留最新的几个
    
    Args:
        filepath: 原始文件路径
    """
    try:
        # 获取目录和文件名
        dirname = os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        
        # 查找所有备份
        backups = []
        for filename in os.listdir(dirname):
            if filename.startswith(f"{basename}.") and filename.endswith('.bak'):
                backup_path = os.path.join(dirname, filename)
                backups.append((backup_path, os.path.getmtime(backup_path)))
        
        # 按修改时间排序
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # 删除超出数量的备份
        if len(backups) > BACKUP_COUNT:
            for backup_path, _ in backups[BACKUP_COUNT:]:
                os.remove(backup_path)
                log_operation(logger, "清理备份", "成功", f"删除旧备份: {backup_path}")
                
    except Exception as e:
        log_exception(logger, e, f"清理旧备份失败: {filepath}")

def read_story(filepath):
    """
    读取故事文件
    
    Args:
        filepath: 故事文件路径
        
    Returns:
        content: 文件内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        log_exception(logger, e, f"读取故事文件失败: {filepath}")
        return None 