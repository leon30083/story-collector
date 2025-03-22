const BaseCollector = require('./base');
const logger = require('../utils/logger');

class HindiCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'HI';
    this.regions = {
      india: ['Delhi', 'Mumbai', 'Jaipur', 'Varanasi', 'Agra'],
      nepal: ['Kathmandu', 'Pokhara', 'Lalitpur', 'Bharatpur', 'Birgunj'],
      mauritius: ['Port Louis', 'Curepipe', 'Quatre Bornes', 'Rose Hill', 'Vacoas']
    };
    this.storyTypes = {
      fairy_tale: 'परी कथा',
      myth: 'पौराणिक कथा',
      folk_tale: 'लोक कथा',
      legend: 'किंवदंती'
    };
  }

  async collectStory(storyData) {
    try {
      logger.info('हिंदी कहानी एकत्र करना शुरू कर रहा है...');

      // 验证地区
      if (!this.isValidRegion(storyData.region)) {
        throw new Error(`असमर्थित क्षेत्र: ${storyData.region}`);
      }

      // 检查故事是否已存在
      const existingStory = await this.notion.checkStoryExists({
        story_id: this.generateStoryId(storyData),
        title: this.generateTitle(storyData)
      });

      if (existingStory.exists) {
        logger.info('कहानी पहले से मौजूद है। छोड़ रहा है...');
        return existingStory.story;
      }

      // 生成故事内容
      const story = await this.generateStory(storyData);

      // 生成 Markdown 内容
      const markdownContent = this.generateMarkdown(story);

      // 保存到 Notion
      const savedStory = await this.notion.createStory(story, markdownContent);

      if (savedStory) {
        logger.info('कहानी सफलतापूर्वक सहेजी गई');
        return savedStory;
      } else {
        logger.error('कहानी सहेजने में विफल');
        return null;
      }
    } catch (error) {
      logger.error('हिंदी कहानी एकत्र करने में विफल:', error);
      return null;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    const country = this.getCountryFromRegion(storyData.region);
    return `HI_${country.toUpperCase()}_${storyData.type.toUpperCase()}_${timestamp}`;
  }

  generateTitle(storyData) {
    const hindiType = this.storyTypes[storyData.type] || storyData.type;
    return `${storyData.region}_${hindiType}_${this.generateStoryId(storyData)}`;
  }

  async generateStory(storyData) {
    // 这里可以添加故事生成逻辑，可以使用 AI 模型或其他方式
    return {
      ...storyData,
      story_id: this.generateStoryId(storyData),
      title: this.generateTitle(storyData),
      content: 'यह कहानी का एक उदाहरण है।', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    const hindiType = this.storyTypes[story.type] || story.type;
    return `# ${story.title}

## कहानी की जानकारी
- पहचानकर्ता: ${story.story_id}
- प्रकार: ${hindiType}
- क्षेत्र: ${story.region}
- आयु वर्ग: ${story.age_group}
- शैक्षिक विषय: ${story.educational_themes.join(', ')}
- लंबाई: ${story.length}
- सांस्कृतिक स्रोत: ${story.cultural_source}

## कहानी का विषय
${story.content}

## निर्माण तिथि
${story.created_at}
`;
  }

  validateStoryData(storyData) {
    super.validateStoryData(storyData);

    // 验证地区
    if (!this.isValidRegion(storyData.region)) {
      throw new Error(`असमर्थित क्षेत्र: ${storyData.region}`);
    }

    // 验证故事类型
    if (!Object.keys(this.storyTypes).includes(storyData.type)) {
      throw new Error(`असमर्थित कहानी प्रकार: ${storyData.type}`);
    }

    // 验证文化来源
    const country = this.getCountryFromRegion(storyData.region);
    const validSources = {
      india: ['Indian', 'Hindu', 'Buddhist', 'Jain', 'Sikh'],
      nepal: ['Nepali', 'Hindu', 'Buddhist', 'Newari'],
      mauritius: ['Mauritian', 'Hindu', 'Indo-Mauritian']
    };

    if (!validSources[country].includes(storyData.cultural_source)) {
      throw new Error(`${country} के लिए असमर्थित सांस्कृतिक स्रोत: ${storyData.cultural_source}`);
    }

    // 验证教育主题
    const validThemes = [
      'साहस', 'बुद्धिमत्ता', 'ईमानदारी', 'सम्मान',
      'धैर्य', 'सहयोग', 'रचनात्मकता', 'जिज्ञासा'
    ];
    const invalidThemes = storyData.educational_themes.filter(
      theme => !validThemes.includes(theme)
    );
    if (invalidThemes.length > 0) {
      throw new Error(`असमर्थित शैक्षिक विषय: ${invalidThemes.join(', ')}`);
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
    throw new Error(`क्षेत्र नहीं मिला: ${region}`);
  }
}

module.exports = HindiCollector; 