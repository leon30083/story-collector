"""
MCP Notion integration module for story collection system
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.logger import get_logger

logger = get_logger(__name__)

class MCPNotionIntegration:
    """MCP Notion integration handler"""
    
    def __init__(self):
        self.base_url = "http://localhost:3000"  # MCP 服务默认地址
        self.api_token = "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"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

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
            url = f"{self.base_url}/query"
            payload = {"filter": filter_params} if filter_params else {}
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json().get("results", [])
            
        except Exception as e:
            logger.error(f"查询故事失败: {str(e)}")
            return []

    def create_story(self, story_data: Dict) -> Optional[Dict]:
        """创建新故事"""
        try:
            url = f"{self.base_url}/create"
            payload = self._format_story_properties(story_data)
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"创建故事失败: {str(e)}")
            return None

    def update_story(self, page_id: str, story_data: Dict) -> Optional[Dict]:
        """更新故事"""
        try:
            url = f"{self.base_url}/update/{page_id}"
            payload = self._format_story_properties(story_data)
            
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"更新故事失败: {str(e)}")
            return None

    def _format_story_properties(self, story: Dict) -> Dict:
        """格式化故事属性"""
        properties = {
            "标题": {"title": [{"text": {"content": story.get("title", "")}}]},
            "故事分类": {"select": {"name": story.get("type", "成语故事")}},
            "故事内容": {"rich_text": [{"text": {"content": story.get("content", "")}}]},
            "地区": {"rich_text": [{"text": {"content": story.get("region", "中国")}}]},
            "语言": {"select": {"name": story.get("language", "中文")}},
            "故事ID": {"rich_text": [{"text": {"content": story.get("story_id", "")}}]},
            "创建时间": {"date": {"start": datetime.now().isoformat()}}
        }
        return properties 