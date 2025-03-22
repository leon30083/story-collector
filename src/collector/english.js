const BaseCollector = require('./base');
const logger = require('../utils/logger');

class EnglishCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'EN';
    this.regions = ['London', 'Edinburgh', 'Dublin', 'New York', 'Boston', 'Toronto', 'Sydney', 'Melbourne'];
  }

  async collectStory(storyData) {
    try {
      logger.info('开始收集英语故事...');

      // 验证地区
      if (!this.regions.includes(storyData.region)) {
        throw new Error(`不支持的地区: ${storyData.region}`);
      }

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
        throw new Error('故事保存失败');
      }
    } catch (error) {
      logger.error('英语故事收集失败:', error);
      throw error;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    return `EN_${storyData.region.toUpperCase()}_${storyData.type.toUpperCase()}_${timestamp}`;
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
      content: 'This is an example story content.', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    return `# ${story.title}

## Story Information
- ID: ${story.story_id}
- Type: ${story.type}
- Region: ${story.region}
- Age Group: ${story.age_group}
- Educational Themes: ${story.educational_themes.join(', ')}
- Length: ${story.length}
- Cultural Source: ${story.cultural_source}

## Story Content
${story.content}

## Created At
${story.created_at}
`;
  }

  validateStoryData(storyData) {
    super.validateStoryData(storyData);

    // 验证地区
    if (!this.regions.includes(storyData.region)) {
      throw new Error(`不支持的地区: ${storyData.region}`);
    }

    // 验证文化来源
    if (!['British', 'American', 'Australian', 'Canadian'].includes(storyData.cultural_source)) {
      throw new Error(`不支持的文化来源: ${storyData.cultural_source}`);
    }

    return true;
  }
}

module.exports = EnglishCollector; 