# 开发者指南 / Developer Guide

## 目录 / Table of Contents

1. [项目架构 / Project Architecture](#项目架构--project-architecture)
2. [开发环境设置 / Development Environment Setup](#开发环境设置--development-environment-setup)
3. [代码结构 / Code Structure](#代码结构--code-structure)
4. [核心模块 / Core Modules](#核心模块--core-modules)
5. [扩展开发 / Extension Development](#扩展开发--extension-development)
6. [测试指南 / Testing Guide](#测试指南--testing-guide)
7. [构建和部署 / Build and Deployment](#构建和部署--build-and-deployment)
8. [贡献指南 / Contributing Guide](#贡献指南--contributing-guide)

## 项目架构 / Project Architecture

### 整体架构 / Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    IAR固件发布工具                            │
│                 IAR Firmware Publish Tool                   │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼───────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   用户界面层    │ │  业务逻辑层  │ │   数据访问层   │
        │  UI Layer     │ │Business   │ │ Data Access │
        │               │ │Logic Layer│ │    Layer    │
        └───────────────┘ └───────────┘ └─────────────┘
                │               │               │
        ┌───────▼───────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   Tkinter     │ │ 版本管理   │ │   文件系统   │
        │   GUI         │ │Version    │ │ File System │
        │               │ │Management │ │             │
        └───────────────┘ └───────────┘ └─────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼───────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   Git集成     │ │ IAR编译   │ │  二进制修改  │
        │  Git Integration│ │IAR Build │ │Binary Modify│
        │               │ │           │ │             │
        └───────────────┘ └───────────┘ └─────────────┘
```

### 设计原则 / Design Principles

1. **模块化设计** / **Modular Design**：每个功能独立成模块
2. **松耦合** / **Loose Coupling**：模块间依赖最小化
3. **高内聚** / **High Cohesion**：相关功能集中管理
4. **可扩展性** / **Extensibility**：易于添加新功能
5. **可维护性** / **Maintainability**：代码清晰易懂

## 开发环境设置 / Development Environment Setup

### 系统要求 / System Requirements

- **操作系统** / **OS**：Windows 10/11
- **Python版本** / **Python Version**：3.7+
- **开发工具** / **Development Tools**：
  - Visual Studio Code / PyCharm
  - Git
  - IAR Embedded Workbench 8.x

### 环境配置 / Environment Configuration

#### 1. 克隆项目 / Clone Project
```bash
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool
```

#### 2. 创建虚拟环境 / Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

#### 3. 安装依赖 / Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. 安装开发依赖 / Install Development Dependencies
```bash
pip install flake8 pytest black isort
```

#### 5. 配置IDE / Configure IDE

**VS Code配置** / **VS Code Configuration**：
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"]
}
```

## 代码结构 / Code Structure

### 文件组织 / File Organization

```
├── main.py                    # 主程序入口
├── iar_builder.py            # IAR编译模块
├── binary_modifier.py        # 二进制文件修改模块
├── version_manager.py        # 固件版本管理模块
├── tool_version_manager.py   # 工具版本管理模块
├── git_manager.py           # Git操作模块
├── file_manager.py          # 文件管理模块
├── path_manager.py          # 路径管理模块
├── config_analyzer.py       # 配置分析模块
├── info_file_updater.py     # 信息文件更新模块
├── increment_tool_version.py # 工具版本递增脚本
├── build_exe.py             # 可执行文件构建脚本
├── config.json              # 默认配置文件
├── user_config.json         # 用户配置文件
├── user_config.example.json # 用户配置示例文件
├── requirements.txt         # Python依赖
└── docs/                    # 文档目录
    ├── README.md
    ├── USER_GUIDE.md
    ├── DEVELOPER_GUIDE.md
    ├── CHANGELOG.md
    └── CONTRIBUTING.md
```

### 命名规范 / Naming Conventions

#### 文件命名 / File Naming
- **Python文件** / **Python Files**：`snake_case.py`
- **配置文件** / **Config Files**：`snake_case.json`
- **文档文件** / **Documentation**：`UPPER_CASE.md`

#### 类命名 / Class Naming
- **类名** / **Class Names**：`PascalCase`
- **示例** / **Example**：`MCUAutoBuildApp`, `VersionManager`

#### 函数和变量命名 / Function and Variable Naming
- **函数名** / **Function Names**：`snake_case`
- **变量名** / **Variable Names**：`snake_case`
- **常量名** / **Constant Names**：`UPPER_CASE`

## 核心模块 / Core Modules

### 1. main.py - 主程序模块

#### 职责 / Responsibilities
- 用户界面管理 / User interface management
- 配置加载和保存 / Configuration loading and saving
- 工作流程协调 / Workflow coordination
- 对话框管理 / Dialog management

#### 关键类 / Key Classes
```python
class MCUAutoBuildApp:
    """主应用程序类"""
    def __init__(self):
        """初始化应用程序"""
    
    def start_build(self):
        """开始编译流程"""
    
    def show_commit_dialog(self):
        """显示Git提交对话框"""
    
    def _center_dialog(self, dialog):
        """居中显示对话框"""
```

### 2. version_manager.py - 固件版本管理

#### 职责 / Responsibilities
- 固件版本号解析和递增 / Firmware version parsing and increment
- 版本号格式验证 / Version format validation
- 配置文件更新 / Configuration file updating

#### 关键方法 / Key Methods
```python
class VersionManager:
    def parse_version(self, version_str: str) -> Optional[Tuple[int, int, int, int]]:
        """解析版本号字符串"""
    
    def increment_version(self, version_tuple: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """递增版本号"""
    
    def update_version_in_file(self, file_path: str, new_version: str) -> bool:
        """更新文件中的版本号"""
```

### 3. tool_version_manager.py - 工具版本管理

#### 职责 / Responsibilities
- 工具自身版本管理 / Tool's own version management
- 版本文件读写 / Version file read/write
- 单数字版本规则 / Single-digit version rules

#### 关键特性 / Key Features
- 版本部分限制在0-9 / Version parts limited to 0-9
- 正确的进位逻辑 / Correct carry-over logic
- 版本文件持久化 / Version file persistence

### 4. git_manager.py - Git操作模块

#### 职责 / Responsibilities
- Git状态检查 / Git status checking
- 提交信息获取 / Commit information retrieval
- 自动提交 / Automatic committing

#### 关键方法 / Key Methods
```python
class GitManager:
    def get_commit_info(self) -> Dict[str, str]:
        """获取Git提交信息"""
    
    def commit_changes(self, message: str) -> bool:
        """提交更改"""
    
    def is_git_repo(self) -> bool:
        """检查是否为Git仓库"""
```

### 5. binary_modifier.py - 二进制文件修改

#### 职责 / Responsibilities
- 二进制文件读取和修改 / Binary file reading and modification
- 版本信息注入 / Version information injection
- CRC校验计算 / CRC checksum calculation
- 内存地址计算和偏移管理 / Memory address calculation and offset management

#### 修改内容 / Modification Content
- **Git Commit ID**：7字节十六进制字符串（短哈希）
- **文件大小** / **File Size**：4字节小端序32位无符号整数
- **CRC校验值** / **CRC Checksum**：4字节小端序32位无符号整数

**注意** / **Note**：固件版本号通过修改源文件后重新编译来更新，不直接修改bin文件。

#### 内存布局 / Memory Layout
```
偏移量    字段          大小      数据类型        说明
+0       commit_id     7字节     字符串          Git Commit ID（短哈希）
+7       file_size     4字节     32位整数        文件大小（小端序）
+11      crc32         4字节     32位整数        CRC32校验值（小端序）
```

#### 关键方法 / Key Methods
```python
class BinaryModifier:
    def modify_binary_file(self, file_path: str, version_info: Dict) -> bool:
        """修改二进制文件，注入版本信息"""
    
    def calculate_crc32(self, data: bytes) -> int:
        """计算CRC32校验和"""
    
    def inject_version_info(self, file_path: str, version: str, commit_id: str) -> bool:
        """注入版本信息到指定内存地址"""
    
    def write_file_size(self, file_path: str, size: int, base_address: int) -> bool:
        """写入文件大小到指定地址"""
    
    def write_crc32(self, file_path: str, crc: int, base_address: int) -> bool:
        """写入CRC32校验值到指定地址"""
```

## 扩展开发 / Extension Development

### 添加新功能 / Adding New Features

#### 1. 创建新模块 / Create New Module

```python
# new_feature.py
import logging
from typing import Dict, Any

class NewFeature:
    """新功能模块"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process(self, data: Dict[str, Any]) -> bool:
        """处理功能逻辑"""
        try:
            # 功能实现
            self.logger.info("新功能处理完成")
            return True
        except Exception as e:
            self.logger.error(f"新功能处理失败: {e}")
            return False
```

#### 2. 集成到主程序 / Integrate into Main Program

```python
# main.py
from new_feature import NewFeature

class MCUAutoBuildApp:
    def __init__(self):
        # ... 现有初始化代码 ...
        self.new_feature = NewFeature()
    
    def start_build(self):
        # ... 现有代码 ...
        
        # 调用新功能
        if self.new_feature.process(data):
            self.logger.info("新功能执行成功")
        else:
            self.logger.error("新功能执行失败")
```

#### 3. 添加配置选项 / Add Configuration Options

```python
# config.json
{
    "new_feature_settings": {
        "enabled": true,
        "option1": "value1",
        "option2": "value2"
    }
}
```

### 添加新语言支持 / Adding New Language Support

#### 1. 定义语言文本 / Define Language Texts

```python
# main.py
LANGUAGES = {
    'zh_CN': {
        'new_feature_title': '新功能',
        'new_feature_description': '这是一个新功能'
    },
    'en_US': {
        'new_feature_title': 'New Feature',
        'new_feature_description': 'This is a new feature'
    },
    'ja_JP': {  # 新增日语支持
        'new_feature_title': '新機能',
        'new_feature_description': 'これは新しい機能です'
    }
}
```

#### 2. 更新UI元素 / Update UI Elements

```python
def update_ui_texts(self):
    """更新UI文本"""
    current_lang = self.languages[self.current_language]
    
    # 现有UI更新...
    
    # 新功能UI更新
    self.new_feature_label.config(text=current_lang['new_feature_title'])
```

## 测试指南 / Testing Guide

### 单元测试 / Unit Testing

#### 测试文件结构 / Test File Structure
```
tests/
├── test_version_manager.py
├── test_git_manager.py
├── test_binary_modifier.py
├── test_file_manager.py
└── test_integration.py
```

#### 示例测试 / Example Test

```python
# tests/test_version_manager.py
import unittest
from version_manager import VersionManager

class TestVersionManager(unittest.TestCase):
    def setUp(self):
        self.version_manager = VersionManager()
    
    def test_parse_version(self):
        """测试版本号解析"""
        version = "V1.0.0.1"
        result = self.version_manager.parse_version(version)
        self.assertEqual(result, (1, 0, 0, 1))
    
    def test_increment_version(self):
        """测试版本号递增"""
        version = (1, 0, 0, 1)
        result = self.version_manager.increment_version(version)
        self.assertEqual(result, (1, 0, 0, 2))

if __name__ == '__main__':
    unittest.main()
```

### 集成测试 / Integration Testing

```python
# tests/test_integration.py
import unittest
from main import MCUAutoBuildApp

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = MCUAutoBuildApp()
    
    def test_full_build_process(self):
        """测试完整编译流程"""
        # 设置测试配置
        self.app.project_path_var.set("test_project")
        self.app.iar_path_var.set("test_iar_path")
        
        # 执行编译流程
        result = self.app.start_build()
        
        # 验证结果
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

### 运行测试 / Running Tests

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_version_manager.py

# 运行测试并生成覆盖率报告
python -m pytest tests/ --cov=. --cov-report=html
```

## 构建和部署 / Build and Deployment

### 开发构建 / Development Build

```bash
# 运行开发版本
python main.py

# 代码格式化
black .
isort .

# 代码检查
flake8 .
```

### 生产构建 / Production Build

```bash
# 构建可执行文件
python build_exe.py

# 验证构建结果
ls -la release/
```

### 版本发布 / Version Release

#### 1. 更新版本号 / Update Version Number
```python
# main.py
__version__ = "1.0.3.0"  # 更新版本号
```

#### 2. 更新变更日志 / Update Changelog
```markdown
# CHANGELOG.md
## [1.0.3.0] - 2024-01-XX
### 新增 / Added
- 新功能描述
```

#### 3. 创建发布标签 / Create Release Tag
```bash
git tag -a v1.0.3.0 -m "Release version 1.0.3.0"
git push origin v1.0.3.0
```

#### 4. 构建发布版本 / Build Release Version
```bash
python build_exe.py
```

## 贡献指南 / Contributing Guide

### 开发流程 / Development Process

#### 1. Fork和克隆 / Fork and Clone
```bash
# Fork项目到自己的GitHub账户
# 克隆Fork的仓库
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool
```

#### 2. 创建功能分支 / Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### 3. 开发和测试 / Development and Testing
```bash
# 开发功能
# 编写测试
# 运行测试
python -m pytest tests/
```

#### 4. 提交更改 / Commit Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

#### 5. 推送和创建PR / Push and Create PR
```bash
git push origin feature/your-feature-name
# 在GitHub上创建Pull Request
```

### 代码规范 / Code Standards

#### 1. Python代码风格 / Python Code Style
- 遵循PEP 8规范 / Follow PEP 8 standards
- 使用Black进行代码格式化 / Use Black for code formatting
- 使用isort进行导入排序 / Use isort for import sorting

#### 2. 注释规范 / Comment Standards
```python
def example_function(param1: str, param2: int) -> bool:
    """
    示例函数说明
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        bool: 返回值说明
    
    Raises:
        ValueError: 异常说明
    """
    pass
```

#### 3. 提交信息规范 / Commit Message Standards
- `feat:` 新功能 / New feature
- `fix:` 修复bug / Bug fix
- `docs:` 文档更新 / Documentation update
- `style:` 代码格式调整 / Code style adjustment
- `refactor:` 代码重构 / Code refactoring
- `test:` 测试相关 / Test related
- `chore:` 构建过程或辅助工具的变动 / Build process or auxiliary tool changes

### 代码审查 / Code Review

#### 审查要点 / Review Points
1. **功能正确性** / **Functional Correctness**：功能是否按预期工作
2. **代码质量** / **Code Quality**：代码是否清晰、可维护
3. **性能影响** / **Performance Impact**：是否影响现有性能
4. **安全性** / **Security**：是否存在安全风险
5. **测试覆盖** / **Test Coverage**：是否有足够的测试覆盖

#### 审查流程 / Review Process
1. 自动检查 / Automatic checks（CI/CD）
2. 同行审查 / Peer review
3. 功能测试 / Functional testing
4. 集成测试 / Integration testing
5. 批准合并 / Approve and merge

---

## 联系和支持 / Contact and Support

### 开发团队 / Development Team
- **项目维护者** / **Project Maintainer**：[Your Name]
- **GitHub**：https://github.com/yourusername
- **邮箱** / **Email**：your.email@example.com

### 获取帮助 / Getting Help
1. **查看文档** / **Check Documentation**：阅读本文档和相关文档
2. **搜索Issues** / **Search Issues**：在GitHub Issues中搜索相关问题
3. **创建Issue** / **Create Issue**：如果问题未解决，创建新的Issue
4. **参与讨论** / **Join Discussion**：在GitHub Discussions中参与讨论

---

*最后更新 / Last Updated: 2024-01-XX*
