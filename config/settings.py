"""
故事收集系统配置文件
包含系统设置和参数
"""

# 基本设置
PROJECT_NAME = "故事收集系统"
VERSION = "0.1.0"

# 路径设置
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORIES_DIR = os.path.join(BASE_DIR, "data", "stories")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
STATE_FILE = os.path.join(BASE_DIR, "data", "state.json")
TEMPLATE_FILE = os.path.join(BASE_DIR, "config", "story_template.md")

# 确保目录存在
for dir_path in [STORIES_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# 日志设置
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_LEVEL = "INFO"  # 可选: DEBUG, INFO, WARNING, ERROR, CRITICAL

# 故事设置
STORY_LANGUAGES = {
    'CN': '中文',
    'EN': '英文',
    'JP': '日文',
    'FR': '法文',
    'DE': '德文'
}

# 地区设置
STORY_REGIONS = {
    'CN': '中国',
    'EN': {
        'London': '伦敦',
        'Edinburgh': '爱丁堡'
    },
    'JP': {
        'Tokyo': '东京',
        'Kyoto': '京都'
    },
    'FR': {
        'Paris': '巴黎',
        'Lyon': '里昂'
    },
    'DE': {
        'Berlin': '柏林',
        'Munich': '慕尼黑'
    }
}

# 故事类型
STORY_TYPES = {
    'fairy_tale': '童话',
    'legend': '传说',
    'myth': '神话',
    'folk_tale': '民间故事'
}

# 故事分类
STORY_CATEGORIES = {
    'traditional': '传统',
    'modern': '现代',
    'festival': '节日'
}

# 故事收集设置
RETRY_COUNT = 3           # 收集失败时的重试次数
BATCH_SIZE = 5            # 每批处理的故事数量
SIMILARITY_THRESHOLD = 0.85  # 故事相似度阈值，超过则视为重复

# 保存设置
BACKUP_COUNT = 3          # 备份文件保留数量
USE_ATOMIC_WRITE = True   # 使用原子写入操作

# 数据库配置
DATABASE = {
    'path': 'data/database/stories.db'
}

# 文件存储配置
STORAGE = {
    'base_path': 'data/stories',
    'file_extension': '.md'
} 