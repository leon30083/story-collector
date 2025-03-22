# AI Assistant Guide for Story Collection System

## System Overview

This document provides guidance for AI assistants on how to effectively utilize the Story Collection System. The system is designed to collect, validate, and store culturally diverse stories suitable for children aged 3-6 years.

### Core Components

```python
StoryCollector/
├── src/                # Source code
│   ├── main.py        # Main program
│   ├── collector/     # Story collection module
│   ├── formatter/     # Format module
│   ├── database/      # Database module
│   ├── integration/   # Integration module
│   └── utils/         # Utility functions
├── data/              # Data storage
│   ├── stories/       # Story files
│   └── database/      # Database files
├── config/            # Configuration files
├── docs/              # Documentation
├── logs/              # Log files
└── tests/             # Test code
```

## Command Interface

### Basic Command Structure

```bash
python src/main.py --language <LANG> --region <REGION> --type <TYPE> --count <COUNT>
```

### Parameter Details

1. `--language` (Required)
   - Format: Two-letter language code
   - Supported languages:
     - `CN`: Chinese (中文) - Unified collection for all Chinese stories
     - `EN`: English - City-specific collection
     - `JP`: Japanese (日本語) - City-specific collection
     - `FR`: French - City-specific collection
     - `DE`: German - City-specific collection

2. `--region` (Required)
   - Format: Region or city name
   - Special rules:
     - For Chinese (CN): Always use "中国"
     - For other languages: Specify city name
   - Examples:
     - Chinese: 中国
     - English: London, Edinburgh
     - Japanese: Tokyo, Kyoto
     - French: Paris, Lyon
     - German: Berlin, Munich

3. `--type` (Required)
   - Story categories:
     - `idiom`: 成语故事 (Idiom stories)
     - `fairy_tale`: 寓言故事 (Fairy tales)
     - `legend`: 经典童话 (Classic tales)
     - `myth`: 神话故事 (Myths)
     - `folk_tale`: 民间故事 (Folk tales)
     - `other`: 其他 (Others)

4. `--count` (Optional)
   - Default: 1
   - Recommended range: 1-10
   - Note: Larger numbers increase processing time

## Story File Format

### File Naming Convention
- Pattern: `[Language]_[Type]_[ID]_[Title].md`
- Examples:
  - Chinese: `中文_童话_CN001_月亮里小兔子的故事.md`
  - English: `EN_legend_EN001_The_Whispering_Woods.md`
  - Japanese: `JP_myth_JP001_桜の精.md`

### Content Structure
```markdown
# Story Title

## Story Introduction
[Brief introduction]

## Story Content
[Detailed content]

## Story Moral
[Educational value]

## Creation Time
[Timestamp]
```

## AI Assistant Usage Guidelines

### 1. Pre-Collection Checks

Before collecting stories:
1. Verify language and region compatibility
2. Check story type appropriateness
3. Confirm target audience suitability (3-6 years)
4. Review existing stories to avoid duplicates
5. Verify Notion integration status (if enabled)

### 2. Command Examples

```bash
# Chinese fairy tale collection
python src/main.py --language CN --region 中国 --type fairy_tale --count 1

# English legend from London
python src/main.py --language EN --region London --type legend --count 1

# Japanese myth from Tokyo
python src/main.py --language JP --region Tokyo --type myth --count 1
```

### 3. Output Handling

Success output example:
```
[INFO] Story Collection Started
[INFO] Loading existing stories...
[INFO] Collecting new story...
[INFO] Story saved: data/stories/CN/fairy_tale/中文_童话_CN001_story.md
[INFO] Notion sync completed
[INFO] Collection completed successfully
```

Error handling:
1. Duplicate detection:
   - System automatically skips duplicates
   - Check logs for details

2. Invalid parameters:
   - Verify language code format
   - Confirm region spelling
   - Ensure valid story type

3. Notion sync errors:
   - Check API key validity
   - Verify database access
   - Monitor sync status

### 4. Quality Assurance

Verify the following aspects:
1. Content appropriateness
   - Age-suitable (3-6 years)
   - Educational value
   - Cultural sensitivity
   - Language clarity

2. Technical validation
   - Correct file format
   - Proper metadata
   - Valid story structure
   - Accurate categorization

3. Notion integration
   - Data synchronization
   - Property mapping
   - Access permissions

### 5. Best Practices

1. Story Collection
   - Start with single story requests
   - Use appropriate language-region combinations
   - Follow naming conventions
   - Maintain cultural authenticity

2. Region Handling
   - Use "中国" for all Chinese stories
   - Specify cities for other languages
   - Respect regional traditions
   - Consider cultural context

3. Error Prevention
   - Validate parameters before execution
   - Check for duplicate stories
   - Verify file paths
   - Monitor system logs

4. Notion Integration
   - Verify sync status
   - Check property mappings
   - Monitor API rate limits
   - Handle sync conflicts

## System Features

### 1. Automated Functions
- Story ID generation
- Duplicate detection
- File naming standardization
- Category-based storage
- SQLite database support
- Notion synchronization

