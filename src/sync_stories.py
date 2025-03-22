import os
import re
from integration.notion_integration import NotionIntegration

def extract_story_info(content, file_path):
    """从故事内容中提取信息"""
    try:
        # 提取标题
        title_match = re.search(r'#\s*(.*?)(?:\n|$)', content)
        title = title_match.group(1) if title_match else os.path.basename(file_path).replace('.md', '')
        
        # 提取故事ID
        story_id = os.path.basename(file_path).replace('.md', '')
        
        # 提取故事内容
        content_match = re.search(r'##\s*故事内容\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        story_content = content_match.group(1).strip() if content_match else ""
        
        return {
            "title": title,
            "story_id": story_id,
            "content": story_content,
            "type": "成语故事",
            "language": "中文",
            "region": "中国",
            "file_path": file_path
        }
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return None

def sync_stories_to_notion(directory):
    """同步指定目录下的所有故事到 Notion"""
    notion = NotionIntegration()
    success_count = 0
    fail_count = 0
    
    for file_name in os.listdir(directory):
        if file_name.endswith('.md'):
            try:
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                story_data = extract_story_info(content, file_path)
                if story_data and notion.sync_story(story_data):
                    print(f"成功同步故事: {story_data['title']}")
                    success_count += 1
                else:
                    print(f"同步故事失败: {file_name}")
                    fail_count += 1
            except Exception as e:
                print(f"处理文件 {file_name} 时出错: {str(e)}")
                fail_count += 1
    
    return success_count, fail_count

if __name__ == "__main__":
    directory = "data/stories/CN/中国/idiom"
    success, fail = sync_stories_to_notion(directory)
    print(f"\n同步完成：成功 {success} 个，失败 {fail} 个") 