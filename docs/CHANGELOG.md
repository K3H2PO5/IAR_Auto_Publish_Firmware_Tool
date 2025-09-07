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

## [1.0.3.6] - 2025-01-XX

### 新增 / Added
- 添加.out文件发布功能，支持同时发布.bin和.out文件到本地和远程目录 / Added .out file publishing feature, support publishing both .bin and .out files to local and remote directories
- 优化设置页面布局，调整复选框间距和对齐方式 / Optimized settings page layout, adjusted checkbox spacing and alignment

### 改进 / Improved
- 改进文件发布逻辑，确保.out文件与.bin文件使用相同的命名规则 / Improved file publishing logic, ensure .out files use the same naming convention as .bin files
- 优化远程发布功能，支持.out文件的远程发布 / Optimized remote publishing feature, support .out file remote publishing
- 改进设置页面用户体验，相关复选框布局更加美观 / Improved settings page user experience, related checkboxes layout more aesthetically pleasing

### 修复 / Fixed
- 修复.out文件查找逻辑，确保能正确找到对应的.out文件 / Fixed .out file finding logic, ensure correct .out file can be found
- 修复设置页面复选框对齐问题 / Fixed settings page checkbox alignment issues

## [1.0.3.5] - 2025-01-XX

### 新增 / Added
- 添加文件名时间戳控制选项，用户可选择是否在文件名中添加时间戳 / Added filename timestamp control option, users can choose whether to add timestamp to filename
- 优化设置页面布局，将相关复选框放在同一行以节省空间 / Optimized settings page layout, place related checkboxes on the same row to save space

### 改进 / Improved
- 改进文件发布逻辑，支持可选的文件名时间戳功能 / Improved file publishing logic, support optional filename timestamp feature
- 改进设置页面用户体验，相关功能选项布局更加紧凑 / Improved settings page user experience, related function options layout more compact

### 修复 / Fixed
- 修复配置合并逻辑，确保新配置项能正确添加到现有用户配置中 / Fixed configuration merge logic, ensure new configuration items can be correctly added to existing user configurations

## [1.0.3.4] - 2025-01-XX

### 新增 / Added
- 添加哈希校验和功能，支持__hash_value变量 / Added hash checksum functionality, support for __hash_value variable
- 添加Flash起始地址显示，在主界面显示当前配置的Flash起始地址 / Added Flash start address display on main interface
- 添加环境诊断功能，帮助排查打包exe运行问题 / Added environment diagnosis feature to help troubleshoot packaged exe issues
- 添加详细的路径搜索和验证日志 / Added detailed path search and validation logging

### 改进 / Improved
- 优化主界面布局，调整信息显示顺序：IAR路径、Flash起始地址、Git状态、固件版本 / Optimized main interface layout, adjusted information display order: IAR path, Flash start address, Git status, firmware version
- 改进IAR路径查找逻辑，确保始终返回有效的exe文件路径 / Improved IAR path finding logic, ensure always returns valid exe file path
- 优化subprocess调用策略，支持多种调用方式以提高兼容性 / Optimized subprocess calling strategy, support multiple calling methods for better compatibility
- 改进错误处理，提供更详细的错误信息和诊断日志 / Improved error handling, provide more detailed error messages and diagnostic logs

### 修复 / Fixed
- 修复打包exe时出现的[WinError 5] 拒绝访问权限错误 / Fixed [WinError 5] Access Denied error when running packaged exe
- 修复IAR路径解析问题，避免返回目录路径而不是exe文件路径 / Fixed IAR path parsing issue, avoid returning directory path instead of exe file path
- 修复subprocess调用时路径包含空格的问题 / Fixed subprocess calling issue with paths containing spaces
- 修复hash_value_offset未设置的问题，支持uint8_t数组类型 / Fixed hash_value_offset not set issue, support uint8_t array type

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