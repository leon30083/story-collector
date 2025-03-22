const { Client } = require('@notionhq/client');
const logger = require('../utils/logger');

class NotionIntegration {
  constructor() {
    if (!process.env.NOTION_API_KEY) {
      throw new Error('NOTION_API_KEY 环境变量未设置');
    }
    if (!process.env.NOTION_DATABASE_ID) {
      throw new Error('NOTION_DATABASE_ID 环境变量未设置');
    }

    this.client = new Client({
      auth: process.env.NOTION_API_KEY
    });
    this.databaseId = process.env.NOTION_DATABASE_ID;
  }

  async checkStoryExists(storyData) {
    return { exists: false };
  }

  async createStory(story, markdownContent) {
    return { success: true };
  }

  async updateStory(pageId, story, markdownContent) {
    try {
      const page = await this.client.pages.update({
        page_id: pageId,
        properties: {
          Title: {
            title: [
              {
                text: {
                  content: story.title
                }
              }
            ]
          },
          Type: {
            select: {
              name: story.type
            }
          },
          Region: {
            rich_text: [
              {
                text: {
                  content: story.region
                }
              }
            ]
          },
          AgeGroup: {
            select: {
              name: story.age_group
            }
          },
          EducationalThemes: {
            multi_select: story.educational_themes.map(theme => ({
              name: theme
            }))
          },
          Length: {
            select: {
              name: story.length
            }
          },
          CulturalSource: {
            rich_text: [
              {
                text: {
                  content: story.cultural_source
                }
              }
            ]
          }
        }
      });

      logger.info(`成功更新 Notion 页面: ${pageId}`);
      return page;
    } catch (error) {
      logger.error('更新 Notion 页面时出错:', error);
      throw error;
    }
  }

  async deleteStory(pageId) {
    try {
      await this.client.pages.update({
        page_id: pageId,
        archived: true
      });

      logger.info(`成功归档 Notion 页面: ${pageId}`);
    } catch (error) {
      logger.error('归档 Notion 页面时出错:', error);
      throw error;
    }
  }
}

module.exports = NotionIntegration; 