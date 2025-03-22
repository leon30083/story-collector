# 故事收集器 (Story Collector)

这是一个用于收集和管理不同语言故事的工具，可以将故事保存到 Notion 数据库中。目前支持中文故事的收集。

## 功能特点

- 支持多语言故事收集
- 自动生成故事 ID 和标题
- 将故事保存到 Notion 数据库
- 防止重复收集相同的故事
- 完整的日志记录
- 故事数据验证

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/story-collector.git
cd story-collector
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id
NODE_ENV=development
```

## 使用方法

1. 启动应用：
```bash
npm start
```

2. 开发模式（自动重启）：
```bash
npm run dev
```

## 故事数据格式

```javascript
{
  type: '民间故事',
  region: '华东',
  age_group: '3-6岁',
  educational_themes: ['勇气', '智慧'],
  length: '中篇',
  cultural_source: '浙江民间故事'
}
```

## 目录结构

```
StoryCollector/
├── src/
│   ├── collector/
│   │   ├── base.js
│   │   └── chinese.js
│   └── utils/
│       └── logger.js
├── logs/
│   ├── error.log
│   └── combined.log
├── package.json
└── README.md
```

## 开发说明

- 所有故事收集器都继承自 `BaseCollector` 类
- 每种语言的故事收集器需要实现特定的方法
- 使用 Winston 进行日志记录
- 使用 Jest 进行测试

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT 