#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IAR项目分析器模块
负责解析IAR项目文件(.ewp)和ICF文件，自动提取flash偏移地址
"""

import os
import re
import xml.etree.ElementTree as ET
import logging
from typing import Optional, Dict, Tuple
from pathlib import Path


class IARProjectAnalyzer:
    """IAR项目分析器"""
    
    def __init__(self):
        """初始化IAR项目分析器"""
        self.logger = logging.getLogger(__name__)
    
    def analyze_ewp_file(self, ewp_path: str) -> Optional[Dict]:
        """
        分析IAR项目文件(.ewp)，提取ICF文件路径
        
        Args:
            ewp_path: IAR项目文件路径
            
        Returns:
            Dict: 包含ICF文件路径和项目信息的字典
        """
        try:
            if not os.path.exists(ewp_path):
                self.logger.error(f"IAR项目文件不存在: {ewp_path}")
                return None
            
            # 解析XML文件
            tree = ET.parse(ewp_path)
            root = tree.getroot()
            
            result = {
                'project_path': ewp_path,
                'icf_files': [],
                'project_name': os.path.splitext(os.path.basename(ewp_path))[0],
                'project_dir': os.path.dirname(ewp_path)
            }
            
            # 查找ICF文件引用
            # IAR项目文件中的ICF文件通常在以下位置：
            # <group><name>Linker files</name><file><name>xxx.icf</name></file></group>
            for group in root.findall('.//group'):
                group_name = group.find('name')
                if group_name is not None and 'linker' in group_name.text.lower():
                    for file_elem in group.findall('file'):
                        name_elem = file_elem.find('name')
                        if name_elem is not None and name_elem.text.endswith('.icf'):
                            icf_file = name_elem.text
                            # 构建完整路径
                            if os.path.isabs(icf_file):
                                full_path = icf_file
                            else:
                                full_path = os.path.join(result['project_dir'], icf_file)
                            
                            result['icf_files'].append({
                                'name': icf_file,
                                'path': full_path,
                                'exists': os.path.exists(full_path)
                            })
                            self.logger.info(f"找到ICF文件: {full_path}")
            
            # 如果没找到，尝试其他常见的ICF文件位置
            if not result['icf_files']:
                self.logger.warning("在项目文件中未找到ICF文件引用，尝试搜索常见位置")
                icf_files = self._search_icf_files(result['project_dir'])
                result['icf_files'] = icf_files
            
            return result
            
        except Exception as e:
            self.logger.error(f"分析IAR项目文件失败: {e}")
            return None
    
    def _search_icf_files(self, project_dir: str) -> list:
        """
        在项目目录中搜索ICF文件
        
        Args:
            project_dir: 项目目录
            
        Returns:
            list: ICF文件信息列表
        """
        icf_files = []
        
        # 常见的ICF文件搜索路径
        search_paths = [
            project_dir,
            os.path.join(project_dir, 'EWARM'),
            os.path.join(project_dir, 'linker'),
            os.path.join(project_dir, 'ld'),
            os.path.join(project_dir, '..', 'EWARM'),
            os.path.join(project_dir, '..', 'linker'),
            os.path.join(project_dir, '..', 'ld')
        ]
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
            
            # 递归搜索.icf文件
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.lower().endswith('.icf'):
                        full_path = os.path.join(root, file)
                        icf_files.append({
                            'name': file,
                            'path': full_path,
                            'exists': True
                        })
                        self.logger.info(f"搜索到ICF文件: {full_path}")
        
        return icf_files
    
    def analyze_icf_file(self, icf_path: str) -> Optional[Dict]:
        """
        分析ICF文件，提取flash偏移地址
        
        Args:
            icf_path: ICF文件路径
            
        Returns:
            Dict: 包含flash偏移地址的字典
        """
        try:
            if not os.path.exists(icf_path):
                self.logger.error(f"ICF文件不存在: {icf_path}")
                return None
            
            with open(icf_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = {
                'icf_path': icf_path,
                'flash_start': None,
                'flash_size': None,
                'ram_start': None,
                'ram_size': None,
                'intvec_start': None
            }
            
            # 查找__ICFEDIT_intvec_start__定义
            intvec_pattern = r'__ICFEDIT_intvec_start__\s*=\s*0x([0-9a-fA-F]+)'
            match = re.search(intvec_pattern, content)
            if match:
                intvec_start = int(match.group(1), 16)
                result['intvec_start'] = intvec_start
                self.logger.info(f"找到__ICFEDIT_intvec_start__: 0x{intvec_start:X}")
            
            # 查找flash区域定义
            # 格式通常为: define memory with size = 0x100000;
            # 或者: define region FLASH = [from 0x08000000 to 0x080FFFFF];
            flash_patterns = [
                r'define\s+region\s+FLASH\s*=\s*\[\s*from\s+0x([0-9a-fA-F]+)\s+to\s+0x([0-9a-fA-F]+)\s*\]',
                r'define\s+memory\s+with\s+size\s*=\s*0x([0-9a-fA-F]+)',
                r'define\s+region\s+ROM\s*=\s*\[\s*from\s+0x([0-9a-fA-F]+)\s+to\s+0x([0-9a-fA-F]+)\s*\]'
            ]
            
            for pattern in flash_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:  # from ... to ... 格式
                        flash_start = int(match.group(1), 16)
                        flash_end = int(match.group(2), 16)
                        result['flash_start'] = flash_start
                        result['flash_size'] = flash_end - flash_start + 1
                        self.logger.info(f"找到Flash区域: 0x{flash_start:X} - 0x{flash_end:X} (大小: 0x{result['flash_size']:X})")
                    else:  # size 格式
                        flash_size = int(match.group(1), 16)
                        # 尝试从intvec_start推断flash_start
                        if result['intvec_start']:
                            result['flash_start'] = result['intvec_start']
                            result['flash_size'] = flash_size
                            self.logger.info(f"找到Flash大小: 0x{flash_size:X}, 起始地址: 0x{result['flash_start']:X}")
                    break
            
            # 查找RAM区域定义
            ram_patterns = [
                r'define\s+region\s+RAM\s*=\s*\[\s*from\s+0x([0-9a-fA-F]+)\s+to\s+0x([0-9a-fA-F]+)\s*\]',
                r'define\s+region\s+IRAM\s*=\s*\[\s*from\s+0x([0-9a-fA-F]+)\s+to\s+0x([0-9a-fA-F]+)\s*\]'
            ]
            
            for pattern in ram_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    ram_start = int(match.group(1), 16)
                    ram_end = int(match.group(2), 16)
                    result['ram_start'] = ram_start
                    result['ram_size'] = ram_end - ram_start + 1
                    self.logger.info(f"找到RAM区域: 0x{ram_start:X} - 0x{ram_end:X} (大小: 0x{result['ram_size']:X})")
                    break
            
            # 验证结果
            if not result['intvec_start'] and not result['flash_start']:
                self.logger.warning("未找到flash起始地址信息")
                return None
            
            return result
            
        except Exception as e:
            self.logger.error(f"分析ICF文件失败: {e}")
            return None
    
    def get_flash_offset_from_project(self, ewp_path: str) -> Optional[int]:
        """
        从IAR项目文件中获取flash偏移地址
        
        Args:
            ewp_path: IAR项目文件路径
            
        Returns:
            int: flash偏移地址，失败返回None
        """
        try:
            self.logger.info(f"开始分析IAR项目文件: {ewp_path}")
            # 分析项目文件
            project_info = self.analyze_ewp_file(ewp_path)
            if not project_info:
                self.logger.error("项目文件分析失败")
                return None
                
            if not project_info['icf_files']:
                self.logger.error("未找到ICF文件")
                return None
            
            self.logger.info(f"找到 {len(project_info['icf_files'])} 个ICF文件")
            # 分析第一个可用的ICF文件
            for i, icf_info in enumerate(project_info['icf_files']):
                self.logger.info(f"检查ICF文件 {i+1}: {icf_info['path']} (存在: {icf_info['exists']})")
                if icf_info['exists']:
                    icf_result = self.analyze_icf_file(icf_info['path'])
                    if icf_result and icf_result['intvec_start']:
                        self.logger.info(f"从项目 {ewp_path} 获取到flash偏移地址: 0x{icf_result['intvec_start']:X}")
                        return icf_result['intvec_start']
                    else:
                        self.logger.warning(f"ICF文件 {icf_info['path']} 解析失败或无intvec_start")
                else:
                    self.logger.warning(f"ICF文件不存在: {icf_info['path']}")
            
            self.logger.error("所有ICF文件都无法解析或不存在")
            return None
            
        except Exception as e:
            self.logger.error(f"从项目文件获取flash偏移地址失败: {e}")
            return None
    
    def find_ewp_file(self, project_path: str) -> Optional[str]:
        """
        在项目路径中查找IAR项目文件
        
        Args:
            project_path: 项目根目录
            
        Returns:
            str: 找到的.ewp文件路径，未找到返回None
        """
        try:
            # 搜索路径
            search_paths = [
                project_path,
                os.path.join(project_path, 'EWARM'),
                os.path.join(project_path, '..', 'EWARM'),
                os.path.join(project_path, '..', '..', 'EWARM')
            ]
            
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue
                
                # 递归搜索.ewp文件
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if file.lower().endswith('.ewp'):
                            ewp_path = os.path.join(root, file)
                            self.logger.info(f"找到IAR项目文件: {ewp_path}")
                            return ewp_path
            
            self.logger.warning("未找到IAR项目文件")
            return None
            
        except Exception as e:
            self.logger.error(f"查找IAR项目文件失败: {e}")
            return None


def test_iar_project_analyzer():
    """测试IAR项目分析器功能"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    analyzer = IARProjectAnalyzer()
    
    print("IAR项目分析器测试")
    
    # 测试查找项目文件
    ewp_file = analyzer.find_ewp_file(".")
    print(f"找到项目文件: {ewp_file}")
    
    if ewp_file:
        # 测试分析项目文件
        project_info = analyzer.analyze_ewp_file(ewp_file)
        print(f"项目信息: {project_info}")
        
        # 测试获取flash偏移地址
        flash_offset = analyzer.get_flash_offset_from_project(ewp_file)
        print(f"Flash偏移地址: 0x{flash_offset:X}" if flash_offset else "未找到")


if __name__ == "__main__":
    test_iar_project_analyzer()
