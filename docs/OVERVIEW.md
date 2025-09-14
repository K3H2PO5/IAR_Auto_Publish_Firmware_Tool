# 功能概览 / Feature Overview

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![IAR](https://img.shields.io/badge/IAR-Embedded%20Workbench-orange.svg)](https://www.iar.com/iar-embedded-workbench/)

## ⚠️ 重要通知 / Important Notice

**本工具已停止更新** / **This tool is no longer maintained**

🚀 **新版本已发布** / **New version available**: [Embedded Firmware Manager](https://github.com/K3H2PO5/Embedded_Firmware_Manager)

**新版本特性** / **New version features**:
- ✅ 支持IAR和MDK双工具链 / Supports both IAR and MDK toolchains
- ✅ 模块化架构设计 / Modular architecture design
- ✅ 可扩展支持更多编译器 / Extensible support for more compilers
- ✅ 更好的错误处理和用户体验 / Better error handling and user experience

**迁移建议** / **Migration recommendation**:
- 如果您需要MDK支持或更多功能，建议迁移到新版本 / If you need MDK support or more features, we recommend migrating to the new version
- 如果仅使用IAR编译器，可以继续使用本工具 / If you only use IAR compiler, you can continue using this tool

---

一个用于IAR Embedded Workbench项目的自动化固件发布工具，支持版本管理、Git集成和二进制文件修改。

An automated firmware publishing tool for IAR Embedded Workbench projects, supporting version management, Git integration, and binary file modification.

## 功能概览 / Feature Overview

本工具提供了完整的IAR固件发布解决方案，从版本管理到最终发布的全流程自动化。

## 功能特性 / Features

#### 中文功能说明

- 📦 **版本管理** - 版本号管理，自动递增/手动设置版本号
- 🔄 **Git集成** - 自动提交版本更改，获取commit信息，支持自定义提交信息
- 🔧 **IAR项目编译** - 自动编译IAR Embedded Workbench项目，支持多配置项目
- 🛠️ **二进制修改** - 自动修改bin文件内容，在指定地址注入File Size、CRC、Hash和Git Commit信息
- 📝 **发布说明** - 自动生成和管理Release Notes
- 📁 **文件管理** - 自动重命名、复制和发布固件文件，支持本地和远程发布
- 🚀 **一键执行** - 全流程自动化，从Git检查到文件发布
- 🌐 **多语言支持** - 支持中文、繁体中文、英文界面

#### English Features

- 📦 **Version Management** - Version number management, automatically increment/manually set version numbers
- 🔄 **Git Integration** - Automatically commit version changes, retrieve commit information, support custom commit messages
- 🔧 **IAR Project Compilation** - Automatically compile IAR Embedded Workbench projects with multi-configuration support
- 🛠️ **Binary Modification** - Automatically modify bin file content, inject File Size, CRC, Hash and Git Commit information at specified addresses
- 📝 **Release Notes** - Automatically generate and manage Release Notes
- 📁 **File Management** - Automatically rename, copy and publish firmware files, supports local and remote publishing
- 🚀 **One-Click Execution** - Full workflow automation from Git check to file publishing
- 🌐 **Multi-Language Support** - Supports Chinese, Traditional Chinese, and English interfaces

## 系统要求 / System Requirements

- Windows 10/11
- Python 3.7+
- IAR Embedded Workbench 8.x
- Git

## 安装说明 / Installation

1. 克隆仓库 / Clone repository：
```bash
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool
```

2. 创建虚拟环境 / Create virtual environment：
```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖 / Install dependencies：
```bash
pip install -r requirements.txt
```

4. 运行程序 / Run the program：
```bash
python main.py
```

## 使用方法 / Usage

1. **首次配置 / Initial Configuration**：
   - 点击"设置"按钮 / Click "Settings" button
   - 配置IAR安装路径 / Configure IAR installation path
   - 设置项目路径 / Set project path
   - 配置bin起始地址 / Configure bin start address
   - 选择配置文件（如main.c）/ Select configuration file (e.g., main.c)

2. **编译发布 / Compile and Publish**：
   - 点击"开始编译"按钮 / Click "Start Compilation" button
   - 工具会自动 / The tool will automatically：
     - 检查Git状态 / Check Git status
     - 递增版本号 / Increment version number
     - 弹出Git提交对话框，输入更新信息 / Pop up Git commit dialog, input update information
     - 提交版本更改 / Commit version changes
     - 编译项目 / Compile project
     - 修改二进制文件 / Modify binary files
     - 生成Release Notes / Generate Release Notes
     - 发布固件到本地目录 / Publish firmware to local directory
     - 如果启用远程发布，复制到远程目录 / If remote publishing is enabled, copy to remote directory

## 配置说明 / Configuration

### 项目设置 / Project Settings
- **IAR安装路径**：IAR Embedded Workbench安装目录  
  **IAR Installation Path**: IAR Embedded Workbench installation directory
- **项目路径**：包含.ewp文件的IAR项目目录  
  **Project Path**: IAR project directory containing .ewp files
- **本地发布目录**：最终固件文件发布目录（项目内fw_publish文件夹）  
  **Local Publish Directory**: Final firmware file publishing directory (fw_publish folder in project)
- **远程发布目录**：可选的远程固件发布目录（绝对路径）  
  **Remote Publish Directory**: Optional remote firmware publishing directory (absolute path)
- **远程发布开关**：启用/禁用远程发布功能  
  **Remote Publish Switch**: Enable/disable remote publishing feature

### 二进制设置 / Binary Settings
- **bin起始地址**：固件在Flash中的起始地址（如0x8000000）  
  **Bin Start Address**: Firmware start address in Flash (e.g., 0x8000000)
- **配置文件**：包含版本号定义的文件（如main.c）  
  **Configuration File**: File containing version number definitions (e.g., main.c)

## 版本号格式 / Version Number Format

支持格式：`V主版本.次版本.修订版本.构建版本`  
Supported format: `VMajor.Minor.Revision.Build`

示例：`V1.0.0.1` → `V1.0.0.2`  
Example: `V1.0.0.1` → `V1.0.0.2`

## 二进制文件修改 / Binary File Modification

工具会自动在bin文件中注入以下信息：  
The tool automatically injects the following information into bin files:

### 修改内容 / Modification Content
- **Git Commit ID**：当前Git提交的短哈希值（7字符）
- **文件大小** / **File Size**：bin文件的实际字节大小（4字节，小端序）
- **CRC校验值** / **CRC Checksum**：整个bin文件的CRC32校验值（4字节，小端序）

**注意** / **Note**：固件版本号通过修改源文件后重新编译来更新，不直接修改bin文件。

### 修改位置 / Modification Locations
- **Commit ID地址** / **Commit ID Address**：通过`#pragma location`在C代码中指定的内存地址
- **文件大小地址** / **File Size Address**：Commit ID地址 + 7字节偏移
- **CRC校验地址** / **CRC Address**：文件大小地址 + 4字节偏移

### 数据格式 / Data Format
- **Commit ID**：7字符十六进制字符串，如"a1b2c3d"
- **文件大小** / **File Size**：32位无符号整数，小端序
- **CRC校验** / **CRC**：32位无符号整数，小端序

## 发布说明管理 / Release Notes Management

工具会自动生成和管理Release Notes：  
The tool automatically generates and manages Release Notes:
- 自动创建`RELEASE_NOTES.md`文件 / Automatically creates `RELEASE_NOTES.md` file
- 记录每次发布的版本信息 / Records version information for each release
- 智能格式化用户输入的更新信息 / Intelligently formats user-input update information
- 自动换行处理（按分号或句号分割）/ Automatic line wrapping (split by semicolons or periods)

## 远程发布功能 / Remote Publishing Feature

支持将固件发布到远程目录：  
Supports publishing firmware to remote directories:
- 可配置的远程发布目录 / Configurable remote publish directory
- 按项目名称+分支名称创建子目录 / Create subdirectories by project name + branch name
- 复制重命名后的bin文件和Release Notes / Copy renamed bin files and Release Notes
- 可选的启用/禁用开关 / Optional enable/disable switch

## 多语言支持 / Multi-language Support

- 简体中文 (zh_CN) / Simplified Chinese (zh_CN)
- 繁体中文 (zh_TW) / Traditional Chinese (zh_TW)
- English (en_US)

## 开发说明 / Development

### 项目结构 / Project Structure
```
├── main.py                 # 主程序入口 / Main program entry
├── iar_builder.py          # IAR编译模块 / IAR compilation module
├── binary_modifier.py      # 二进制文件修改模块 / Binary file modification module
├── version_manager.py      # 版本管理模块 / Version management module
├── git_manager.py          # Git操作模块 / Git operations module
├── file_manager.py         # 文件管理模块 / File management module
├── path_manager.py         # 路径管理模块 / Path management module
├── config_analyzer.py      # 配置分析模块 / Configuration analysis module
├── info_file_updater.py    # 信息文件更新模块 / info file update module
├── tool_version_manager.py # 工具版本管理模块 / Tool version management module
├── config.json            # 默认配置文件 / Default configuration file
├── user_config.json       # 用户配置文件 / User configuration file
└── requirements.txt       # Python依赖 / Python dependencies
```

### 构建可执行文件 / Build Executable

```bash
python build_exe.py
```

这将自动：  
This will automatically:
- 递增工具版本号 / Increment tool version number
- 创建PyInstaller spec文件 / Create PyInstaller spec file
- 构建可执行文件 / Build executable file
- 输出到`release/`目录 / Output to `release/` directory

生成的文件：  
Generated files:
- `IAR_Firmware_Publish_Tool.spec` - PyInstaller配置文件 / PyInstaller configuration file
- `IAR_Firmware_Publish_Tool_v{version}.exe` - 可执行文件 / Executable file

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交Issue和Pull Request！  
Welcome to submit Issues and Pull Requests!

## 更新日志 / Changelog

### v1.0.4.2
- 修复语言设置持久化问题 / Fixed language setting persistence issue
- 改进配置加载机制 / Improved configuration loading mechanism
- 优化用户界面体验 / Optimized user interface experience

## 联系方式 / Contact

如有问题，请提交Issue或联系开发者。  
If you have any questions, please submit an Issue or contact the developer.