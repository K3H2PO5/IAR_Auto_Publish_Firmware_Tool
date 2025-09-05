#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.c文件更新模块
负责更新main.c文件中的版本号
"""

import os
import re
import logging
from typing import Tuple, Optional


class MainCUpdater:
    """main.c文件更新器"""
    
    def __init__(self, config: dict):
        """
        初始化main.c更新器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 版本号模式（每一位固定一位十进制数）
        self.version_pattern = r'V(\d)\.(\d)\.(\d)\.(\d)'
    
    def extract_version_from_main_c(self, main_c_path: str) -> Optional[str]:
        """
        从main.c文件中提取固件版本
        
        Args:
            main_c_path: main.c文件路径
            
        Returns:
            str: 版本字符串，失败时返回None
        """
        try:
            if not os.path.exists(main_c_path):
                self.logger.error(f"main.c文件不存在: {main_c_path}")
                return None
            
            with open(main_c_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找 __Firmware_Version 定义
            pattern = r'__root const char __Firmware_Version\[10\] = "([^"]+)"'
            match = re.search(pattern, content)
            
            if match:
                version = match.group(1)
                self.logger.info(f"从main.c提取到版本: {version}")
                return version
            else:
                self.logger.warning("在main.c中未找到__Firmware_Version定义")
                return None
                
        except Exception as e:
            self.logger.error(f"从main.c提取版本失败: {e}")
            return None
    
    def update_version_in_main_c(self, main_c_path: str, new_version: str) -> Tuple[bool, str]:
        """
        更新main.c文件中的版本号
        
        Args:
            main_c_path: main.c文件路径
            new_version: 新版本号
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            # 输入验证
            if not main_c_path:
                return False, "main.c文件路径为空"
            
            if not new_version:
                return False, "新版本号为空"
            
            if not isinstance(main_c_path, str):
                return False, f"main.c文件路径类型错误: {type(main_c_path)}"
            
            if not isinstance(new_version, str):
                return False, f"版本号类型错误: {type(new_version)}"
            
            if not os.path.exists(main_c_path):
                return False, f"main.c文件不存在: {main_c_path}"
            
            # 验证版本号格式
            if not re.match(self.version_pattern, new_version):
                return False, f"版本号格式不正确: {new_version}，应为 Vx.x.x.x 格式"
            
            # 检查文件是否可写
            if not os.access(main_c_path, os.W_OK):
                return False, f"main.c文件不可写: {main_c_path}"
            
            # 读取文件内容
            with open(main_c_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换版本号
            pattern = r'(__root const char __Firmware_Version\[10\] = ")[^"]+(")'
            replacement = f'\\g<1>{new_version}\\g<2>'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content == content:
                return False, "未找到版本号定义或版本号未发生变化"
            
            # 备份原文件
            backup_path = main_c_path + '.backup'
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info(f"已创建备份文件: {backup_path}")
            except Exception as e:
                self.logger.warning(f"创建备份文件失败: {e}")
            
            # 写入新内容
            with open(main_c_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"成功更新main.c中的版本号: {new_version}")
            return True, f"版本号已更新为: {new_version}"
            
        except Exception as e:
            error_msg = f"更新main.c版本号失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def validate_version_format(self, version: str) -> bool:
        """
        验证版本号格式是否正确
        
        Args:
            version: 版本号字符串
            
        Returns:
            bool: 格式是否正确
        """
        return bool(re.match(self.version_pattern, version))
    
    def get_version_line_info(self, main_c_path: str) -> dict:
        """
        获取main.c中版本号行的信息
        
        Args:
            main_c_path: main.c文件路径
            
        Returns:
            dict: 版本号行信息
        """
        info = {
            'found': False,
            'line_number': 0,
            'line_content': '',
            'version': None
        }
        
        try:
            if not os.path.exists(main_c_path):
                return info
            
            with open(main_c_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if '__Firmware_Version' in line and '=' in line:
                    info['found'] = True
                    info['line_number'] = i
                    info['line_content'] = line.strip()
                    
                    # 提取版本号
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        info['version'] = match.group(1)
                    break
            
        except Exception as e:
            self.logger.error(f"获取版本号行信息失败: {e}")
        
        return info


def test_main_c_updater():
    """测试main.c更新器功能"""
    # 测试配置
    test_config = {
        'version_pattern': r'V(\d)\.(\d)\.(\d)\.(\d)'
    }
    
    updater = MainCUpdater(test_config)
    
    print("main.c更新器测试")
    
    # 测试版本号格式验证
    test_versions = ["V0.0.1.0", "V1.2.3.4", "V9.9.9.9", "V10.1.2.3", "V1.23.4.5"]
    for version in test_versions:
        is_valid = updater.validate_version_format(version)
        print(f"版本号 {version}: {'有效' if is_valid else '无效'}")
    
    # 测试版本号行信息提取
    main_c_path = "../app/main.c"
    if os.path.exists(main_c_path):
        info = updater.get_version_line_info(main_c_path)
        print(f"版本号行信息: {info}")
        
        # 测试版本号提取
        current_version = updater.extract_version_from_main_c(main_c_path)
        print(f"当前版本: {current_version}")
    else:
        print("main.c文件不存在，跳过文件测试")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_main_c_updater()
