import sqlite3
from typing import Dict, List, Optional
import json
from pathlib import Path

class StoryDatabase:
    def __init__(self, db_path: str = "data/database/stories.db"):
        """初始化故事数据库
        
        Args:
            db_path: 数据库文件路径
        """
        # 确保数据库目录存在
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建故事表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    language TEXT NOT NULL,
                    region TEXT NOT NULL,
                    type TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_language ON stories(language)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_region ON stories(region)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON stories(type)')
            
            conn.commit()
    
    def add_story(self, story_info: Dict[str, str]) -> bool:
        """添加新故事到数据库
        
        Args:
            story_info: 故事信息字典
                - id: 故事ID
                - title: 标题
                - language: 语言
                - region: 地区
                - type: 类型
                - summary: 简介
                - file_path: 文件路径
                - metadata: 额外元数据(可选)
        
        Returns:
            bool: 是否添加成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 处理可选的元数据
                metadata = json.dumps(story_info.get('metadata', {}))
                
                cursor.execute('''
                    INSERT INTO stories 
                    (id, title, language, region, type, summary, file_path, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    story_info['id'],
                    story_info['title'],
                    story_info['language'],
                    story_info['region'],
                    story_info['type'],
                    story_info['summary'],
                    story_info['file_path'],
                    metadata
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding story to database: {e}")
            return False
    
    def get_story(self, story_id: str) -> Optional[Dict[str, str]]:
        """获取故事信息
        
        Args:
            story_id: 故事ID
        
        Returns:
            Dict[str, str]: 故事信息字典，如果不存在返回None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM stories WHERE id = ?', (story_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                story_info = dict(zip(columns, row))
                story_info['metadata'] = json.loads(story_info['metadata'])
                return story_info
            
            return None
    
    def search_stories(self, 
                      language: Optional[str] = None,
                      region: Optional[str] = None,
                      story_type: Optional[str] = None) -> List[Dict[str, str]]:
        """搜索故事
        
        Args:
            language: 语言过滤
            region: 地区过滤
            story_type: 类型过滤
        
        Returns:
            List[Dict[str, str]]: 符合条件的故事列表
        """
        query = 'SELECT * FROM stories WHERE 1=1'
        params = []
        
        if language:
            query += ' AND language = ?'
            params.append(language)
        
        if region:
            query += ' AND region = ?'
            params.append(region)
        
        if story_type:
            query += ' AND type = ?'
            params.append(story_type)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            columns = [description[0] for description in cursor.description]
            stories = []
            
            for row in cursor.fetchall():
                story_info = dict(zip(columns, row))
                story_info['metadata'] = json.loads(story_info['metadata'])
                stories.append(story_info)
            
            return stories
    
    def get_story_count(self) -> Dict[str, int]:
        """获取故事统计信息
        
        Returns:
            Dict[str, int]: 包含各种统计数据的字典
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {
                'total': cursor.execute('SELECT COUNT(*) FROM stories').fetchone()[0],
                'by_language': {},
                'by_type': {},
                'by_region': {}
            }
            
            # 按语言统计
            cursor.execute('SELECT language, COUNT(*) FROM stories GROUP BY language')
            stats['by_language'] = dict(cursor.fetchall())
            
            # 按类型统计
            cursor.execute('SELECT type, COUNT(*) FROM stories GROUP BY type')
            stats['by_type'] = dict(cursor.fetchall())
            
            # 按地区统计
            cursor.execute('SELECT region, COUNT(*) FROM stories GROUP BY region')
            stats['by_region'] = dict(cursor.fetchall())
            
            return stats
    
    def get_all_stories(self) -> List[Dict[str, str]]:
        """获取所有故事
        
        Returns:
            List[Dict[str, str]]: 所有故事的列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM stories')
            
            columns = [description[0] for description in cursor.description]
            stories = []
            
            for row in cursor.fetchall():
                story_info = dict(zip(columns, row))
                story_info['metadata'] = json.loads(story_info['metadata'])
                stories.append(story_info)
            
            return stories 