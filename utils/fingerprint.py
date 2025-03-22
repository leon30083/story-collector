"""
故事指纹生成工具
用于生成故事的唯一标识，用于去重
"""

import hashlib
import re
import json
from difflib import SequenceMatcher

def generate_fingerprint(story_data):
    """
    生成故事的指纹
    
    Args:
        story_data: 故事数据字典
        
    Returns:
        fingerprint: 故事指纹(MD5哈希值)
    """
    # 提取关键信息
    title = story_data.get('title', '')
    region = story_data.get('region', '')
    story_type = story_data.get('type', '')
    
    # 处理故事内容，提取关键段落
    content = story_data.get('story_content', '')
    
    # 生成指纹基础字符串
    fingerprint_base = f"{title}|{region}|{story_type}|{_extract_content_signature(content)}"
    
    # 生成MD5哈希
    return hashlib.md5(fingerprint_base.encode('utf-8')).hexdigest()

def _extract_content_signature(content):
    """
    从故事内容中提取特征签名
    
    Args:
        content: 故事内容文本
        
    Returns:
        signature: 内容特征签名
    """
    if not content:
        return ""
    
    # 清理文本
    clean_content = _clean_text(content)
    
    # 提取前100个单词和后100个单词
    words = clean_content.split()
    if len(words) <= 200:
        return clean_content
    
    start = ' '.join(words[:100])
    end = ' '.join(words[-100:])
    
    return f"{start}...{end}"

def _clean_text(text):
    """
    清理文本，移除特殊字符、多余空格等
    
    Args:
        text: 原始文本
        
    Returns:
        cleaned_text: 清理后的文本
    """
    if not text:
        return ""
    
    # 移除Markdown标记
    text = re.sub(r'#.*?\n', ' ', text)
    text = re.sub(r'\*\*|\*|__|\||_|`', '', text)
    
    # 移除多余空白字符
    text = re.sub(r'\s+', ' ', text)
    
    # 移除标点符号
    text = re.sub(r'[^\w\s]', '', text)
    
    return text.strip().lower()

def calculate_similarity(text1, text2):
    """
    计算两段文本的相似度
    
    Args:
        text1: 第一段文本
        text2: 第二段文本
        
    Returns:
        similarity: 相似度(0-1)
    """
    # 清理文本
    clean_text1 = _clean_text(text1)
    clean_text2 = _clean_text(text2)
    
    # 使用SequenceMatcher计算相似度
    return SequenceMatcher(None, clean_text1, clean_text2).ratio()

def load_fingerprints(filepath):
    """
    从文件加载指纹
    
    Args:
        filepath: 指纹文件路径
        
    Returns:
        fingerprints: 已存在的指纹字典
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_fingerprints(fingerprints, filepath):
    """
    保存指纹到文件
    
    Args:
        fingerprints: 指纹字典
        filepath: 保存路径
        
    Returns:
        success: 是否保存成功
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(fingerprints, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def is_duplicate(story_data, existing_fingerprints, similarity_threshold=0.85):
    """
    检查故事是否是重复的
    
    Args:
        story_data: 故事数据
        existing_fingerprints: 已存在的指纹字典
        similarity_threshold: 相似度阈值
        
    Returns:
        is_duplicate: 是否重复
    """
    # 生成当前故事的指纹
    fingerprint = generate_fingerprint(story_data)
    
    # 检查指纹是否已存在
    if fingerprint in existing_fingerprints:
        return True
    
    # 检查内容相似度
    story_content = story_data.get('story_content', '')
    story_language = story_data.get('language_code', '')
    story_region = story_data.get('region', '')
    
    for fp, data in existing_fingerprints.items():
        # 如果是不同语言或地区的故事，提高相似度阈值（更严格的判断）
        check_threshold = similarity_threshold
        
        # 如果保存的数据中有语言代码和地区信息
        data_language = data.get('language_code', '')
        data_region = data.get('region', '')
        
        # 如果语言不同，则需要更高的相似度才判定为重复
        if data_language and story_language and data_language != story_language:
            check_threshold = 0.95  # 非常高的阈值
            continue  # 不同语言的故事直接跳过比较
        
        # 如果地区不同，也提高相似度要求
        if data_region and story_region and data_region != story_region:
            check_threshold = 0.90
        
        # 标题完全相同的情况
        if 'title' in story_data and story_data['title'] == data.get('title', ''):
            # 如果语言和地区都相同，则认为是重复
            if (not data_language or not story_language or data_language == story_language) and \
               (not data_region or not story_region or data_region == story_region):
                return True
        
        # 检查内容相似度
        existing_content = data.get('story_content', '')
        if existing_content and calculate_similarity(story_content, existing_content) > check_threshold:
            return True
    
    return False 