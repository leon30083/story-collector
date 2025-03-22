# Story Collector

一个多语言故事收集系统，支持从不同地区收集故事并保存到 Notion 数据库。

## 功能特性

- 支持多语言故事收集：
  - 中文故事（中国、台湾、香港）
  - 英语故事（美国、英国、加拿大、澳大利亚）
  - 日语故事（日本）
  - 西班牙语故事（西班牙、墨西哥、阿根廷）
  - 阿拉伯语故事（埃及、沙特阿拉伯、阿联酋）
  - 印地语故事（印度）
- 自动故事去重
- Notion 数据库集成
- 完整的错误处理
- 详细的日志记录
- 全面的测试覆盖

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/leon30083/story-collector.git
cd story-collector
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```env
NOTION_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_database_id
```

## 使用方法

1. 运行测试：
```bash
npm test
```

2. 收集故事：
```bash
node src/index.js
```

## 项目结构

```
StoryCollector/
├── src/
│   ├── collector/      # 各语言故事收集器
│   ├── integration/    # 第三方集成（如 Notion）
│   ├── utils/         # 工具函数
│   └── index.js       # 主入口文件
├── tests/             # 测试文件
├── data/              # 数据文件
├── config/            # 配置文件
└── docs/              # 文档
```

## 开发

1. 安装开发依赖：
```bash
npm install --save-dev
```

2. 运行测试：
```bash
npm test
```

3. 检查代码覆盖率：
```bash
npm run test:coverage
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

- leon30083

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md) 