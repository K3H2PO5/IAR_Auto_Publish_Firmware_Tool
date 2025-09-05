# IAR固件发布工具 / IAR Firmware Publish Tool

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![IAR](https://img.shields.io/badge/IAR-Embedded%20Workbench-orange.svg)](https://www.iar.com/iar-embedded-workbench/)

一个用于IAR Embedded Workbench项目的自动化固件发布工具，支持版本管理、Git集成和二进制文件修改。

An automated firmware publishing tool for IAR Embedded Workbench projects, supporting version management, Git integration, and binary file modification.

## 功能特性 / Features

- 🔧 **IAR项目编译** - 自动编译IAR Embedded Workbench项目  
  **IAR Project Compilation** - Automatically compile IAR Embedded Workbench projects
- 📦 **版本管理** - 自动递增固件版本号  
  **Version Management** - Automatically increment firmware version numbers
- 🔄 **Git集成** - 自动提交版本更改，获取commit信息  
  **Git Integration** - Automatically commit version changes and retrieve commit information
- 🛠️ **二进制修改** - 自动修改bin文件，注入版本和Git信息  
  **Binary Modification** - Automatically modify bin files, inject version and Git information
- 🌐 **多语言支持** - 支持中文、繁体中文、英文界面  
  **Multi-language Support** - Supports Chinese, Traditional Chinese, and English interfaces
- 📁 **文件管理** - 自动复制和发布固件文件  
  **File Management** - Automatically copy and publish firmware files
- ⚙️ **配置管理** - 用户配置持久化保存  
  **Configuration Management** - Persistent user configuration storage

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
     - 提交版本更改 / Commit version changes
     - 编译项目 / Compile project
     - 修改二进制文件 / Modify binary files
     - 发布固件 / Publish firmware

## 配置说明 / Configuration

### 项目设置 / Project Settings
- **IAR安装路径**：IAR Embedded Workbench安装目录  
  **IAR Installation Path**: IAR Embedded Workbench installation directory
- **项目路径**：包含.ewp文件的IAR项目目录  
  **Project Path**: IAR project directory containing .ewp files
- **输出目录**：编译输出文件保存目录  
  **Output Directory**: Directory for saving compiled output files
- **固件发布目录**：最终固件文件发布目录  
  **Firmware Publish Directory**: Final firmware file publishing directory

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
- 固件版本号 / Firmware version number
- Git commit ID
- 文件大小 / File size
- CRC校验和 / CRC checksum

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

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交Issue和Pull Request！  
Welcome to submit Issues and Pull Requests!

## 更新日志 / Changelog

### v1.0.3.0
- 修复语言设置持久化问题 / Fixed language setting persistence issue
- 改进配置加载机制 / Improved configuration loading mechanism
- 优化用户界面体验 / Optimized user interface experience

## 联系方式 / Contact

如有问题，请提交Issue或联系开发者。  
If you have any questions, please submit an Issue or contact the developer.