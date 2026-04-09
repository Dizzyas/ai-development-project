# AI Development Project

这是一个包含多个AI和Python练习项目的集合，涵盖了机器学习、游戏开发、工具应用等多个领域。

## 📁 项目结构

```
ai-development-project/
├── 📱 TranslationApp/          # 单词翻译工具
│   └── 单词翻译工具.py         # 基于GUI的翻译应用
├── 🎮 贪吃蛇.py                # 经典贪吃蛇游戏
├── 🤖 ia开发入门.py            # 机器学习入门示例
├── 📚 AI学习指南_updated.md    # AI学习文档
├── 🛠️ .trae/                   # Trae IDE配置和工具
│   ├── boss/                   # BMAD自动化开发流水线
│   ├── mcp/                    # MCP工具集
│   └── skills/                 # 各种技能模块
└── logs/                       # 日志文件（已忽略）
```

## 🚀 项目介绍

### 1. 单词翻译工具 (TranslationApp)
一个基于Tkinter的桌面翻译应用，具有以下功能：
- 🎯 实时剪贴板监控，自动翻译复制的文本
- ⌨️ 全局快捷键支持
- 🎨 美观的OneDark Pro主题界面
- 📋 浮动窗口显示翻译结果

**运行方式：**
```bash
cd TranslationApp
python 单词翻译工具.py
```

### 2. 贪吃蛇游戏
使用Pygame开发的经典贪吃蛇游戏：
- 🎮 流畅的游戏体验
- 🏆 计分系统
- 🔄 游戏重置功能
- 🎨 简洁的界面设计

**运行方式：**
```bash
python 贪吃蛇.py
```

### 3. 机器学习入门 (ia开发入门.py)
线性回归模型的入门示例，包含：
- 📊 数据生成和可视化
- 🤖 模型训练和预测
- 📈 性能评估（MSE、R²评分）
- 🎨 结果可视化

**运行方式：**
```bash
python ia开发入门.py
```

## 📦 依赖安装

```bash
# 基础依赖
pip install numpy matplotlib scikit-learn

# 游戏依赖
pip install pygame

# 翻译工具依赖
pip install tkinter pyperclip pynput requests

# 或使用requirements.txt（如果提供）
pip install -r requirements.txt
```

## 🛠️ 开发工具

本项目使用 [Trae IDE](https://trae.ai/) 进行开发，包含以下工具集：

- **Boss Mode**: 自动化开发流水线
- **MCP Obsidian**: Obsidian笔记工具集成
- **UI/UX Pro Max**: UI设计智能助手
- **SportSciencePro**: 体育科学专家系统

## 🔒 安全说明

- 所有敏感信息（API密钥、密码等）都存储在 `.env` 文件中
- `.env` 和日志文件已在 `.gitignore` 中配置，不会被提交到GitHub
- 请勿将真实的API密钥提交到代码仓库

## 📝 学习资源

- [AI学习指南](AI学习指南_updated.md) - 详细的AI学习路径和资源

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目仅供学习和个人使用。

---

**作者**: Dizzyas  
**创建时间**: 2026年4月
