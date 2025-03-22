"""
Notion integration module for story collection system
"""

import os
import sys
import time
from typing import Dict, List, Optional
from datetime import datetime
import requests
from notion_client import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.notion_config import (
    NOTION_API_KEY,
    NOTION_DATABASE_ID,
    PROPERTY_MAPPINGS,
    STORY_TYPE_OPTIONS,
    LANGUAGE_OPTIONS,
    DEFAULT_VALUES,
    SYNC_SETTINGS,
    ERROR_HANDLING
)

from utils.logger import get_logger

logger = get_logger(__name__)

class NotionIntegration:
    """Notion integration handler"""
    
    def __init__(self):
        self.client = Client(auth=NOTION_API_KEY)
        self.database_id = NOTION_DATABASE_ID
        self.retry_count = ERROR_HANDLING['retry_count']
        self.retry_delay = ERROR_HANDLING['retry_delay']

    def sync_story(self, story_data: Dict) -> bool:
        """同步故事到 Notion"""
        try:
            # 检查故事是否已存在
            existing_stories = self.query_stories({
                "property": "故事ID",
                "rich_text": {
                    "equals": story_data.get("story_id", "")
                }
            })
            
            if existing_stories:
                # 更新现有故事
                page_id = existing_stories[0]["id"]
                response = self.update_story(page_id, story_data)
                if response is None:
                    logger.error(f"更新故事失败")
                    return False
                    
                logger.info(f"更新故事成功: {story_data.get('title', '')}")
            else:
                # 创建新故事
                response = self.create_story(story_data)
                if response is None:
                    logger.error(f"创建故事失败")
                    return False
                    
                logger.info(f"创建故事成功: {story_data.get('title', '')}")
            
            return True
            
        except Exception as e:
            logger.error(f"同步故事失败: {str(e)}")
            return False

    def query_stories(self, filter_params: Dict = None) -> List[Dict]:
        """查询故事"""
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter=filter_params
            )
            
            if response is None:
                logger.error(f"查询故事失败")
                return []
            
            return response.get("results", [])
            
        except Exception as e:
            logger.error(f"查询故事失败: {str(e)}")
            return []

    def _format_story_properties(self, story: Dict) -> Dict:
        """Format story data according to Notion property types"""
        # 确保故事内容不超过2000字
        content = story.get("content", "")
        if len(content) > 2000:
            content = content[:1997] + "..."

        properties = {
            "标题": {"title": [{"text": {"content": story.get("title", "")}}]},
            "故事分类": {"select": {"name": story.get("type", "成语故事")}},
            "故事内容": {"rich_text": [{"text": {"content": content}}]},
            "地区": {"rich_text": [{"text": {"content": story.get("region", "中国")}}]},
            "语言": {"select": {"name": story.get("language", "中文")}},
            "故事ID": {"rich_text": [{"text": {"content": story.get("story_id", "")}}]},
            "创建时间": {"date": {"start": datetime.now().isoformat()}}
        }
        return properties

    def create_story(self, story_data):
        """Create a new story in Notion database"""
        try:
            properties = self._format_story_properties(story_data)
            # 创建页面
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            # 如果有文件路径，上传文件
            if story_data.get("file_path"):
                self.upload_file(response["id"], story_data["file_path"])
            
            return response
        except Exception as e:
            logger.error(f"Error creating story in Notion: {e}")
            return None

    def update_story(self, page_id, story_data):
        """Update an existing story in Notion"""
        try:
            properties = self._format_story_properties(story_data)
            # 更新页面
            response = self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            
            # 如果有文件路径，上传文件
            if story_data.get("file_path"):
                self.upload_file(page_id, story_data["file_path"])
            
            return response
        except Exception as e:
            logger.error(f"Error updating story in Notion: {e}")
            return None

    def upload_file(self, page_id: str, file_path: str):
        """Upload a file to a Notion page as a code block"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # 获取文件名
            file_name = os.path.basename(file_path)
            
            # 添加文件名和内容作为代码块
            response = self.client.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"text": {"content": f"原始文件: {file_name}"}}]
                        }
                    },
                    {
                        "type": "code",
                        "code": {
                            "language": "markdown",
                            "rich_text": [{"text": {"content": file_content}}]
                        }
                    }
                ]
            )
            
            logger.info(f"文件 {file_name} 内容添加成功")
            return response
        except Exception as e:
            logger.error(f"添加文件内容失败: {str(e)}")
            return None

    def get_story_by_id(self, story_id):
        """Get story by ID"""
        filter_params = {
            "property": "故事ID",
            "rich_text": {
                "equals": story_id
            }
        }
        return self.query_stories(filter_params) 