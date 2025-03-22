#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试故事收集模块
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collector import StoryCollector
from utils.fingerprint import generate_fingerprint

class TestStoryCollector(unittest.TestCase):
    """测试故事收集器类"""
    
    def setUp(self):
        """测试前准备"""
        # 模拟初始化，跳过真实的加载过程
        with patch('src.collector.StoryCollector._load_existing_data'):
            self.collector = StoryCollector()
            self.collector.existing_stories = []
            self.collector.fingerprints = {}
    
    def test_is_duplicate_story(self):
        """测试故事重复检测"""
        # 添加一个已存在的故事指纹
        mock_story_data = {
            'title': '测试故事',
            'region': '测试地区',
            'type': 'fairy_tale',
            'story_content': '这是一个测试故事的内容。'
        }
        
        fingerprint = generate_fingerprint(mock_story_data)
        self.collector.fingerprints[fingerprint] = {
            'title': mock_story_data['title'],
            'filepath': '/path/to/story.md',
            'story_content': mock_story_data['story_content']
        }
        
        # 测试完全相同的故事
        result = self.collector._is_duplicate_story(mock_story_data, mock_story_data['story_content'])
        self.assertTrue(result, "应该检测为重复故事")
        
        # 测试不同的故事
        different_story = {
            'title': '另一个故事',
            'region': '另一个地区',
            'type': 'legend',
            'story_content': '这是一个完全不同的故事内容。'
        }
        
        result = self.collector._is_duplicate_story(different_story, different_story['story_content'])
        self.assertFalse(result, "不应该检测为重复故事")
    
    @patch('src.collector.StoryCollector._simulate_model_call')
    def test_collect_story(self, mock_simulate):
        """测试故事收集流程"""
        # 模拟模型返回的故事内容
        mock_content = """
# CN002 测试故事 (Test Story)

## 基本信息
- 故事编号: CN002
- 分类: 传统民间故事
- 子分类: 测试地区
- 地区: 测试地区
- 类型: 童话故事

## 故事来源
这是一个测试故事。

## 故事梗概
这是测试故事的内容。
        """
        
        mock_simulate.return_value = mock_content
        
        # 模拟验证和格式化
        with patch('src.collector.validate_story') as mock_validate:
            mock_validate.return_value = (True, [], mock_content)
            
            with patch('src.collector.format_story') as mock_format:
                mock_format.return_value = mock_content
                
                # 测试收集故事
                success, metadata, content = self.collector.collect_story(
                    'CN', '测试地区', 'traditional', 'fairy_tale'
                )
                
                self.assertTrue(success, "故事收集应该成功")
                self.assertEqual(metadata['title'], '测试故事', "故事标题应该正确提取")
                self.assertEqual(content, mock_content, "故事内容应该正确返回")
    
    @patch('src.collector.save_story')
    def test_save_collected_story(self, mock_save):
        """测试保存收集的故事"""
        # 模拟保存函数
        mock_save.return_value = (True, '/path/to/story.md')
        
        # 准备测试数据
        metadata = {
            'title': '测试故事',
            'language_code': 'CN',
            'region': '测试地区',
            'category': 'traditional',
            'type': 'fairy_tale'
        }
        
        content = "# CN002 测试故事\n\n## 故事梗概\n这是测试内容。"
        
        # 测试保存故事
        success, filepath = self.collector.save_collected_story(metadata, content)
        
        self.assertTrue(success, "故事保存应该成功")
        self.assertEqual(filepath, '/path/to/story.md', "应该返回正确的文件路径")
        self.assertEqual(len(self.collector.fingerprints), 1, "应该添加新的指纹")
        self.assertEqual(len(self.collector.existing_stories), 1, "应该添加新的故事记录")

if __name__ == '__main__':
    unittest.main() 