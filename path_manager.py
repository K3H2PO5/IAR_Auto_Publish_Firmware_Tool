#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径管理模块
负责路径验证、自动查找和路径解析
"""

import os
import glob
import logging
from typing import Optional, List, Tuple
from pathlib import Path


class PathManager:
    """路径管理器"""
    
    def __init__(self, project_path: str = None):
        """
        初始化路径管理器
        
        Args:
            project_path: 项目根目录路径
        """
        self.project_path = os.path.abspath(project_path) if project_path else os.getcwd()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"项目根目录: {self.project_path}")
    
    def find_iar_workspace(self, pattern: str = "*.eww") -> Optional[str]:
        """
        查找IAR工作区文件
        
        Args:
            pattern: 文件匹配模式
            
        Returns:
            str: 找到的工作区文件路径，未找到返回None
        """
        try:
            # 在项目目录及其子目录中查找
            search_paths = [
                self.project_path,
                os.path.join(self.project_path, "EWARM"),
                os.path.join(self.project_path, "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "..", "EWARM")
            ]
            
            for search_path in search_paths:
                if os.path.exists(search_path):
                    # 递归查找匹配的文件
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if file.lower().endswith('.eww'):
                                file_path = os.path.join(root, file)
                                self.logger.info(f"找到IAR工作区文件: {file_path}")
                                return file_path
            
            self.logger.warning("未找到IAR工作区文件")
            return None
            
        except Exception as e:
            self.logger.error(f"查找IAR工作区文件失败: {e}")
            return None
    
    def find_iar_project(self, pattern: str = "*.ewp") -> Optional[str]:
        """
        查找IAR项目文件
        
        Args:
            pattern: 文件匹配模式
            
        Returns:
            str: 找到的项目文件路径，未找到返回None
        """
        try:
            # 在项目目录及其子目录中查找
            search_paths = [
                self.project_path,
                os.path.join(self.project_path, "EWARM"),
                os.path.join(self.project_path, "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "..", "EWARM")
            ]
            
            for search_path in search_paths:
                if os.path.exists(search_path):
                    # 递归查找匹配的文件
                    for root, dirs, files in os.walk(search_path):
                        for file in files:
                            if file.lower().endswith('.ewp'):
                                file_path = os.path.join(root, file)
                                self.logger.info(f"找到IAR项目文件: {file_path}")
                                return file_path
            
            self.logger.warning("未找到IAR项目文件")
            return None
            
        except Exception as e:
            self.logger.error(f"查找IAR项目文件失败: {e}")
            return None
    
    def find_bin_file(self, project_name: str = None) -> Optional[str]:
        """
        查找编译生成的bin文件
        
        Args:
            project_name: 项目名称
            
        Returns:
            str: 找到的bin文件路径，未找到返回None
        """
        try:
            # 常见的bin文件位置
            search_paths = [
                os.path.join(self.project_path, "EWARM", "Debug", "Exe"),
                os.path.join(self.project_path, "EWARM", "Release", "Exe"),
                os.path.join(self.project_path, "..", "EWARM", "Debug", "Exe"),
                os.path.join(self.project_path, "..", "EWARM", "Release", "Exe"),
                os.path.join(self.project_path, "..", "..", "EWARM", "Debug", "Exe"),
                os.path.join(self.project_path, "..", "..", "EWARM", "Release", "Exe"),
                os.path.join(self.project_path, "..", "..", "..", "EWARM", "Debug", "Exe"),
                os.path.join(self.project_path, "..", "..", "..", "EWARM", "Release", "Exe")
            ]
            
            # 如果提供了项目名称，首先尝试查找特定名称的bin文件
            if project_name:
                for bin_dir in search_paths:
                    if os.path.exists(bin_dir):
                        specific_bin = os.path.join(bin_dir, f"{project_name}.bin")
                        if os.path.exists(specific_bin):
                            self.logger.info(f"找到bin文件: {specific_bin}")
                            return specific_bin
            
            # 如果直接路径找不到，尝试搜索所有bin文件
            search_dirs = [
                os.path.join(self.project_path, "EWARM"),
                os.path.join(self.project_path, "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "EWARM"),
                os.path.join(self.project_path, "..", "..", "..", "EWARM")
            ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root, dirs, files in os.walk(search_dir):
                        for file in files:
                            if file.lower().endswith('.bin'):
                                file_path = os.path.join(root, file)
                                self.logger.info(f"找到bin文件: {file_path}")
                                return file_path
            
            self.logger.warning("未找到bin文件")
            return None
            
        except Exception as e:
            self.logger.error(f"查找bin文件失败: {e}")
            return None
    
    def find_main_c_file(self) -> Optional[str]:
        """
        查找main.c文件
        
        Returns:
            str: 找到的main.c文件路径，未找到返回None
        """
        try:
            # 常见的main.c位置
            search_paths = [
                os.path.join(self.project_path, "app", "main.c"),
                os.path.join(self.project_path, "src", "main.c"),
                os.path.join(self.project_path, "main.c"),
                os.path.join(self.project_path, "..", "app", "main.c"),
                os.path.join(self.project_path, "..", "src", "main.c"),
                os.path.join(self.project_path, "..", "main.c")
            ]
            
            for main_c_path in search_paths:
                if os.path.exists(main_c_path):
                    self.logger.info(f"找到main.c文件: {main_c_path}")
                    return main_c_path
            
            # 如果直接路径找不到，尝试搜索
            search_dirs = [
                self.project_path,
                os.path.join(self.project_path, ".."),
                os.path.join(self.project_path, "..", "..")
            ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root, dirs, files in os.walk(search_dir):
                        for file in files:
                            if file.lower() == "main.c":
                                file_path = os.path.join(root, file)
                                self.logger.info(f"找到main.c文件: {file_path}")
                                return file_path
            
            self.logger.warning(f"未找到main.c文件，搜索路径: {search_paths}")
            return None
            
        except Exception as e:
            self.logger.error(f"查找main.c文件失败: {e}")
            return None
    
    def resolve_relative_path(self, relative_path: str) -> str:
        """
        解析相对路径为绝对路径
        
        Args:
            relative_path: 相对路径
            
        Returns:
            str: 绝对路径
        """
        if os.path.isabs(relative_path):
            return relative_path
        
        # 基于项目根目录解析相对路径
        absolute_path = os.path.join(self.project_path, relative_path)
        absolute_path = os.path.normpath(absolute_path)
        
        self.logger.info(f"解析相对路径: {relative_path} -> {absolute_path}")
        return absolute_path
    
    def validate_paths(self, paths: dict) -> Tuple[bool, List[str]]:
        """
        验证路径是否存在
        
        Args:
            paths: 路径字典，键为路径名称，值为路径字符串
            
        Returns:
            Tuple[bool, List[str]]: (是否全部有效, 无效路径列表)
        """
        invalid_paths = []
        
        for name, path in paths.items():
            if not path:
                continue
                
            # 解析相对路径
            if not os.path.isabs(path):
                path = self.resolve_relative_path(path)
            
            if not os.path.exists(path):
                invalid_paths.append(f"{name}: {path}")
                self.logger.warning(f"路径不存在: {name} = {path}")
            else:
                self.logger.info(f"路径有效: {name} = {path}")
        
        return len(invalid_paths) == 0, invalid_paths
    
    def auto_find_paths(self, config: dict) -> dict:
        """
        自动查找并更新配置中的路径
        
        Args:
            config: 配置字典
            
        Returns:
            dict: 更新后的配置字典
        """
        updated_config = config.copy()
        
        # 确保project_settings存在
        if 'project_settings' not in updated_config:
            updated_config['project_settings'] = {}
        
        project_settings = updated_config['project_settings']
        
        # 查找IAR工作区文件
        current_workspace = project_settings.get('iar_workspace_path', '')
        if not current_workspace or not os.path.exists(current_workspace):
            workspace_path = self.find_iar_workspace()
            if workspace_path:
                project_settings['iar_workspace_path'] = workspace_path
                self.logger.info(f"自动找到IAR工作区文件: {workspace_path}")
        
        # 查找IAR项目文件
        current_project = project_settings.get('iar_project_path', '')
        if not current_project or not os.path.exists(current_project):
            project_path = self.find_iar_project()
            if project_path:
                project_settings['iar_project_path'] = project_path
                self.logger.info(f"自动找到IAR项目文件: {project_path}")
        
        # 查找bin文件
        current_bin = project_settings.get('output_bin_path', '')
        if not current_bin or not os.path.exists(current_bin):
            # 尝试从项目文件中获取项目名称
            project_name = self._extract_project_name_from_ewp(project_settings.get('iar_project_path', ''))
            if not project_name:
                project_name = 'MCU'  # 默认项目名称
            
            bin_path = self.find_bin_file(project_name)
            if bin_path:
                project_settings['output_bin_path'] = bin_path
                self.logger.info(f"自动找到bin文件: {bin_path}")
        
        return updated_config
    
    def _extract_project_name_from_ewp(self, ewp_path: str) -> Optional[str]:
        """
        从ewp文件中提取项目名称（bin文件名）
        
        Args:
            ewp_path: ewp文件路径
            
        Returns:
            str: 项目名称（bin文件名），失败时返回None
        """
        try:
            if not ewp_path or not os.path.exists(ewp_path):
                return None
            
            # 读取ewp文件内容
            with open(ewp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找输出文件名配置
            # 在ewp文件中查找类似 <name>MCU</name> 的配置
            import re
            name_match = re.search(r'<name>([^<]+)</name>', content)
            if name_match:
                project_name = name_match.group(1).strip()
                self.logger.info(f"从ewp文件提取项目名称: {project_name}")
                return project_name
            
            # 如果没找到，尝试查找其他可能的配置
            # 查找 <configuration name="Debug"> 中的配置
            config_match = re.search(r'<configuration[^>]*name="([^"]+)"', content)
            if config_match:
                config_name = config_match.group(1).strip()
                # 通常bin文件名与配置名相关
                project_name = config_name
                self.logger.info(f"从ewp文件配置名提取项目名称: {project_name}")
                return project_name
            
            # 如果都没找到，使用文件名作为默认值
            project_name = os.path.splitext(os.path.basename(ewp_path))[0]
            self.logger.warning(f"无法从ewp文件内容提取项目名称，使用文件名: {project_name}")
            return project_name
            
        except Exception as e:
            self.logger.error(f"从ewp文件提取项目名称失败: {e}")
            # 失败时使用文件名作为默认值
            try:
                project_name = os.path.splitext(os.path.basename(ewp_path))[0]
                self.logger.warning(f"解析失败，使用文件名作为默认值: {project_name}")
                return project_name
            except:
                return None


def test_path_manager():
    """测试路径管理器功能"""
    manager = PathManager()
    
    print("路径管理器测试")
    print(f"项目根目录: {manager.project_path}")
    
    # 查找各种文件
    workspace = manager.find_iar_workspace()
    print(f"IAR工作区文件: {workspace}")
    
    project = manager.find_iar_project()
    print(f"IAR项目文件: {project}")
    
    bin_file = manager.find_bin_file()
    print(f"Bin文件: {bin_file}")
    
    main_c = manager.find_main_c_file()
    print(f"Main.c文件: {main_c}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_path_manager()
