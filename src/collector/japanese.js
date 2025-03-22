const BaseCollector = require('./base');
const logger = require('../utils/logger');

class JapaneseCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'JP';
    this.regions = ['Tokyo', 'Kyoto', 'Osaka', 'Hokkaido', 'Fukuoka', 'Nagoya'];
    this.storyTypes = {
      fairy_tale: '童話',
      myth: '神話',
      folk_tale: '民話',
      legend: '伝説'
    };
  }

  async collectStory(storyData) {
    try {
      logger.info('日本語の物語を収集開始...');

      // 验证地区
      if (!this.regions.includes(storyData.region)) {
        throw new Error(`サポートされていない地域: ${storyData.region}`);
      }

      // 检查故事是否已存在
      const existingStory = await this.notion.checkStoryExists({
        story_id: this.generateStoryId(storyData),
        title: this.generateTitle(storyData)
      });

      if (existingStory.exists) {
        logger.info('物語は既に存在します。スキップします。');
        return existingStory.story;
      }

      // 生成故事内容
      const story = await this.generateStory(storyData);

      // 生成 Markdown 内容
      const markdownContent = this.generateMarkdown(story);

      // 保存到 Notion
      const savedStory = await this.notion.createStory(story, markdownContent);

      if (savedStory) {
        logger.info('物語の保存に成功しました。');
        return savedStory;
      } else {
        logger.error('物語の保存に失敗しました。');
        return null;
      }
    } catch (error) {
      logger.error('日本語の物語収集に失敗:', error);
      return null;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    return `JP_${storyData.region.toUpperCase()}_${storyData.type.toUpperCase()}_${timestamp}`;
  }

  generateTitle(storyData) {
    const japaneseType = this.storyTypes[storyData.type] || storyData.type;
    return `${storyData.region}_${japaneseType}_${this.generateStoryId(storyData)}`;
  }

  async generateStory(storyData) {
    // 这里可以添加故事生成逻辑，可以使用 AI 模型或其他方式
    return {
      ...storyData,
      story_id: this.generateStoryId(storyData),
      title: this.generateTitle(storyData),
      content: 'これは物語の例です。', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    const japaneseType = this.storyTypes[story.type] || story.type;
    return `# ${story.title}

## 物語情報
- ID: ${story.story_id}
- 種類: ${japaneseType}
- 地域: ${story.region}
- 年齢層: ${story.age_group}
- 教育的テーマ: ${story.educational_themes.join(', ')}
- 長さ: ${story.length}
- 文化的出典: ${story.cultural_source}

## 物語内容
${story.content}

## 作成日時
${story.created_at}
`;
  }

  validateStoryData(storyData) {
    super.validateStoryData(storyData);

    // 验证地区
    if (!this.regions.includes(storyData.region)) {
      throw new Error(`サポートされていない地域: ${storyData.region}`);
    }

    // 验证故事类型
    if (!Object.keys(this.storyTypes).includes(storyData.type)) {
      throw new Error(`サポートされていない物語の種類: ${storyData.type}`);
    }

    // 验证文化来源
    if (!['Japanese', 'Ainu', 'Ryukyuan'].includes(storyData.cultural_source)) {
      throw new Error(`サポートされていない文化的出典: ${storyData.cultural_source}`);
    }

    // 验证教育主题
    const validThemes = [
      '勇気', '知恵', '誠実', '礼儀',
      '忍耐', '協力', '創造性', '好奇心'
    ];
    const invalidThemes = storyData.educational_themes.filter(
      theme => !validThemes.includes(theme)
    );
    if (invalidThemes.length > 0) {
      throw new Error(`サポートされていない教育的テーマ: ${invalidThemes.join(', ')}`);
    }

    return true;
  }
}

module.exports = JapaneseCollector; 