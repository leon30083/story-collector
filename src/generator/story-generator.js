const logger = require('../utils/logger');

class StoryGenerator {
  constructor() {
    this.templates = {
      fairy_tale: {
        structure: [
          'Once upon a time...',
          'There was a {character} who...',
          'One day...',
          'After that...',
          'And they lived happily ever after.'
        ],
        characters: ['princess', 'prince', 'witch', 'dragon', 'fairy', 'king', 'queen', 'knight'],
        settings: ['castle', 'forest', 'mountain', 'ocean', 'village', 'city', 'garden']
      },
      myth: {
        structure: [
          'In the beginning...',
          'The gods decided to...',
          'But then...',
          'As a result...',
          'And that is why...'
        ],
        characters: ['god', 'goddess', 'hero', 'monster', 'spirit', 'mortal'],
        settings: ['heaven', 'earth', 'underworld', 'mountain', 'sea', 'sky']
      },
      folk_tale: {
        structure: [
          'Long ago...',
          'There lived a {character} who...',
          'One day...',
          'After that...',
          'And that is how...'
        ],
        characters: ['farmer', 'merchant', 'artisan', 'scholar', 'monk', 'villager'],
        settings: ['village', 'market', 'temple', 'field', 'mountain', 'river']
      }
    };
  }

  generateStory(storyData) {
    try {
      const template = this.templates[storyData.type];
      if (!template) {
        throw new Error(`不支持的故事类型: ${storyData.type}`);
      }

      // 根据年龄段调整故事复杂度
      const complexity = this.getComplexity(storyData.age_group);

      // 生成故事内容
      const content = this.generateContent(template, complexity);

      // 添加教育主题
      const storyWithThemes = this.addEducationalThemes(content, storyData.educational_themes);

      // 添加文化元素
      const storyWithCulture = this.addCulturalElements(storyWithThemes, storyData.cultural_source);

      return storyWithCulture;
    } catch (error) {
      logger.error('故事生成失败:', error);
      throw error;
    }
  }

  getComplexity(ageGroup) {
    switch (ageGroup) {
      case '3-4岁':
        return {
          sentenceLength: 5,
          vocabularyLevel: 'simple',
          plotComplexity: 'basic'
        };
      case '4-5岁':
        return {
          sentenceLength: 8,
          vocabularyLevel: 'medium',
          plotComplexity: 'moderate'
        };
      case '5-6岁':
        return {
          sentenceLength: 12,
          vocabularyLevel: 'advanced',
          plotComplexity: 'complex'
        };
      default:
        return {
          sentenceLength: 8,
          vocabularyLevel: 'medium',
          plotComplexity: 'moderate'
        };
    }
  }

  generateContent(template, complexity) {
    const character = this.getRandomElement(template.characters);
    const setting = this.getRandomElement(template.settings);

    return template.structure
      .map(sentence => {
        return sentence
          .replace('{character}', character)
          .replace('{setting}', setting);
      })
      .join('\n\n');
  }

  addEducationalThemes(content, themes) {
    // 这里可以添加教育主题相关的逻辑
    return content;
  }

  addCulturalElements(content, culturalSource) {
    // 这里可以添加文化元素相关的逻辑
    return content;
  }

  getRandomElement(array) {
    return array[Math.floor(Math.random() * array.length)];
  }
}

module.exports = StoryGenerator; 