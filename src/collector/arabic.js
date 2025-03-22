const BaseCollector = require('./base');
const logger = require('../utils/logger');

class ArabicCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'AR';
    this.regions = {
      egypt: ['Cairo', 'Alexandria', 'Luxor', 'Aswan', 'Sharm El Sheikh'],
      saudi: ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam'],
      uae: ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ras Al Khaimah'],
      morocco: ['Casablanca', 'Rabat', 'Marrakech', 'Fez', 'Tangier']
    };
    this.storyTypes = {
      fairy_tale: 'حكاية خرافية',
      myth: 'أسطورة',
      folk_tale: 'قصة شعبية',
      legend: 'أسطورة'
    };
  }

  async collectStory(storyData) {
    try {
      logger.info('بدء جمع القصة العربية...');

      // 验证地区
      if (!this.isValidRegion(storyData.region)) {
        throw new Error(`المنطقة غير مدعومة: ${storyData.region}`);
      }

      // 检查故事是否已存在
      const existingStory = await this.notion.checkStoryExists({
        story_id: this.generateStoryId(storyData),
        title: this.generateTitle(storyData)
      });

      if (existingStory.exists) {
        logger.info('القصة موجودة بالفعل. تخطي...');
        return existingStory.story;
      }

      // 生成故事内容
      const story = await this.generateStory(storyData);

      // 生成 Markdown 内容
      const markdownContent = this.generateMarkdown(story);

      // 保存到 Notion
      const savedStory = await this.notion.createStory(story, markdownContent);

      if (savedStory) {
        logger.info('تم حفظ القصة بنجاح');
        return savedStory;
      } else {
        logger.error('فشل في حفظ القصة');
        return null;
      }
    } catch (error) {
      logger.error('فشل في جمع القصة العربية:', error);
      return null;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    const country = this.getCountryFromRegion(storyData.region);
    return `AR_${country.toUpperCase()}_${storyData.type.toUpperCase()}_${timestamp}`;
  }

  generateTitle(storyData) {
    const arabicType = this.storyTypes[storyData.type] || storyData.type;
    return `${storyData.region}_${arabicType}_${this.generateStoryId(storyData)}`;
  }

  async generateStory(storyData) {
    // 这里可以添加故事生成逻辑，可以使用 AI 模型或其他方式
    return {
      ...storyData,
      story_id: this.generateStoryId(storyData),
      title: this.generateTitle(storyData),
      content: 'هذا مثال لمحتوى القصة.', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    const arabicType = this.storyTypes[story.type] || story.type;
    return `# ${story.title}

## معلومات القصة
- المعرف: ${story.story_id}
- النوع: ${arabicType}
- المنطقة: ${story.region}
- الفئة العمرية: ${story.age_group}
- الموضوعات التعليمية: ${story.educational_themes.join(', ')}
- الطول: ${story.length}
- المصدر الثقافي: ${story.cultural_source}

## محتوى القصة
${story.content}

## تاريخ الإنشاء
${story.created_at}
`;
  }

  validateStoryData(storyData) {
    super.validateStoryData(storyData);

    // 验证地区
    if (!this.isValidRegion(storyData.region)) {
      throw new Error(`المنطقة غير مدعومة: ${storyData.region}`);
    }

    // 验证故事类型
    if (!Object.keys(this.storyTypes).includes(storyData.type)) {
      throw new Error(`نوع القصة غير مدعوم: ${storyData.type}`);
    }

    // 验证文化来源
    const country = this.getCountryFromRegion(storyData.region);
    const validSources = {
      egypt: ['Egyptian', 'Ancient Egyptian', 'Islamic', 'Coptic'],
      saudi: ['Saudi', 'Islamic', 'Bedouin', 'Najdi'],
      uae: ['Emirati', 'Islamic', 'Bedouin', 'Gulf'],
      morocco: ['Moroccan', 'Berber', 'Islamic', 'Andalusian']
    };

    if (!validSources[country].includes(storyData.cultural_source)) {
      throw new Error(`المصدر الثقافي غير مدعوم لـ ${country}: ${storyData.cultural_source}`);
    }

    // 验证教育主题
    const validThemes = [
      'الشجاعة', 'الحكمة', 'الصدق', 'الاحترام',
      'الصبر', 'التعاون', 'الإبداع', 'الفضول'
    ];
    const invalidThemes = storyData.educational_themes.filter(
      theme => !validThemes.includes(theme)
    );
    if (invalidThemes.length > 0) {
      throw new Error(`الموضوعات التعليمية غير مدعومة: ${invalidThemes.join(', ')}`);
    }

    return true;
  }

  isValidRegion(region) {
    return Object.values(this.regions).some(cities => cities.includes(region));
  }

  getCountryFromRegion(region) {
    for (const [country, cities] of Object.entries(this.regions)) {
      if (cities.includes(region)) {
        return country;
      }
    }
    throw new Error(`لم يتم العثور على المنطقة: ${region}`);
  }
}

module.exports = ArabicCollector; 