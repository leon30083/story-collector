"""
格式化工具
用于处理故事格式，确保符合模板规范
"""

import re
import os
import sys
from datetime import datetime

# 导入配置
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import TEMPLATE_FILE

def read_template():
    """
    读取故事模板
    
    Returns:
        template: 模板内容
    """
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def extract_sections(content):
    """
    从故事内容中提取各个部分
    
    Args:
        content: 故事Markdown内容
        
    Returns:
        sections: 故事各部分的字典
    """
    sections = {}
    
    # 提取标题
    title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    if title_match:
        sections['title'] = title_match.group(1).strip()
    
    # 提取基本信息
    basic_info_pattern = r'## 基本信息\s+(.+?)(?=##|\Z)'
    basic_info_match = re.search(basic_info_pattern, content, re.DOTALL)
    if basic_info_match:
        basic_info = basic_info_match.group(1).strip()
        # 提取具体项目
        for line in basic_info.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                parts = line[1:].split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(' ', '_')
                    value = parts[1].strip()
                    sections[key] = value
    
    # 提取其他主要部分
    sections_pattern = r'## ([^\n]+)\s+(.*?)(?=## |$)'
    for section_match in re.finditer(sections_pattern, content, re.DOTALL):
        section_name = section_match.group(1).strip().lower().replace(' ', '_')
        section_content = section_match.group(2).strip()
        sections[section_name] = section_content
    
    return sections

def format_story(story_data):
    """
    将故事数据格式化为Markdown格式
    
    Args:
        story_data: 故事数据字典
        
    Returns:
        formatted_content: 格式化后的Markdown内容
    """
    template = read_template()
    
    # 如果没有模板，则创建基本内容
    if not template:
        return _create_basic_content(story_data)
    
    # 替换模板中的占位符
    formatted_content = template
    
    # 替换标题
    if 'title' in story_data:
        if 'original_title' in story_data:
            title_line = f"# {story_data['language_code']}{story_data.get('story_number', '001')} {story_data['title']} ({story_data['original_title']})"
        else:
            title_line = f"# {story_data['language_code']}{story_data.get('story_number', '001')} {story_data['title']}"
        formatted_content = re.sub(r'^# .*?$', title_line, formatted_content, flags=re.MULTILINE)
    
    # 替换基本信息
    if 'language_code' in story_data:
        formatted_content = re.sub(r'- 故事编号: \[语言代码\]\[编号\]', 
                                  f"- 故事编号: {story_data['language_code']}{story_data.get('story_number', '001')}", 
                                  formatted_content)
    
    if 'category' in story_data:
        formatted_content = re.sub(r'- 分类: \[传统民间故事/现代故事/节日故事等\]', 
                                  f"- 分类: {story_data['category']}", 
                                  formatted_content)
    
    if 'region' in story_data:
        formatted_content = re.sub(r'- 子分类: \[具体地区/文化圈分类\]', 
                                  f"- 子分类: {story_data['region']}", 
                                  formatted_content)
        formatted_content = re.sub(r'- 地区: \[具体城市/地区，所属国家\]', 
                                  f"- 地区: {story_data['region']}", 
                                  formatted_content)
    
    if 'type' in story_data:
        formatted_content = re.sub(r'- 类型: \[故事类型：神话/传说/童话等\]', 
                                  f"- 类型: {story_data['type']}", 
                                  formatted_content)
    
    # 替换故事内容
    if 'story_content' in story_data:
        # 提取故事梗概部分
        story_content = story_data['story_content']
        story_parts = {}
        
        # 尝试从story_content中提取各个部分
        parts = re.findall(r'## ([^\n]+)\s+(.*?)(?=##|\Z)', story_content, re.DOTALL)
        for part_name, part_content in parts:
            part_key = part_name.strip().lower()
            story_parts[part_key] = part_content.strip()
        
        # 替换故事来源
        if '故事来源' in story_parts:
            formatted_content = re.sub(r'## 故事来源\s+\[简要说明故事的文化背景和来源，100字以内\]',
                                     f"## 故事来源\n\n{story_parts['故事来源']}", 
                                     formatted_content)
        
        # 替换故事梗概
        if '故事梗概' in story_parts:
            formatted_content = re.sub(r'## 故事梗概\s+\[详细的故事情节，包括人物、事件发展和结局，1000字左右\]',
                                     f"## 故事梗概\n\n{story_parts['故事梗概']}", 
                                     formatted_content)
        
        # 替换其他部分
        for section in ['文化背景', '故事主题', '故事意义', '教育价值', '相关传统', '参考来源']:
            section_lower = section.lower()
            if section_lower in story_parts:
                pattern = f"## {section}\\s+.*?(?=##|\\Z)"
                replacement = f"## {section}\n\n{story_parts[section_lower]}"
                formatted_content = re.sub(pattern, replacement, formatted_content, flags=re.DOTALL)
    
    # 添加收集记录
    now = datetime.now().strftime('%Y-%m')
    collector = story_data.get('collector', '自动收集')
    formatted_content = re.sub(r'- 收集时间: \[年月\]', f'- 收集时间: {now}', formatted_content)
    formatted_content = re.sub(r'- 收集人: \[收集者\]', f'- 收集人: {collector}', formatted_content)
    formatted_content = re.sub(r'- 完整性: \[完整性评估\]', f'- 完整性: {story_data.get("completeness", "完整")}', formatted_content)
    
    return formatted_content

