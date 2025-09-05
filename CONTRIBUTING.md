# 贡献指南 / Contributing Guide

感谢您对IAR固件发布工具的贡献！  
Thank you for contributing to the IAR Firmware Publish Tool!

## 如何贡献 / How to Contribute

### 报告问题 / Report Issues
1. 在GitHub Issues中搜索是否已有相同问题  
   Search GitHub Issues to see if the same issue already exists
2. 如果没有，请创建新的Issue  
   If not, please create a new Issue
3. 详细描述问题，包括：  
   Describe the issue in detail, including:
   - 操作系统版本 / Operating system version
   - Python版本 / Python version
   - 错误信息 / Error message
   - 复现步骤 / Reproduction steps

### 提交代码 / Submit Code
1. Fork本仓库 / Fork this repository
2. 创建功能分支：`git checkout -b feature/amazing-feature`  
   Create feature branch: `git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add some amazing feature'`  
   Commit changes: `git commit -m 'Add some amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`  
   Push branch: `git push origin feature/amazing-feature`
5. 创建Pull Request / Create Pull Request

## 开发环境设置 / Development Environment Setup

1. 克隆仓库 / Clone repository：
```bash
git clone https://github.com/yourusername/iar-firmware-publish-tool.git
cd iar-firmware-publish-tool
```

2. 创建虚拟环境 / Create virtual environment：
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. 安装依赖 / Install dependencies：
```bash
pip install -r requirements.txt
```

## 代码规范 / Code Standards

- 使用Python 3.7+语法 / Use Python 3.7+ syntax
- 遵循PEP 8代码风格 / Follow PEP 8 code style
- 添加适当的注释和文档字符串 / Add appropriate comments and docstrings
- 保持函数简洁，单一职责 / Keep functions concise with single responsibility

## 测试 / Testing

在提交代码前，请确保：  
Before submitting code, please ensure:
- 代码可以正常运行 / Code runs properly
- 没有语法错误 / No syntax errors
- 新功能不会破坏现有功能 / New features don't break existing functionality

## 提交信息规范 / Commit Message Standards

使用清晰的提交信息：  
Use clear commit messages:
- `feat:` 新功能 / New feature
- `fix:` 修复bug / Bug fix
- `docs:` 文档更新 / Documentation update
- `style:` 代码格式调整 / Code style adjustment
- `refactor:` 代码重构 / Code refactoring
- `test:` 测试相关 / Test related
- `chore:` 构建过程或辅助工具的变动 / Build process or auxiliary tool changes

示例 / Examples：
```
feat: add support for multiple IAR versions
fix: resolve language switching issue
docs: update README with installation instructions
```

## 许可证 / License

通过贡献代码，您同意您的贡献将在MIT许可证下发布。  
By contributing code, you agree that your contributions will be published under the MIT License.

详细许可证条款请查看 [LICENSE.md](LICENSE.md)  
For detailed license terms, please see [LICENSE.md](LICENSE.md)
