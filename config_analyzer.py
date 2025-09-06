#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置分析器模块
负责分析.c文件中的二进制配置参数
"""

import os
import re
import logging
from typing import Dict, Optional, Tuple


class ConfigAnalyzer:
    """配置分析器"""
    
    def __init__(self):
        """初始化配置分析器"""
        self.logger = logging.getLogger(__name__)
    
    def analyze_config_file(self, config_file_path: str, feature_settings: Dict = None) -> Dict[str, int]:
        """
        分析配置文件，提取二进制参数（仅支持IAR #pragma location定位方式）
        
        Args:
            config_file_path: 配置文件路径
            feature_settings: 功能设置字典，包含关键字配置
            
        Returns:
            Dict[str, int]: 解析出的参数字典
        """
        result = {
            'firmware_version_offset': 0,
            'git_commit_id_offset': 0,
            'file_size_offset': 0,
            'bin_checksum_offset': 0,
            'hash_value_offset': 0,
            'commit_id_size': 7,
            'crc_size': 4,
            'reserved_area_size': 512
            # 注意：不包含bin_start_address，因为它应该由用户设置
        }
        
        # 获取用户配置的关键字，如果没有则使用默认值
        if feature_settings is None:
            feature_settings = {}
        
        git_commit_id_keyword = feature_settings.get('git_commit_id_keyword', '__git_commit_id')
        file_size_keyword = feature_settings.get('file_size_keyword', '__file_size')
        bin_checksum_keyword = feature_settings.get('bin_checksum_keyword', '__bin_checksum')
        hash_value_keyword = feature_settings.get('hash_value_keyword', '__hash_value')
        firmware_version_keyword = feature_settings.get('firmware_version_keyword', '__Firmware_Version')
        
        try:
            if not os.path.exists(config_file_path):
                self.logger.error(f"配置文件不存在: {config_file_path}")
                return result
            
            with open(config_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找固件版本的地址（使用用户配置的关键字）
            fw_version_pattern = rf'#pragma\s+location\s*=\s*0x([0-9a-fA-F]+)\s*\n\s*__root\s+const\s+char\s+{re.escape(firmware_version_keyword)}[^;]*;'
            fw_version_offset = self._find_pragma_location(content, fw_version_pattern)
            if fw_version_offset is not None:
                result['firmware_version_offset'] = fw_version_offset
                self.logger.info(f"找到{firmware_version_keyword}地址: 0x{fw_version_offset:X}")
            
            # 查找Git提交ID的地址（使用用户配置的关键字）
            commit_id_pattern = rf'#pragma\s+location\s*=\s*0x([0-9a-fA-F]+)\s*\n\s*__root\s+const\s+char\s+{re.escape(git_commit_id_keyword)}[^;]*;'
            commit_id_offset = self._find_pragma_location(content, commit_id_pattern)
            if commit_id_offset is not None:
                result['git_commit_id_offset'] = commit_id_offset
                self.logger.info(f"找到{git_commit_id_keyword}地址: 0x{commit_id_offset:X}")
            
            # 查找文件大小的地址（使用用户配置的关键字）
            file_size_pattern = rf'#pragma\s+location\s*=\s*0x([0-9a-fA-F]+)\s*\n\s*__root\s+volatile\s+const\s+uint32_t\s+{re.escape(file_size_keyword)}[^;]*;'
            file_size_offset = self._find_pragma_location(content, file_size_pattern)
            if file_size_offset is not None:
                result['file_size_offset'] = file_size_offset
                self.logger.info(f"找到{file_size_keyword}地址: 0x{file_size_offset:X}")
            
            # 查找二进制校验和的地址（使用用户配置的关键字）
            checksum_pattern = rf'#pragma\s+location\s*=\s*0x([0-9a-fA-F]+)\s*\n\s*__root\s+volatile\s+const\s+uint32_t\s+{re.escape(bin_checksum_keyword)}[^;]*;'
            checksum_offset = self._find_pragma_location(content, checksum_pattern)
            if checksum_offset is not None:
                result['bin_checksum_offset'] = checksum_offset
                self.logger.info(f"找到{bin_checksum_keyword}地址: 0x{checksum_offset:X}")
            
            # 查找哈希校验和的地址（使用用户配置的关键字）
            # 支持uint32_t和uint8_t数组类型
            hash_value_pattern = rf'#pragma\s+location\s*=\s*0x([0-9a-fA-F]+)\s*\n\s*__root\s+volatile\s+const\s+(?:uint32_t|uint8_t)\s+{re.escape(hash_value_keyword)}(?:\[\d+\])?[^;]*;'
            hash_value_offset = self._find_pragma_location(content, hash_value_pattern)
            if hash_value_offset is not None:
                result['hash_value_offset'] = hash_value_offset
                self.logger.info(f"找到{hash_value_keyword}地址: 0x{hash_value_offset:X}")
            
            # 查找数组大小定义（使用用户配置的关键字）
            commit_id_size_pattern = rf'{re.escape(git_commit_id_keyword)}\[(\d+)\]'
            commit_id_size = self._find_array_size(content, commit_id_size_pattern)
            if commit_id_size is not None:
                result['commit_id_size'] = commit_id_size
                self.logger.info(f"找到{git_commit_id_keyword}数组大小: {commit_id_size}")
            
            # 检查是否找到了所有必需的地址
            missing_addresses = []
            if result['firmware_version_offset'] == 0:
                missing_addresses.append(firmware_version_keyword)
            if result['git_commit_id_offset'] == 0:
                missing_addresses.append(git_commit_id_keyword)
            if result['file_size_offset'] == 0:
                missing_addresses.append(file_size_keyword)
            if result['bin_checksum_offset'] == 0:
                missing_addresses.append(bin_checksum_keyword)
            if result['hash_value_offset'] == 0:
                missing_addresses.append(hash_value_keyword)
            
            if missing_addresses:
                self.logger.error(f"配置文件中缺少以下地址定义: {', '.join(missing_addresses)}")
                self.logger.error("请确保配置文件中包含以下格式的定义:")
                self.logger.error("#pragma location=0x08004410")
                self.logger.error(f"__root const char {firmware_version_keyword}[10] = \"V1.0.0.0\";")
                self.logger.error(f"#pragma location=0x08004420")
                self.logger.error(f"__root const char {git_commit_id_keyword}[7] = \"\";")
                self.logger.error(f"#pragma location=0x08004430")
                self.logger.error(f"__root volatile const uint32_t {file_size_keyword} = 0;")
                self.logger.error(f"#pragma location=0x08004434")
                self.logger.error(f"__root volatile const uint32_t {bin_checksum_keyword} = 0;")
                self.logger.error(f"#pragma location=0x08004438")
                self.logger.error(f"__root volatile const uint32_t {hash_value_keyword} = 0;")
            else:
                self.logger.info(f"配置分析完成: {result}")
            
        except Exception as e:
            self.logger.error(f"分析配置文件失败: {e}")
        
        return result
    
    def _find_pragma_location(self, content: str, pattern: str) -> Optional[int]:
        """
        查找#pragma location定位的地址
        
        Args:
            content: 文件内容
            pattern: 正则表达式模式
            
        Returns:
            int: 十六进制地址，未找到返回None
        """
        try:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                hex_value = match.group(1)
                return int(hex_value, 16)
        except Exception as e:
            self.logger.debug(f"查找#pragma location模式失败 {pattern}: {e}")
        
        return None
    
    def _find_array_size(self, content: str, pattern: str) -> Optional[int]:
        """
        查找数组大小
        
        Args:
            content: 文件内容
            pattern: 正则表达式模式
            
        Returns:
            int: 数组大小，未找到返回None
        """
        try:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                size = match.group(1)
                return int(size)
        except Exception as e:
            self.logger.debug(f"查找数组大小模式失败 {pattern}: {e}")
        
        return None
    
    
    def find_config_file(self, project_path: str) -> Optional[str]:
        """
        查找配置文件
        
        Args:
            project_path: 项目路径
            
        Returns:
            str: 找到的配置文件路径，未找到返回None
        """
        # 常见的配置文件名
        config_names = [
            'binary_config.c',
            'config.c',
            'binary_info.c',
            'firmware_info.c',
            'version_info.c',
            'binary_params.c'
        ]
        
        # 搜索路径
        search_paths = [
            project_path,
            os.path.join(project_path, 'src'),
            os.path.join(project_path, 'app'),
            os.path.join(project_path, 'inc'),
            os.path.join(project_path, 'include'),
            os.path.join(project_path, '..', 'src'),
            os.path.join(project_path, '..', 'app'),
            os.path.join(project_path, '..', 'inc'),
            os.path.join(project_path, '..', 'include')
        ]
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.lower() in [name.lower() for name in config_names]:
                        file_path = os.path.join(root, file)
                        self.logger.info(f"找到配置文件: {file_path}")
                        return file_path
        
        self.logger.warning("未找到配置文件")
        return None
    
    def validate_config(self, config: Dict[str, int], feature_settings: Dict = None) -> Tuple[bool, str]:
        """
        验证配置参数
        
        Args:
            config: 配置字典
            feature_settings: 功能设置字典，用于确定哪些字段是必需的
            
        Returns:
            Tuple[bool, str]: (是否有效, 错误信息)
        """
        missing_fields = []
        
        if config['firmware_version_offset'] == 0:
            missing_fields.append("__Firmware_Version地址")
        
        # 根据功能设置检查必需的字段
        if feature_settings is None:
            feature_settings = {}
        
        if feature_settings.get('enable_git_commit_id', True) and config['git_commit_id_offset'] == 0:
            keyword = feature_settings.get('git_commit_id_keyword', '__git_commit_id')
            missing_fields.append(f"{keyword}地址")
        
        if feature_settings.get('enable_file_size', True) and config['file_size_offset'] == 0:
            keyword = feature_settings.get('file_size_keyword', '__file_size')
            missing_fields.append(f"{keyword}地址")
        
        if feature_settings.get('enable_bin_checksum', True) and config['bin_checksum_offset'] == 0:
            keyword = feature_settings.get('bin_checksum_keyword', '__bin_checksum')
            missing_fields.append(f"{keyword}地址")
        
        # 如果启用了Git提交ID功能，检查数组大小
        if feature_settings.get('enable_git_commit_id', True) and config['commit_id_size'] == 0:
            keyword = feature_settings.get('git_commit_id_keyword', '__git_commit_id')
            missing_fields.append(f"{keyword}数组大小")
        
        if missing_fields:
            return False, f"配置文件中缺少以下必需的定义: {', '.join(missing_fields)}。请检查配置文件是否包含正确的#pragma location定义。"
        
        # 检查地址顺序
        offsets = [
            config['firmware_version_offset'],
            config['git_commit_id_offset'],
            config['file_size_offset'],
            config['bin_checksum_offset']
        ]
        
        if offsets != sorted(offsets):
            return False, "地址偏移量必须按顺序排列"
        
        return True, "配置有效"


def test_config_analyzer():
    """测试配置分析器功能"""
    analyzer = ConfigAnalyzer()
    
    print("配置分析器测试")
    
    # 测试查找配置文件
    config_file = analyzer.find_config_file(".")
    print(f"找到配置文件: {config_file}")
    
    if config_file:
        # 测试分析配置文件
        config = analyzer.analyze_config_file(config_file)
        print(f"解析结果: {config}")
        
        # 测试验证配置
        is_valid, message = analyzer.validate_config(config)
        print(f"配置验证: {is_valid}, {message}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_config_analyzer()
