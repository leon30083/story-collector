"""
Notion integration configuration

使用说明：
1. 将你的 Notion API 密钥替换 NOTION_API_KEY
2. 将你的数据库 ID 替换 NOTION_DATABASE_ID
   - 数据库 ID 可以从数据库页面的 URL 中获取
   - URL 格式：https://www.notion.so/workspace/1234567890abcdef1234567890abcdef?v=...
   - 数据库 ID 就是 URL 中 "?" 前面的部分
3. 确保数据库属性名称与 properties 中的映射一致
"""

# Notion API Configuration
NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "1bd6929012f680f38e81fead620f5b9f"

# Property Mappings
PROPERTY_MAPPINGS = {
    "标题": "title",
    "故事分类": "select",
    "故事内容": "rich_text",
    "语言": "select",
    "创建时间": "created_time",
    "地区": "rich_text",
    "故事ID": "rich_text"
}

# Story Type Options (故事分类选项)
STORY_TYPE_OPTIONS = {
    "成语故事": "成语故事",     # 成语典故和历史故事
    "寓言故事": "寓言故事",     # 蕴含哲理的短小故事
    "经典童话": "经典童话",     # 具有想象力的儿童故事
    "神话故事": "神话故事",     # 古代神话和传说
    "民间故事": "民间故事",     # 民间流传的故事
    "其他": "其他"             # 其他类型
}

# Language Options (语言选项)
LANGUAGE_OPTIONS = {
    "中文": "中文",
    "英文": "英文",
    "日文": "日文",
    "法文": "法文",
    "德文": "德文",
    "其他": "其他"
}

# Default Values
DEFAULT_VALUES = {
    "创建时间": "last_edited_time"
}

# Database Mapping
NOTION_DATABASE_MAPPING = {
    "stories": {
        "database_id": "1bd6929012f680f38e81fead620f5b9f",  # 数据库 ID
        "properties": {
            "title": "标题",
            "language": "语言",
            "region": "地区",
            "type": "故事分类",
            "content": "故事内容",
            "created_time": "创建时间",
            "story_id": "故事ID"
        }
    }
}

# Sync Settings
SYNC_SETTINGS = {
    "auto_sync": True,      # 是否自动同步到 Notion
    "sync_interval": 300,   # 同步间隔（秒）
    "batch_size": 50        # 批量同步数量
}

# Error Handling
ERROR_HANDLING = {
    "retry_count": 3,       # 重试次数
    "retry_delay": 5,       # 重试延迟（秒）
    "log_errors": True      # 是否记录错误
} 