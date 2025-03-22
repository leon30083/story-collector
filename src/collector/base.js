class BaseCollector {
  constructor(notion) {
    if (new.target === BaseCollector) {
      throw new Error('BaseCollector 不能直接实例化');
    }
    this.notion = notion;
    this.language = null;
  }

  async collectStory(storyData) {
    throw new Error('子类必须实现 collectStory 方法');
  }

  generateStoryId(storyData) {
    throw new Error('子类必须实现 generateStoryId 方法');
  }

  generateTitle(storyData) {
    throw new Error('子类必须实现 generateTitle 方法');
  }

  generateStory(storyData) {
    throw new Error('子类必须实现 generateStory 方法');
  }

  generateMarkdown(story) {
    throw new Error('子类必须实现 generateMarkdown 方法');
  }

  validateStoryData(storyData) {
    const requiredFields = [
      'type',
      'region',
      'age_group',
      'educational_themes',
      'length',
      'cultural_source'
    ];

    for (const field of requiredFields) {
      if (!storyData[field]) {
        throw new Error(`缺少必要字段: ${field}`);
      }
    }

    if (!Array.isArray(storyData.educational_themes)) {
      throw new Error('educational_themes 必须是数组');
    }

    return true;
  }
}

module.exports = BaseCollector; 