### 2. Quality Controls
- Format validation
- Content verification
- Cultural sensitivity check
- Educational value assessment
- Sync status monitoring

### 3. Management Features
- Detailed operation logs
- Statistical reporting
- Batch collection support
- Database management
- Notion collaboration

## Troubleshooting Guide

### Common Issues

1. Story Not Saved
   - Check file permissions
   - Verify directory structure
   - Ensure valid parameters
   - Check Notion sync status

2. Duplicate Detection
   - Review existing stories
   - Check database records
   - Verify uniqueness criteria
   - Check Notion duplicates

3. Database Errors
   - Check SQLite connection
   - Verify table structure
   - Confirm unique constraints
   - Monitor Notion sync

4. Notion Integration Issues
   - Verify API key
   - Check database access
   - Monitor rate limits
   - Handle sync conflicts

### Resolution Steps

1. Parameter Validation
   - Verify language code
   - Check region name
   - Confirm story type
   - Validate count range

2. System Status
   - Check log files
   - Verify database status
   - Confirm directory permissions
   - Monitor Notion status

3. Content Verification
   - Review story format
   - Check metadata
   - Validate content structure
   - Verify Notion properties

## Version Information

- System Version: 0.2.0
- Documentation Version: 0.2.0
- Last Updated: 2024-03-21

## Support

For technical issues:
1. Check system logs in `logs/` directory
2. Review error messages
3. Verify configuration in `config/` directory
4. Test with example commands
5. Check Notion integration status

## Notion Integration

### Overview
The system supports integration with Notion databases, allowing you to:
- View and query stories directly in Notion
- Sync stories automatically between local storage and Notion
- Use Notion's powerful filtering and sorting capabilities
- Collaborate with team members through Notion

### Setup Requirements
1. Notion API Key
   - Get your API key from https://www.notion.so/my-integrations
   - Add it to `config/notion_config.py`

2. Notion Database
   - Create a new database in Notion
   - Copy the database ID from the URL
   - Add it to `config/notion_config.py`

### Database Properties
   Required properties in Notion database:
   - 名称 (Title)：故事标题
   - 故事分类 (Select)：故事类型选项
     - 成语故事
     - 寓言故事
     - 经典童话
     - 神话故事
     - 民间故事
     - 其他
   - 故事内容 (Rich text)：故事简短概述
   - 更新时间 (Date)：最后更新时间
   - 地区 (Rich text)：故事来源地区
   - 语言 (Select)：故事语言
     - 中文
     - 英文
     - 日文
     - 法文
     - 德文
     - 其他
   - 故事ID (Rich text)：唯一标识符
   - 原始文件：每个故事页面包含原始 Markdown 文件内容

### Extended Classification System
The system now supports a multi-dimensional classification approach:

1. Age Groups (Select)
   - 3-4岁
   - 4-5岁
   - 5-6岁

2. Educational Themes (Multi-select)
   - 品德教育 (Moral Education)
   - 智慧启发 (Wisdom Inspiration)
   - 情感教育 (Emotional Education)
   - 生活教育 (Life Education)

3. Story Length (Select)
   - 微故事 (100字以内)
   - 短篇故事 (100-500字)
   - 中篇故事 (500-1000字)
   - 长篇故事 (1000字以上)

4. Cultural Source (Select)
   - 中国传统 (Chinese Traditional)
   - 世界经典 (World Classics)
   - 现代创作 (Modern Creation)

For detailed classification guidelines, refer to `docs/story_classification_guide.md`.

### Usage

#### 1. Query Stories in Notion
```python
from src.integration.notion_integration import NotionIntegration

# Initialize Notion integration
notion = NotionIntegration()

# Query all stories
stories = notion.query_stories()

# Query with filters
filter_params = {
    "property": "故事ID",
    "rich_text": {
        "equals": "CN001"
    }
}
filtered_stories = notion.query_stories(filter_params)
```

#### 2. Sync Stories
Stories are automatically synced to Notion when:
- New stories are collected
- Existing stories are updated
- Manual sync is triggered using `python src/main.py --sync-notion`

Each story page in Notion will include:
- All configured properties
- Original Markdown file content as a code block
- File name as a heading

#### 3. Notion Features
You can use Notion's features to:
- Filter stories by language, region, or type
- Sort stories by creation date
- Create views for different story categories
- Add comments and discussions
- Share with team members
- View and copy original story files

### Best Practices
1. Database Organization
   - Use Notion's views to organize stories
   - Create filters for common queries
   - Set up sorting for easy access
   - Ensure property types match the system settings

2. Collaboration
   - Use Notion's sharing features
   - Add comments for feedback
   - Track changes through history
   - Maintain consistent property formats

3. Performance
   - Use filters to limit query results
   - Avoid querying all stories at once
   - Monitor sync status
   - Handle long text content appropriately

4. Error Handling
   - Check API responses
   - Validate property types
   - Monitor rate limits
   - Handle sync conflicts
   - Log sync operations

5. Security
   - Protect API keys
   - Manage access permissions
   - Monitor integration usage
   - Review sync logs regularly 