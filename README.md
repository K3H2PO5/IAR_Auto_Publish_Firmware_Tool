# IAR固件发布工具 / IAR Firmware Publish Tool

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](docs/LICENSE.md)
[![Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![IAR](https://img.shields.io/badge/IAR-Embedded%20Workbench-orange.svg)](https://www.iar.com/iar-embedded-workbench/)

一个用于IAR Embedded Workbench项目的自动化固件发布工具，支持版本管理、Git集成和二进制文件修改。

An automated firmware publishing tool for IAR Embedded Workbench projects, supporting version management, Git integration, and binary file modification.

## 界面预览 / Interface Preview

### 主界面 / Main Interface
![主界面](./docs/screenshot/main%20ui.png)

### 设置界面 / Settings Interface
![设置界面](./docs/screenshot/setting.png)

### 编译过程 / Compilation Process
![编译过程](./docs/screenshot/compile.png)

### 二进制文件修改 / Binary File Modification
![二进制文件修改](./docs/screenshot/bin%20file.png)

### 发布说明 / Release Notes
![发布说明](./docs/screenshot/release%20note.png)

## 快速开始 / Quick Start

### 安装和运行 / Installation and Running

1. **克隆仓库** / **Clone repository**：
```bash
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool
```

2. **安装依赖** / **Install dependencies**：
```bash
pip install -r requirements.txt
```

3. **运行程序** / **Run the program**：
```bash
python main.py
```

### 主要功能 / Main Features

- 🔧 **IAR项目编译** - 自动编译IAR Embedded Workbench项目
- 📦 **版本管理** - 自动递增固件版本号
- 🔄 **Git集成** - 自动提交版本更改，获取commit信息
- 🛠️ **二进制修改** - 自动修改bin文件，注入版本和Git信息
- 🌐 **多语言支持** - 支持中文、繁体中文、英文界面
- 📁 **文件管理** - 自动复制和发布固件文件
- 📝 **发布说明** - 自动生成和管理Release Notes

## 文档 / Documentation

- 📖 [功能概览](./docs/OVERVIEW.md) - 完整的功能说明和界面展示
- 🚀 [快速开始指南](./docs/QUICKSTART.md) - 5分钟快速上手
- 👤 [用户指南](./docs/USER_GUIDE.md) - 详细的使用说明和最佳实践
- 👨‍💻 [开发者指南](./docs/DEVELOPER_GUIDE.md) - 开发环境设置和代码贡献
- 📋 [更新日志](./docs/CHANGELOG.md) - 版本更新历史
- 🤝 [贡献指南](./docs/CONTRIBUTING.md) - 如何参与项目开发

## 系统要求 / System Requirements

- Windows 10/11
- Python 3.7+
- IAR Embedded Workbench 8.x
- Git

## 许可证 / License

本项目采用 MIT 许可证 - 查看 [LICENSE](./docs/LICENSE.md) 文件了解详情。

This project is licensed under the MIT License - see the [LICENSE](./docs/LICENSE.md) file for details.

## 联系方式 / Contact

如有问题，请提交Issue或联系开发者。

If you have any questions, please submit an Issue or contact the developer.
