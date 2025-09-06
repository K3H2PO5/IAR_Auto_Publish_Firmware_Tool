# 变更日志 / Changelog

所有重要的项目变更都将记录在此文件中。  
All notable changes to this project will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，  
Format based on [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。  
This project adheres to [Semantic Versioning](https://semver.org/lang/zh-CN/).

## [未发布] / [Unreleased]

### 计划中 / Planned
- 支持更多IAR版本 / Support for more IAR versions
- 添加配置文件模板 / Add configuration file templates
- 改进错误处理 / Improve error handling

## [1.0.2.1] - 2024-01-XX

### 新增 / Added
- 添加Git提交对话框，支持自定义提交信息 / Added Git commit dialog with custom commit message support
- 添加Release Notes自动生成功能 / Added automatic Release Notes generation
- 添加远程发布功能，支持将固件发布到远程目录 / Added remote publishing feature, support publishing firmware to remote directories
- 添加工具版本管理，支持打包时自动递增版本号 / Added tool version management, support automatic version increment during packaging
- 添加多显示器支持，对话框自动居中到主窗口 / Added multi-monitor support, dialogs automatically center to main window
- 添加Enter键换行，Ctrl+Enter确认的提交对话框交互 / Added Enter for new line, Ctrl+Enter to confirm commit dialog interaction

### 改进 / Improved
- 优化Git集成，合并代码更改和版本更新为单个提交 / Optimized Git integration, merge code changes and version updates into single commit
- 改进路径管理，避免打包exe后的路径问题 / Improved path management, avoid path issues after packaging exe
- 优化用户界面，重命名"固件发布目录"为"本地发布目录" / Optimized user interface, renamed "Firmware Publish Directory" to "Local Publish Directory"
- 改进版本号递增逻辑，确保每个版本部分为单数字 / Improved version increment logic, ensure each version part is single digit

### 修复 / Fixed
- 修复配置保存问题，确保用户设置正确写入配置文件 / Fixed configuration save issue, ensure user settings are correctly written to config files
- 修复远程发布文件复制问题 / Fixed remote publishing file copying issues
- 修复对话框在多显示器环境下的显示问题 / Fixed dialog display issues in multi-monitor environments
- 修复工具版本号显示和递增逻辑 / Fixed tool version number display and increment logic

### 移除 / Removed
- 移除.out文件夹相关功能，简化工具结构 / Removed .out folder related functionality, simplified tool structure
- 移除build.bat文件，使用Python脚本进行打包 / Removed build.bat file, use Python script for packaging