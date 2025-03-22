from typing import Dict, Tuple, Optional
import random
import time
import os
import json

class StoryCollector:
    def __init__(self):
        """初始化故事收集器"""
        self.collected_stories = []
        self.id_counter_file = os.path.join('data', 'id_counter.json')
        self._load_id_counter()
    
    def _load_id_counter(self):
        """加载ID计数器"""
        try:
            if os.path.exists(self.id_counter_file):
                with open(self.id_counter_file, 'r') as f:
                    self.id_counters = json.load(f)
            else:
                self.id_counters = {}
        except Exception:
            self.id_counters = {}
    
    def _save_id_counter(self):
        """保存ID计数器"""
        os.makedirs(os.path.dirname(self.id_counter_file), exist_ok=True)
        with open(self.id_counter_file, 'w') as f:
            json.dump(self.id_counters, f)
    
    def _generate_story_id(self, language: str) -> str:
        """生成故事ID"""
        if language not in self.id_counters:
            self.id_counters[language] = 0
        
        self.id_counters[language] += 1
        story_id = f"{language}{self.id_counters[language]:03d}"
        
        self._save_id_counter()
        return story_id
    
    def collect_story(self, language: str, region: str, category: str, story_type: str) -> Tuple[bool, Optional[Dict], str]:
        """收集故事
        
        Args:
            language: 语言代码
            region: 地区
            category: 分类
            story_type: 类型
        
        Returns:
            Tuple[bool, Optional[Dict], str]: (是否成功, 元数据, 内容)
        """
        # 模拟故事收集过程
        time.sleep(1)  # 模拟网络延迟
        
        # 生成示例故事
        story_id = self._generate_story_id(language)
        title = self._generate_title(language, region, story_type)
        content = self._generate_content(title, region, story_type)
        
        metadata = {
            'id': story_id,
            'title': title,
            'language': language,
            'region': region,
            'category': category,
            'type': story_type,
            'collected_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.collected_stories.append(metadata)
        return True, metadata, content
    
    def _generate_title(self, language: str, region: str, story_type: str) -> str:
        """生成故事标题"""
        themes = ['月亮', '太阳', '星星', '山', '海', '河流', '森林', '花园']
        characters = ['小兔子', '小狐狸', '小猫', '小狗', '小鸟', '蝴蝶', '小鱼']
        actions = ['的冒险', '的梦想', '的旅行', '的故事', '的秘密', '的智慧']
        
        theme = random.choice(themes)
        character = random.choice(characters)
        action = random.choice(actions)
        
        return f"{theme}里{character}{action}"
    
    def _generate_content(self, title: str, region: str, story_type: str) -> str:
        """生成故事内容"""
        return f"""# {title}

## 故事简介
这是一个来自{region}的{story_type}。

## 故事内容
从前，在一个美丽的地方，住着一群快乐的小动物...
[故事内容待完善]

## 故事寓意
友善、勇敢、智慧、合作的重要性。

## 创作时间
{time.strftime('%Y-%m-%d %H:%M:%S')}
""" 