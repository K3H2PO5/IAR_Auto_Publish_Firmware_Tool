# 快速开始指南 / Quick Start Guide

## 5分钟快速上手 / 5-Minute Quick Start

### 1. 下载和安装 / Download and Install

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool

# 安装依赖 / Install dependencies
pip install -r requirements.txt
```

### 2. 首次运行 / First Run

```bash
python main.py
```

### 3. 基本配置 / Basic Configuration

1. 点击"设置"按钮 / Click "Settings" button
2. 配置IAR安装路径（如：`C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.3`）  
   Configure IAR installation path (e.g.: `C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.3`)
3. 设置项目路径（包含.ewp文件的目录）  
   Set project path (directory containing .ewp files)
4. 配置bin起始地址（如：`0x8000000`）  
   Configure bin start address (e.g.: `0x8000000`)
5. 选择配置文件（如：`main.c`）  
   Select configuration file (e.g.: `main.c`)
6. 点击"保存" / Click "Save"

### 4. 开始使用 / Start Using

1. 点击"开始编译" / Click "Start Compilation"
2. 工具会自动 / The tool will automatically：
   - 检查Git状态 / Check Git status
   - 递增版本号 / Increment version number
   - 编译项目 / Compile project
   - 修改二进制文件 / Modify binary files
   - 发布固件 / Publish firmware

## 常见问题 / FAQ

### Q: 提示"配置不完整"怎么办？  
Q: What to do when "Configuration incomplete" is prompted?
A: 请确保在设置中配置了所有必要参数：  
A: Please ensure all necessary parameters are configured in settings:
- IAR安装路径 / IAR installation path
- 项目路径 / Project path
- bin起始地址 / bin start address
- 配置文件 / Configuration file

### Q: 编译失败怎么办？  
Q: What to do when compilation fails?
A: 检查：  
A: Check:
- IAR路径是否正确 / Whether IAR path is correct
- 项目路径是否包含.ewp文件 / Whether project path contains .ewp files
- IAR是否已正确安装 / Whether IAR is properly installed

### Q: 如何切换语言？  
Q: How to switch language?
A: 在设置中选择语言选项，支持中文、繁体中文、英文。  
A: Select language option in settings, supports Chinese, Traditional Chinese, and English.

## 更多帮助 / More Help

- 查看完整文档：[README.md](README.md)  
  View complete documentation: [README.md](README.md)
- 报告问题：[GitHub Issues](https://github.com/yourusername/iar-firmware-publish-tool/issues)  
  Report issues: [GitHub Issues](https://github.com/yourusername/iar-firmware-publish-tool/issues)
- 贡献代码：[CONTRIBUTING.md](CONTRIBUTING.md)  
  Contribute code: [CONTRIBUTING.md](CONTRIBUTING.md)
