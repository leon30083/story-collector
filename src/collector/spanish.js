const BaseCollector = require('./base');
const logger = require('../utils/logger');

class SpanishCollector extends BaseCollector {
  constructor(notion) {
    super(notion);
    this.language = 'SP';
    this.regions = {
      spain: ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Bilbao'],
      mexico: ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Oaxaca'],
      argentina: ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata'],
      colombia: ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
    };
    this.storyTypes = {
      fairy_tale: 'cuento de hadas',
      myth: 'mito',
      folk_tale: 'cuento popular',
      legend: 'leyenda'
    };
  }

  async collectStory(storyData) {
    try {
      logger.info('Iniciando recolección de cuento en español...');

      // 验证地区
      if (!this.isValidRegion(storyData.region)) {
        throw new Error(`Región no soportada: ${storyData.region}`);
      }

      // 检查故事是否已存在
      const existingStory = await this.notion.checkStoryExists({
        story_id: this.generateStoryId(storyData),
        title: this.generateTitle(storyData)
      });

      if (existingStory.exists) {
        logger.info('El cuento ya existe. Saltando...');
        return existingStory.story;
      }

      // 生成故事内容
      const story = await this.generateStory(storyData);

      // 生成 Markdown 内容
      const markdownContent = this.generateMarkdown(story);

      // 保存到 Notion
      const savedStory = await this.notion.createStory(story, markdownContent);

      if (savedStory) {
        logger.info('Cuento guardado exitosamente');
        return savedStory;
      } else {
        logger.error('Error al guardar el cuento');
        return null;
      }
    } catch (error) {
      logger.error('Error en la recolección del cuento en español:', error);
      return null;
    }
  }

  generateStoryId(storyData) {
    const timestamp = Date.now();
    const country = this.getCountryFromRegion(storyData.region);
    return `SP_${country.toUpperCase()}_${storyData.type.toUpperCase()}_${timestamp}`;
  }

  generateTitle(storyData) {
    const spanishType = this.storyTypes[storyData.type] || storyData.type;
    return `${storyData.region}_${spanishType}_${this.generateStoryId(storyData)}`;
  }

  async generateStory(storyData) {
    // 这里可以添加故事生成逻辑，可以使用 AI 模型或其他方式
    return {
      ...storyData,
      story_id: this.generateStoryId(storyData),
      title: this.generateTitle(storyData),
      content: 'Este es un ejemplo de contenido del cuento.', // 这里需要替换为实际的故事生成逻辑
      created_at: new Date().toISOString()
    };
  }

  generateMarkdown(story) {
    const spanishType = this.storyTypes[story.type] || story.type;
    return `# ${story.title}

## Información del Cuento
- ID: ${story.story_id}
- Tipo: ${spanishType}
- Región: ${story.region}
- Grupo de Edad: ${story.age_group}
- Temas Educativos: ${story.educational_themes.join(', ')}
- Longitud: ${story.length}
- Fuente Cultural: ${story.cultural_source}

## Contenido del Cuento
${story.content}

## Fecha de Creación
${story.created_at}
`;
  }

  validateStoryData(storyData) {
    super.validateStoryData(storyData);

    // 验证地区
    if (!this.isValidRegion(storyData.region)) {
      throw new Error(`Región no soportada: ${storyData.region}`);
    }

    // 验证故事类型
    if (!Object.keys(this.storyTypes).includes(storyData.type)) {
      throw new Error(`Tipo de cuento no soportado: ${storyData.type}`);
    }

    // 验证文化来源
    const country = this.getCountryFromRegion(storyData.region);
    const validSources = {
      spain: ['Spanish', 'Catalan', 'Basque', 'Galician'],
      mexico: ['Mexican', 'Maya', 'Aztec', 'Mixtec'],
      argentina: ['Argentine', 'Gaucho', 'Indigenous'],
      colombia: ['Colombian', 'Indigenous', 'Afro-Colombian']
    };

    if (!validSources[country].includes(storyData.cultural_source)) {
      throw new Error(`Fuente cultural no soportada para ${country}: ${storyData.cultural_source}`);
    }

    // 验证教育主题
    const validThemes = [
      'Valentía', 'Sabiduría', 'Honestidad', 'Respeto',
      'Paciencia', 'Cooperación', 'Creatividad', 'Curiosidad'
    ];
    const invalidThemes = storyData.educational_themes.filter(
      theme => !validThemes.includes(theme)
    );
    if (invalidThemes.length > 0) {
      throw new Error(`Temas educativos no soportados: ${invalidThemes.join(', ')}`);
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
    throw new Error(`Región no encontrada: ${region}`);
  }
}

module.exports = SpanishCollector; 