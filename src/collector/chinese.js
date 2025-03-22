const BaseCollector = require('./base');
const logger = require('../utils/logger');

class ChineseCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'CN';
  }

  async collectStory(storyData) {
    try {
      logger.info('开始收集中文故事...');

      // 检查故事是否已存在
      const existingStory = await this.notion.checkStoryExists({
        story_id: this.generateStoryId(storyData),
        title: this.generateTitle(storyData)
      });

      if (existingStory.exists) {
        logger.info('故事已存在，跳过收集');
        return existingStory.story;
      }

      // 生成故事内容
      const story = await this.generateStory(storyData);

      // 生成 Markdown 内容
      const markdownContent = this.generateMarkdown(story);

      // 保存到 Notion
      const savedStory = await this.notion.createStory(story, markdownContent);

      if (savedStory) {
        logger.info('故事保存成功');
        return savedStory;
      } else {
        logger.error('故事保存失败');
        return null;
      }
    } catch (error) {
      logger.error('中文故事收集失败:', error);
      return null;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    return `CN_${storyData.type.toUpperCase()}_${timestamp}`;
  }

  generateTitle(storyData) {
    return `${storyData.region}_${storyData.type}_${this.generateStoryId(storyData)}`;
  }

  async generateStory(storyData) {
    // 这里可以添加故事生成逻辑，可以使用 AI 模型或其他方式
    return {
      ...storyData,
      story_id: this.generateStoryId(storyData),
      title: this.generateTitle(storyData),
      content: '这是一个示例故事内容。', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    return `# ${story.title}

## 故事信息
- ID: ${story.story_id}
- 类型: ${story.type}
- 地区: ${story.region}
- 年龄段: ${story.age_group}
- 教育主题: ${story.educational_themes.join(', ')}
- 故事长度: ${story.length}
- 文化来源: ${story.cultural_source}

## 故事内容
${story.content}

## 创建时间
${story.created_at}
`;
  }
}

module.exports = ChineseCollector; 