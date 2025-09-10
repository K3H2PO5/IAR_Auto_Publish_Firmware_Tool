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

## [1.0.3.8] - 2025-01-09

### 修复 / Fixed
- 修复ICF文件解析问题，正确解析IlinkIcfFile节点中的$PROJ_DIR$宏 / Fixed ICF file parsing issue, correctly parse $PROJ_DIR$ macro in IlinkIcfFile node
- 移除path_manager.py中硬编码的默认文件名，要求必须传入参数避免个人习惯影响 / Removed hardcoded default file names in path_manager.py, require parameters to avoid personal habits affecting others
- 修复配置文件优先级问题，确保用户界面指定的项目路径优先于user_config.json中的设置 / Fixed configuration priority issue, ensure UI-specified project path takes precedence over user_config.json settings
- 确保所有配置文件路径都使用相对路径，与主程序文件在同一目录 / Ensure all configuration file paths use relative paths, same directory as main program file
- 移除os.getcwd()的使用，避免打包exe时的工作目录问题 / Removed os.getcwd() usage to avoid working directory issues when packaging exe
- 移除ICF文件默认路径搜索逻辑，如果ewp文件中没有ICF文件引用则直接报错 / Removed ICF file default path search logic, directly report error if no ICF file reference found in .ewp file

### 改进 / Improved
- 优化代码结构，移除重复的配置文件 / Optimized code structure, removed duplicate configuration files
- 改进错误处理，项目路径无效时直接报错而不是使用当前工作目录 / Improved error handling, directly report error when project path is invalid instead of using current working directory

### 清理 / Cleanup
- 删除重复的config.example.json文件，保留config.json作为实际配置文件 / Removed duplicate config.example.json files, kept config.json as actual configuration file
- 修复build_exe.py中对已删除文件的引用，避免打包时出现文件找不到错误 / Fixed references to deleted files in build_exe.py to avoid file not found errors during packaging

## [1.0.3.7] - 2025-01-09

### 修复 / Fixed
- 修复IAR编译命令路径错误，使用正确的ewp文件路径而不是项目根目录 / Fixed IAR compilation command path error, use correct .ewp file path instead of project root directory
- 修复bin文件查找逻辑，严格匹配ewp文件名对应的bin文件，避免选择错误的备份文件 / Fixed bin file finding logic, strictly match .ewp filename corresponding bin file, avoid selecting wrong backup files
- 修复exe运行时配置文件路径问题，使用绝对路径确保配置文件正确加载 / Fixed exe runtime configuration file path issue, use absolute paths to ensure configuration files are loaded correctly
- 修复项目路径和ewp文件路径混淆问题，确保路径变量正确分离 / Fixed project path and .ewp file path confusion issue, ensure path variables are correctly separated
- 修复配置文件选择对话框文件类型筛选，添加对C++文件(.cpp, .cc, .cxx, .hpp, .hxx)的支持 / Fixed configuration file selection dialog file type filter, added support for C++ files (.cpp, .cc, .cxx, .hpp, .hxx)

### 改进 / Improved
- 改进编译命令构建逻辑，确保IAR编译器能正确识别项目文件 / Improved compilation command building logic, ensure IAR compiler can correctly identify project files
- 改进bin文件查找策略，移除"查找最新文件"逻辑，采用严格文件名匹配 / Improved bin file finding strategy, removed "find latest file" logic, adopted strict filename matching
- 改进错误处理，提供更详细的路径和文件存在性检查日志 / Improved error handling, provide more detailed path and file existence check logs
- 改进配置管理，确保exe和源码版本都能正确加载配置文件 / Improved configuration management, ensure both exe and source code versions can correctly load configuration files
- 优化配置结构，将版本变量名配置移至用户配置，统一使用firmware_version_keyword / Optimized configuration structure, moved version variable name configuration to user config, unified use of firmware_version_keyword
- 改进版本号匹配正则表达式，支持不同数量的空格和注释（单行注释//、多行注释/* */） / Improved version number matching regex, support different amounts of spaces and comments (single-line //, multi-line /* */)
- 修复路径管理中的硬编码问题，新增通用的find_info_file方法支持多种文件名和扩展名 / Fixed hardcoded paths in path management, added generic find_info_file method supporting multiple file names and extensions
- 优化方法命名，明确区分工具路径和项目路径，避免混淆 / Optimized method naming, clearly distinguish between tool paths and project paths to avoid confusion
- 修复PathManager初始化问题，移除os.getcwd()避免打包exe时的工作目录问题 / Fixed PathManager initialization issue, removed os.getcwd() to avoid working directory problems when packaging exe
- 优化代码结构，移除main.py中重复的_find_info_file方法，统一使用PathManager的find_info_file方法 / Optimized code structure, removed duplicate _find_info_file method in main.py, unified use of PathManager's find_info_file method
- 合并重复的文件查找方法，删除config_analyzer.py中的find_config_file方法，统一使用path_manager.find_info_file / Merged duplicate file search methods, removed find_config_file from config_analyzer.py, unified use of path_manager.find_info_file
- 优化文件搜索性能，在find_info_file方法中排除.git、.clion、.idea和cmake开头的目录，避免搜索构建系统生成的临时文件 / Optimized file search performance, excluded .git, .clion, .idea and cmake* directories in find_info_file method to avoid searching build system generated temporary files
- 改进错误信息显示，区分"未找到文件"和"找到多个文件"的情况，在找到多个文件时列出所有文件路径，提供更明确的错误提示 / Improved error message display, distinguish between "file not found" and "multiple files found" cases, list all file paths when multiple files are found, provide clearer error prompts
- 修复错误信息前后矛盾的问题，统一使用find_info_file_with_details方法，避免重复搜索和矛盾的错误提示 / Fixed contradictory error messages, unified use of find_info_file_with_details method to avoid duplicate searches and conflicting error prompts
- 优化弹窗错误信息显示，建议用户查看日志输出获取详细信息，避免弹窗信息过于冗长 / Optimized popup error message display, suggest users check log output for detailed information, avoid overly verbose popup messages

### 移除 / Removed
- 移除备份spec文件功能，简化PyInstaller构建过程 / Removed backup spec file functionality, simplified PyInstaller build process
- 移除_find_latest_bin_file方法，采用更可靠的严格匹配策略 / Removed _find_latest_bin_file method, adopted more reliable strict matching strategy

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