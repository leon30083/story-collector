const ChineseCollector = require('../src/collector/chinese');
const EnglishCollector = require('../src/collector/english');
const JapaneseCollector = require('../src/collector/japanese');
const SpanishCollector = require('../src/collector/spanish');
const ArabicCollector = require('../src/collector/arabic');
const HindiCollector = require('../src/collector/hindi');
const NotionIntegration = require('../src/integration/notion');

describe('Story Collection Integration Tests', () => {
  let notion;
  let collectors;

  beforeEach(() => {
    notion = new NotionIntegration();
    collectors = {
      chinese: new ChineseCollector(notion),
      english: new EnglishCollector(notion),
      japanese: new JapaneseCollector(notion),
      spanish: new SpanishCollector(notion),
      arabic: new ArabicCollector(notion),
      hindi: new HindiCollector(notion)
    };
  });

  describe('Chinese Story Collection', () => {
    test('should collect a Chinese story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: '华东',
        age_group: '3-4岁',
        educational_themes: ['勇气', '智慧'],
        length: '短篇',
        cultural_source: '浙江民间故事'
      };

      const result = await collectors.chinese.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('English Story Collection', () => {
    test('should collect an English story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: 'London',
        age_group: '3-4岁',
        educational_themes: ['courage', 'wisdom'],
        length: 'short',
        cultural_source: 'British'
      };

      const result = await collectors.english.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('Japanese Story Collection', () => {
    test('should collect a Japanese story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: 'Tokyo',
        age_group: '3-4岁',
        educational_themes: ['勇気', '知恵'],
        length: '短篇',
        cultural_source: 'Japanese'
      };

      const result = await collectors.japanese.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('Spanish Story Collection', () => {
    test('should collect a Spanish story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: 'Madrid',
        age_group: '3-4岁',
        educational_themes: ['Valentía', 'Sabiduría'],
        length: 'corto',
        cultural_source: 'Spanish'
      };

      const result = await collectors.spanish.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('Arabic Story Collection', () => {
    test('should collect an Arabic story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: 'Cairo',
        age_group: '3-4岁',
        educational_themes: ['الشجاعة', 'الحكمة'],
        length: 'قصير',
        cultural_source: 'Egyptian'
      };

      const result = await collectors.arabic.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('Hindi Story Collection', () => {
    test('should collect a Hindi story successfully', async () => {
      const storyData = {
        type: 'fairy_tale',
        region: 'Delhi',
        age_group: '3-4岁',
        educational_themes: ['साहस', 'बुद्धिमत्ता'],
        length: 'लघु',
        cultural_source: 'Hindu'
      };

      const result = await collectors.hindi.collectStory(storyData);
      expect(result).toBeTruthy();
    });
  });

  describe('Error Handling', () => {
    test('should handle invalid story data', async () => {
      const invalidStoryData = {
        type: 'invalid_type',
        region: 'InvalidRegion'
      };

      await expect(collectors.english.collectStory(invalidStoryData))
        .rejects
        .toThrow('不支持的地区');
    });
  });
}); 