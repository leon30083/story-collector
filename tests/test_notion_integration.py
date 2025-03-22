"""
Test script for Notion integration
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.integration.notion_integration import NotionIntegration

def test_notion_connection():
    """测试 Notion 连接"""
    print("开始测试 Notion 集成...")
    
    # 初始化 Notion 集成
    notion = NotionIntegration()
    
    # 测试查询
    print("\n1. 测试查询所有故事...")
    stories = notion.query_stories()
    print(f"找到 {len(stories)} 个故事")
    
    # 测试过滤查询
    print("\n2. 测试过滤查询...")
    filter_params = {
        "property": "语言",
        "select": {
            "equals": "中文"
        }
    }
    filtered_stories = notion.query_stories(filter_params)
    print(f"找到 {len(filtered_stories)} 个中文故事")
    
    # 测试创建故事
    print("\n3. 测试创建新故事...")
    test_story = {
        "title": "测试故事",
        "language": "中文",
        "region": "中国",
        "type": "童话",
        "content": "这是一个测试故事的内容。",
        "moral": "这是一个测试故事的寓意。",
        "created_time": datetime.now().isoformat(),
        "story_id": "TEST001"
    }
    
    response = notion.create_story(test_story)
    if response:
        print(f"成功创建故事页面，ID: {response.get('id')}")
        
        # 测试更新故事
        print("\n4. 测试更新故事...")
        test_story["content"] = "这是更新后的测试故事内容。"
        if notion.update_story(response["id"], test_story):
            print("成功更新故事内容")
        else:
            print("更新故事失败")
    else:
        print("创建故事失败")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_notion_connection() 