#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
集成测试模块
测试整个故事收集系统的工作流程
"""

import os
import sys
import shutil
import tempfile
import unittest

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collector import StoryCollector
from src.validator import validate_story
from utils.formatter import format_story
from utils.fingerprint import generate_fingerprint, is_duplicate

class TestIntegration(unittest.TestCase):
    """集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录作为测试数据目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 修改配置
        import config.settings
        self.original_stories_dir = config.settings.STORIES_DIR
        self.original_state_file = config.settings.STATE_FILE
        
        config.settings.STORIES_DIR = os.path.join(self.temp_dir, 'stories')
        config.settings.STATE_FILE = os.path.join(self.temp_dir, 'state.json')
        
        # 创建必要的目录
        os.makedirs(config.settings.STORIES_DIR, exist_ok=True)
        
        # 初始化收集器
        self.collector = StoryCollector()
    
    def tearDown(self):
        """测试后清理"""
        # 恢复原始配置
        import config.settings
        config.settings.STORIES_DIR = self.original_stories_dir
        config.settings.STATE_FILE = self.original_state_file
        
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 准备测试数据
        test_story = """
# CN003 测试集成故事 (Integration Test Story)

## 基本信息
- 故事编号: CN003
- 分类: 传统民间故事
- 子分类: 测试地区
- 地区: 测试地区
- 类型: 童话故事

## 故事来源
这是一个用于集成测试的故事。

## 故事梗概
从前有一个小村庄，村里住着一个善良的老爷爷。他每天都会给村里的孩子们讲故事。
有一天，他讲了一个关于诚信的故事，告诉孩子们诚实守信的重要性。
孩子们听完故事后，都决定要做一个诚实的好孩子。

## 文化背景
1. 传统村落文化：
   - 社区关爱
   - 长幼有序
   - 邻里互助
   - 共同教育

## 故事主题
1. 主要人物：
   - 老爷爷：慈祥、智慧
   - 村里的孩子们：天真、求知

2. 核心价值观：
   - 诚信为本
   - 尊老爱幼
   - 团结互助
   - 知识传承

## 收集记录
- 收集时间: 2023-03
- 收集人: 自动测试
- 完整性: 测试
        """
        
        # 1. 测试验证功能
        is_valid, issues, fixed_content = validate_story({
            'title': '测试集成故事',
            'language_code': 'CN',
            'region': '测试地区',
            'category': 'traditional',
            'type': 'fairy_tale'
        }, test_story)
        
        # 应该有一些问题，因为内容不完整
        self.assertFalse(is_valid, "不完整的故事应该验证失败")
        self.assertTrue(len(issues) > 0, "应该检测到内容问题")
        
        # 2. 测试指纹生成和重复检测
        story_data = {
            'title': '测试集成故事',
            'region': '测试地区',
            'type': 'fairy_tale',
            'story_content': test_story
        }
        
        fingerprint = generate_fingerprint(story_data)
        self.assertTrue(len(fingerprint) > 0, "应该生成有效的指纹")
        
        # 3. 测试故事收集和保存
        # 模拟模型调用返回测试故事
        self.collector._simulate_model_call = lambda x: test_story
        
        # 收集故事
        success, metadata, content = self.collector.collect_story(
            'CN', '测试地区', 'traditional', 'fairy_tale'
        )
        
        self.assertTrue(success, "故事收集应该成功")
        
        # 保存故事
        save_success, filepath = self.collector.save_collected_story(metadata, content)
        
        self.assertTrue(save_success, "故事保存应该成功")
        self.assertTrue(os.path.exists(filepath), "应该生成故事文件")
        
        # 4. 测试重复检测
        # 再次尝试收集相同故事
        success, metadata, content = self.collector.collect_story(
            'CN', '测试地区', 'traditional', 'fairy_tale'
        )
        
        self.assertFalse(success, "重复故事应该被检测出来")
        
        # 5. 测试统计信息
        stats = self.collector.get_collection_stats()
        
        self.assertEqual(stats['collected_count'], 1, "应该收集了1个故事")
        self.assertEqual(stats['skipped_count'], 1, "应该跳过了1个重复故事")
        self.assertEqual(stats['total_existing'], 1, "系统中应该有1个故事")
        self.assertEqual(stats['total_fingerprints'], 1, "应该有1个指纹")

if __name__ == '__main__':
    unittest.main() 