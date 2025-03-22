"""
故事验证模块
用于验证故事内容的格式和质量
"""

import sys
import os
import re

# 导入配置和工具
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger, log_operation
from utils.formatter import validate_story_format, fix_common_issues
from config.settings import STORY_LANGUAGES, STORY_TYPES, STORY_CATEGORIES

# 获取日志记录器
logger = get_logger('story_validator')

def validate_story(story_data, content):
    """
    验证故事数据和内容
    
    Args:
        story_data: 故事元数据
        content: 故事内容
        
    Returns:
        (is_valid, issues, fixed_content): 是否有效、问题列表、修复后的内容
    """
    issues = []
    
    # 验证元数据
    metadata_issues = validate_metadata(story_data)
    issues.extend(metadata_issues)
    
    # 验证内容格式
    is_valid_format, format_issues = validate_story_format(content)
    if not is_valid_format:
        issues.extend(format_issues)
        
    # 验证内容质量
    quality_issues = validate_content_quality(content)
    issues.extend(quality_issues)
    
    # 如果有问题，尝试修复
    fixed_content = content
    if issues:
        fixed_content = fix_common_issues(content)
        log_operation(logger, "修复故事格式", "成功" if fixed_content != content else "无需修复")
    
    return len(issues) == 0, issues, fixed_content

def validate_metadata(story_data):
    """
    验证故事元数据
    
    Args:
        story_data: 故事元数据
        
    Returns:
        issues: 问题列表
    """
    issues = []
    
    # 检查必须字段
    required_fields = ['title', 'language_code', 'region', 'category', 'type']
    for field in required_fields:
        if field not in story_data or not story_data[field]:
            issues.append(f"缺少必要字段: {field}")
    
    # 检查语言代码
    if 'language_code' in story_data and story_data['language_code'] not in STORY_LANGUAGES:
        issues.append(f"无效的语言代码: {story_data['language_code']}，有效的语言代码: {', '.join(STORY_LANGUAGES.keys())}")
    
    # 检查分类
    if 'category' in story_data and story_data['category'] not in STORY_CATEGORIES:
        issues.append(f"无效的故事分类: {story_data['category']}，有效的分类: {', '.join(STORY_CATEGORIES.keys())}")
    
    # 检查类型
    if 'type' in story_data and story_data['type'] not in STORY_TYPES:
        issues.append(f"无效的故事类型: {story_data['type']}，有效的类型: {', '.join(STORY_TYPES.keys())}")
    
    return issues

def validate_content_quality(content):
    """
    验证故事内容质量
    
    Args:
        content: 故事内容
        
    Returns:
        issues: 问题列表
    """
    issues = []
    
    # 检查内容长度
    if len(content) < 200:
        issues.append("故事内容过短，应该至少包含200个字符")
    
    # 检查是否包含故事梗概部分
    if not re.search(r'## 故事梗概', content, re.MULTILINE):
        issues.append("缺少故事梗概部分")
    else:
        # 提取故事梗概
        story_content_match = re.search(r'## 故事梗概\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if story_content_match:
            story_content = story_content_match.group(1).strip()
            
            # 检查梗概长度
            if len(story_content) < 100:
                issues.append("故事梗概过短，应该至少包含100个字符的详细描述")
                
            # 检查是否有段落
            if '\n\n' not in story_content and len(story_content) > 300:
                issues.append("故事梗概缺少适当的段落分隔")
    
    # 检查文化背景部分
    if '## 文化背景' in content:
        culture_match = re.search(r'## 文化背景\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if culture_match:
            culture_content = culture_match.group(1).strip()
            if len(culture_content) < 50:
                issues.append("文化背景部分内容不足")
    
    # 检查故事主题部分
    if '## 故事主题' in content:
        theme_match = re.search(r'## 故事主题\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if theme_match:
            theme_content = theme_match.group(1).strip()
            if len(theme_content) < 50:
                issues.append("故事主题部分内容不足")
    
    # 检查教育价值部分
    if '## 教育价值' in content:
        edu_match = re.search(r'## 教育价值\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if edu_match:
            edu_content = edu_match.group(1).strip()
            if len(edu_content) < 50:
                issues.append("教育价值部分内容不足")
    
    return issues

def extract_metadata_from_content(content):
    """
    从故事内容中提取元数据
    
    Args:
        content: 故事内容
        
    Returns:
        metadata: 提取的元数据
    """
    metadata = {}
    
    # 提取标题
    title_match = re.search(r'^# ([^\(]+)(?:\(([^\)]+)\))?', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
        if title_match.group(2):
            metadata['original_title'] = title_match.group(2).strip()
    
    # 提取基本信息
    basic_info_match = re.search(r'## 基本信息\s+(.*?)(?=##|\Z)', content, re.DOTALL)
    if basic_info_match:
        basic_info = basic_info_match.group(1).strip()
        
        # 提取故事编号
        story_number_match = re.search(r'- 故事编号:\s*([^\n]+)', basic_info)
        if story_number_match:
            full_number = story_number_match.group(1).strip()
            # 尝试提取语言代码
            if len(full_number) >= 2:
                metadata['language_code'] = full_number[:2]
                metadata['story_number'] = full_number[2:] if len(full_number) > 2 else ''
        
        # 提取分类
        category_match = re.search(r'- 分类:\s*([^\n]+)', basic_info)
        if category_match:
            metadata['category'] = _match_category(category_match.group(1).strip())
        
        # 提取子分类/地区
        region_match = re.search(r'- 子分类:\s*([^\n]+)', basic_info)
        if region_match:
            metadata['region'] = region_match.group(1).strip()
        
        # 提取故事类型
        type_match = re.search(r'- 类型:\s*([^\n]+)', basic_info)
        if type_match:
            metadata['type'] = _match_type(type_match.group(1).strip())
    
    return metadata

def _match_category(category_text):
    """
    匹配故事分类
    
    Args:
        category_text: 分类文本
        
    Returns:
        category_key: 匹配的分类键
    """
    # 直接匹配
    if category_text in STORY_CATEGORIES:
        return category_text
    
    # 尝试反向查找
    for key, value in STORY_CATEGORIES.items():
        if value in category_text:
            return key
    
    # 模糊匹配
    if '传统' in category_text:
        return 'traditional'
    elif '现代' in category_text:
        return 'modern'
    elif '节日' in category_text:
        return 'festival'
    
    return 'traditional'  # 默认为传统故事

def _match_type(type_text):
    """
    匹配故事类型
    
    Args:
        type_text: 类型文本
        
    Returns:
        type_key: 匹配的类型键
    """
    # 直接匹配
    if type_text in STORY_TYPES:
        return type_text
    
    # 尝试反向查找
    for key, value in STORY_TYPES.items():
        if value in type_text:
            return key
    
    # 模糊匹配
    if '神话' in type_text:
        return 'myth'
    elif '传说' in type_text:
        return 'legend'
    elif '童话' in type_text:
        return 'fairy_tale'
    elif '城市' in type_text:
        return 'urban'
    elif '科技' in type_text:
        return 'tech'
    elif '环保' in type_text:
        return 'eco'
    elif '节日' in type_text:
        return 'festival'
    elif '宗教' in type_text:
        return 'religious'
    
    return 'general'  # 默认为一般故事 