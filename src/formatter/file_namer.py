import re
from typing import Dict

class FileNamer:
    def __init__(self):
        self.language_prefix_map = {
            'CN': '中文',
            'EN': '英文',
            'JP': '日文',
            'FR': '法文',
            'DE': '德文'
        }
        
        self.type_map = {
            'fairy_tale': '童话',
            'legend': '传说',
            'myth': '神话',
            'folk_tale': '民间故事'
        }

    def generate_filename(self, story_info: Dict[str, str]) -> str:
        """生成故事文件名
        
        Args:
            story_info: 包含故事信息的字典
                - language: 语言代码
                - story_id: 故事ID
                - title: 故事标题
                - type: 故事类型
        
        Returns:
            str: 格式化的文件名
        """
        # 获取语言前缀
        lang_prefix = self.language_prefix_map.get(story_info['language'], story_info['language'])
        
        # 获取故事类型
        story_type = self.type_map.get(story_info['type'], story_info['type'])
        
        # 清理标题中的特殊字符
        clean_title = re.sub(r'[\\/:*?"<>|]', '_', story_info['title'])
        
        # 生成文件名格式：语言_类型_ID_标题.md
        filename = f"{lang_prefix}_{story_type}_{story_info['story_id']}_{clean_title}.md"
        
        return filename 