def _create_basic_content(story_data):
    """
    创建基本的故事内容
    
    Args:
        story_data: 故事数据
        
    Returns:
        content: 创建的内容
    """
    content = []
    
    # 添加标题
    if 'title' in story_data:
        if 'original_title' in story_data:
            content.append(f"# {story_data['title']} ({story_data['original_title']})")
        else:
            content.append(f"# {story_data['title']}")
    else:
        content.append("# 未命名故事")
    
    content.append("")
    
    # 添加基本信息
    content.append("## 基本信息")
    for key, value in story_data.items():
        if key not in ['title', 'original_title', 'story_content']:
            content.append(f"- {key.replace('_', ' ').title()}: {value}")
    
    content.append("")
    
    # 添加故事内容
    if 'story_content' in story_data:
        content.append("## 故事梗概")
        content.append(story_data['story_content'])
    
    content.append("")
    
    # 添加收集记录
    content.append("## 收集记录")
    content.append(f"- 收集时间: {datetime.now().strftime('%Y-%m')}")
    content.append(f"- 收集人: {story_data.get('collector', '自动收集')}")
    content.append(f"- 完整性: {story_data.get('completeness', '部分')}")
    
    return "\n".join(content)

def validate_story_format(content):
    """
    验证故事格式是否符合要求
    
    Args:
        content: 故事内容
        
    Returns:
        (is_valid, issues): 是否有效和问题列表
    """
    issues = []
    
    # 检查标题
    if not re.search(r'^# ', content, re.MULTILINE):
        issues.append("缺少标题(# 开头)")
    
    # 检查基本信息
    if not re.search(r'## 基本信息', content, re.MULTILINE):
        issues.append("缺少基本信息部分")
    
    # 检查故事梗概
    if not re.search(r'## 故事梗概', content, re.MULTILINE):
        issues.append("缺少故事梗概部分")
    
    # 检查收集记录
    if not re.search(r'## 收集记录', content, re.MULTILINE):
        issues.append("缺少收集记录部分")
    
    return len(issues) == 0, issues

def fix_common_issues(content):
    """
    修复常见的格式问题
    
    Args:
        content: 原始内容
        
    Returns:
        fixed_content: 修复后的内容
    """
    fixed_content = content
    
    # 修复标题格式
    if not re.search(r'^# ', fixed_content, re.MULTILINE):
        title_match = re.search(r'^(.+?)$', fixed_content.strip(), re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            fixed_content = re.sub(r'^.+?$', f'# {title}', fixed_content.strip(), count=1, flags=re.MULTILINE)
        else:
            fixed_content = f"# 未命名故事\n\n{fixed_content}"
    
    # 修复基本信息部分
    if not re.search(r'## 基本信息', fixed_content, re.MULTILINE):
        fixed_content += "\n\n## 基本信息\n- 故事编号: 未编号\n- 分类: 未分类\n"
    
    # 修复故事梗概部分
    if not re.search(r'## 故事梗概', fixed_content, re.MULTILINE):
        fixed_content += "\n\n## 故事梗概\n[无故事内容]"
    
    # 修复收集记录部分
    if not re.search(r'## 收集记录', fixed_content, re.MULTILINE):
        now = datetime.now().strftime('%Y-%m')
        fixed_content += f"\n\n## A收集记录\n- 收集时间: {now}\n- 收集人: 自动收集\n- 完整性: 部分"
    
    return fixed_content 