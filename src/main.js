const { program } = require('commander');
const { NotionIntegration } = require('./integration');
const { ChineseCollector, EnglishCollector, JapaneseCollector } = require('./collector');
const logger = require('./utils/logger');
const validator = require('./utils/validator');

// 配置命令行参数
program
  .version('0.3.0')
  .option('-l, --language <type>', '故事语言 (CN/EN/JP)')
  .option('-r, --region <name>', '故事地区')
  .option('-t, --type <type>', '故事类型 (idiom/fairy_tale/legend/myth/folk_tale)')
  .option('-c, --count <number>', '收集数量', '1')
  .option('--age <group>', '年龄段 (3-4岁/4-5岁/5-6岁)')
  .option('--themes <themes...>', '教育主题 (品德教育/智慧启发/情感教育/生活教育)')
  .option('--length <length>', '故事长度 (微故事/短篇故事/中篇故事/长篇故事)')
  .option('--source <source>', '文化来源 (中国传统/世界经典/现代创作)')
  .parse(process.argv);

const options = program.opts();

// 验证参数
if (!options.language || !options.region || !options.type) {
  console.error('错误: 必须提供语言、地区和故事类型参数');
  process.exit(1);
}

// 验证语言和地区组合
if (!validator.validateLanguageRegion(options.language, options.region)) {
  console.error('错误: 无效的语言和地区组合');
  process.exit(1);
}

// 初始化 Notion 集成
const notion = new NotionIntegration();

// 根据语言选择合适的收集器
function getCollector(language) {
  switch (language.toUpperCase()) {
    case 'CN':
      return new ChineseCollector(notion);
    case 'EN':
      return new EnglishCollector(notion);
    case 'JP':
      return new JapaneseCollector(notion);
    default:
      throw new Error(`不支持的语言: ${language}`);
  }
}

async function main() {
  try {
    logger.info('开始收集故事...');
    logger.info(`参数: 语言=${options.language}, 地区=${options.region}, 类型=${options.type}, 数量=${options.count}`);

    const collector = getCollector(options.language);
    
    // 准备故事数据
    const storyData = {
      language: options.language,
      region: options.region,
      type: options.type,
      age_group: options.age || '3-4岁',
      educational_themes: options.themes || ['品德教育'],
      length: options.length || '短篇故事',
      cultural_source: options.source || (options.language === 'CN' ? '中国传统' : '世界经典')
    };

    // 验证故事数据
    const validation = validator.validateStoryData(storyData);
    if (!validation.isValid) {
      console.error('错误: 无效的故事数据:', validation.errors.join(', '));
      process.exit(1);
    }

    // 收集故事
    const count = parseInt(options.count, 10);
    for (let i = 0; i < count; i++) {
      logger.info(`正在收集第 ${i + 1}/${count} 个故事...`);
      const story = await collector.collectStory(storyData);
      if (story) {
        logger.info(`成功收集故事: ${story.title}`);
      } else {
        logger.error('故事收集失败');
      }
    }

    logger.info('故事收集完成');
  } catch (error) {
    logger.error('故事收集失败:', error);
    process.exit(1);
  }
}

main(); 