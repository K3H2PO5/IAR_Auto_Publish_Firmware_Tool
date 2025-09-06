#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具版本管理模块
负责工具本身的版本号管理，包括自动修改.py文件版本号
"""

import os
import sys
import re
import logging
from typing import Optional, Tuple
from datetime import datetime


class ToolVersionManager:
    """工具版本管理器"""
    
    def __init__(self, tool_file_path: str = None):
        """
        初始化工具版本管理器
        
        Args:
            tool_file_path: 工具主文件路径，默认为main.py
        """
        self.logger = logging.getLogger(__name__)
        
        # 确定工具文件路径
        if tool_file_path:
            self.tool_file_path = tool_file_path
        else:
            # 默认使用main.py
            self.tool_file_path = os.path.join(os.path.dirname(__file__), 'main.py')
        
        # 版本号存储文件（用于exe打包后的版本管理）
        if hasattr(sys, 'frozen') and sys.frozen:
            # 如果是打包后的exe，使用exe所在目录
            base_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境，使用脚本所在目录
            base_path = os.path.dirname(__file__)
        
        # 设置版本文件路径
        self.version_file_path = os.path.join(base_path, 'tool_version.txt')
        
        # 版本号模式
        self.version_pattern = r'__version__\s*=\s*["\']([^"\']+)["\']'
        self.version_format = '__version__ = "{}"'
        
        self.logger.info(f"工具版本管理器初始化，文件路径: {self.tool_file_path}")
        self.logger.info(f"是否为exe环境: {hasattr(sys, 'frozen') and sys.frozen}")
        self.logger.info(f"当前工作目录: {os.getcwd()}")
    
    def get_current_version(self) -> Optional[str]:
        """
        获取当前工具版本号
        
        Returns:
            str: 当前版本号，如果未找到返回None
        """
        try:
            self.logger.info(f"开始获取工具版本号...")
            self.logger.info(f"main.py路径: {self.tool_file_path}")
            self.logger.info(f"main.py存在: {os.path.exists(self.tool_file_path)}")
            
            # 如果是exe环境，尝试从版本文件读取
            if hasattr(sys, 'frozen') and sys.frozen:
                self.logger.info("检测到exe环境，尝试从版本文件读取版本号")
                if os.path.exists(self.version_file_path):
                    with open(self.version_file_path, 'r', encoding='utf-8') as f:
                        version = f.read().strip()
                    if version:
                        self.logger.info(f"从版本文件读取工具版本: {version}")
                        return version
                else:
                    self.logger.warning("版本文件不存在，使用硬编码版本号")
                    # 在exe环境中使用硬编码的版本号
                    hardcoded_version = "1.0.3.1"  # 这个版本号需要在打包时更新
                    self.logger.info(f"使用硬编码版本号: {hardcoded_version}")
                    return hardcoded_version
            
            # 开发环境：直接从main.py读取版本号
            if os.path.exists(self.tool_file_path):
                with open(self.tool_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找版本号
                match = re.search(self.version_pattern, content)
                if match:
                    version = match.group(1)
                    self.logger.info(f"从main.py读取工具版本: {version}")
                    return version
                else:
                    self.logger.warning("main.py中未找到版本号定义")
            else:
                self.logger.warning("main.py文件不存在")
            
            # 如果找不到，使用默认版本
            default_version = "1.0.0.0"
            self.logger.warning(f"未找到工具版本号，使用默认版本: {default_version}")
            return default_version
                
        except Exception as e:
            self.logger.error(f"获取工具版本号失败: {e}")
            # 即使出错也返回默认版本
            default_version = "1.0.0.0"
            return default_version
    
    
    def parse_version(self, version_str: str) -> Optional[Tuple[int, int, int, int]]:
        """
        解析版本字符串
        注意：每个版本号部分都限制在0-9之间
        
        Args:
            version_str: 版本字符串，如 "1.0.0.0"
            
        Returns:
            Tuple[int, int, int, int]: 版本号元组 (major, minor, patch, build)
        """
        try:
            # 移除可能的空白字符
            version_str = version_str.strip()
            
            # 使用正则表达式匹配版本号
            pattern = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
            match = re.match(pattern, version_str)
            if not match:
                self.logger.warning(f"无法解析工具版本号: {version_str}")
                return None
            
            # 提取版本号部分
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            build = int(match.group(4))
            
            # 确保版本号各部分都在0-9范围内
            major = min(major, 9)
            minor = min(minor, 9)
            patch = min(patch, 9)
            build = min(build, 9)
            
            self.logger.info(f"解析工具版本号: {version_str} -> ({major}, {minor}, {patch}, {build})")
            return (major, minor, patch, build)
            
        except Exception as e:
            self.logger.error(f"解析工具版本号失败: {e}")
            return None
    
    def format_version(self, major: int, minor: int, patch: int, build: int) -> str:
        """
        格式化版本号为字符串
        
        Args:
            major: 主版本号
            minor: 次版本号
            patch: 补丁版本号
            build: 构建版本号
            
        Returns:
            str: 格式化的版本字符串
        """
        return f"{major}.{minor}.{patch}.{build}"
    
    def increment_version(self, version_tuple: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """
        递增版本号（末位加一，溢出则进位）
        注意：每个版本号部分都限制在0-9之间
        
        Args:
            version_tuple: 当前版本号元组
            
        Returns:
            Tuple[int, int, int, int]: 递增后的版本号元组
        """
        major, minor, patch, build = version_tuple
        
        # 确保版本号各部分都在0-9范围内
        major = min(major, 9)
        minor = min(minor, 9)
        patch = min(patch, 9)
        build = min(build, 9)
        
        # 从末位开始递增
        build += 1
        
        # 检查是否需要进位
        if build > 9:
            build = 0
            patch += 1
            
            if patch > 9:
                patch = 0
                minor += 1
                
                if minor > 9:
                    minor = 0
                    major += 1
                    
                    if major > 9:
                        # 如果主版本号也超过9，重置为1
                        major = 1
        
        new_version = (major, minor, patch, build)
        self.logger.info(f"工具版本号递增: {self.format_version(*version_tuple)} -> {self.format_version(*new_version)}")
        return new_version
    
    def update_version(self, new_version: str) -> bool:
        """
        更新工具版本号
        
        Args:
            new_version: 新版本号
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 直接更新main.py文件
            if os.path.exists(self.tool_file_path):
                try:
                    # 读取文件内容
                    with open(self.tool_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 查找并替换版本号
                    if re.search(self.version_pattern, content):
                        # 替换现有版本号
                        new_content = re.sub(self.version_pattern, self.version_format.format(new_version), content)
                        
                        # 写回文件
                        with open(self.tool_file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        self.logger.info(f"main.py版本号已更新为: {new_version}")
                        return True
                    else:
                        self.logger.warning("main.py中未找到版本号定义")
                        return False
                except Exception as e:
                    self.logger.error(f"更新main.py版本号失败: {e}")
                    return False
            else:
                self.logger.warning("main.py文件不存在，无法更新版本号")
                return False
            
        except Exception as e:
            self.logger.error(f"更新工具版本号失败: {e}")
            return False
    
    def auto_increment_version(self) -> Optional[str]:
        """
        自动递增工具版本号
        
        Returns:
            str: 新的版本号，如果失败返回None
        """
        try:
            # 获取当前版本
            current_version = self.get_current_version()
            if not current_version:
                # 如果没有版本号，使用默认版本
                current_version = "1.0.0.0"
                self.logger.info("未找到版本号，使用默认版本: 1.0.0.0")
            
            # 解析版本号
            version_tuple = self.parse_version(current_version)
            if not version_tuple:
                self.logger.error("无法解析当前版本号")
                return None
            
            # 递增版本号
            new_version_tuple = self.increment_version(version_tuple)
            new_version = self.format_version(*new_version_tuple)
            
            # 更新版本号
            if self.update_version(new_version):
                return new_version
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"自动递增工具版本号失败: {e}")
            return None
    
    def get_version_info(self) -> dict:
        """
        获取版本信息
        
        Returns:
            dict: 版本信息字典
        """
        try:
            current_version = self.get_current_version()
            if not current_version:
                return {
                    'version': '未知',
                    'version_tuple': None,
                    'file_path': self.tool_file_path,
                    'version_file_path': self.version_file_path,
                    'file_exists': os.path.exists(self.tool_file_path),
                    'version_file_exists': os.path.exists(self.version_file_path),
                    'last_modified': None
                }
            
            version_tuple = self.parse_version(current_version)
            
            # 获取文件修改时间
            last_modified = None
            if os.path.exists(self.version_file_path):
                stat = os.stat(self.version_file_path)
                last_modified = datetime.fromtimestamp(stat.st_mtime)
            elif os.path.exists(self.tool_file_path):
                stat = os.stat(self.tool_file_path)
                last_modified = datetime.fromtimestamp(stat.st_mtime)
            
            return {
                'version': current_version,
                'version_tuple': version_tuple,
                'file_path': self.tool_file_path,
                'version_file_path': self.version_file_path,
                'file_exists': os.path.exists(self.tool_file_path),
                'version_file_exists': os.path.exists(self.version_file_path),
                'last_modified': last_modified
            }
            
        except Exception as e:
            self.logger.error(f"获取版本信息失败: {e}")
            return {
                'version': '错误',
                'version_tuple': None,
                'file_path': self.tool_file_path,
                'version_file_path': self.version_file_path,
                'file_exists': os.path.exists(self.tool_file_path),
                'version_file_exists': os.path.exists(self.version_file_path),
                'last_modified': None,
                'error': str(e)
            }


def test_tool_version_manager():
    """测试工具版本管理器功能"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    manager = ToolVersionManager()
    
    print("工具版本管理器测试")
    print(f"工具文件路径: {manager.tool_file_path}")
    
    # 获取当前版本
    current_version = manager.get_current_version()
    print(f"当前版本: {current_version}")
    
    # 获取版本信息
    version_info = manager.get_version_info()
    print(f"版本信息: {version_info}")
    
    # 测试版本解析
    if current_version:
        parsed = manager.parse_version(current_version)
        if parsed:
            incremented = manager.increment_version(parsed)
            print(f"版本递增: {current_version} -> {manager.format_version(*incremented)}")


if __name__ == "__main__":
    test_tool_version_manager()
