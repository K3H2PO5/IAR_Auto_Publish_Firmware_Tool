#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具版本递增脚本
在打包exe文件时调用此脚本来递增工具版本号
"""

import os
import sys
import re
from typing import Optional, Tuple

def parse_version(version_str: str) -> Optional[Tuple[int, int, int, int]]:
    """
    解析版本号字符串
    
    Args:
        version_str: 版本号字符串，格式如 "1.0.1.9"
        
    Returns:
        tuple: (major, minor, revision, build) 或 None
    """
    pattern = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
    match = re.match(pattern, version_str)
    if match:
        return tuple(int(x) for x in match.groups())
    return None

def format_version(major: int, minor: int, revision: int, build: int) -> str:
    """
    格式化版本号
    
    Args:
        major, minor, revision, build: 版本号各部分
        
    Returns:
        str: 格式化后的版本号
    """
    return f"{major}.{minor}.{revision}.{build}"

def increment_version(major: int, minor: int, revision: int, build: int) -> Tuple[int, int, int, int]:
    """
    递增版本号
    注意：每个版本号部分都限制在0-9之间
    
    Args:
        major, minor, revision, build: 当前版本号
        
    Returns:
        tuple: 递增后的版本号
    """
    # 确保版本号各部分都在0-9范围内
    major = min(major, 9)
    minor = min(minor, 9)
    revision = min(revision, 9)
    build = min(build, 9)
    
    # 从末位开始递增
    build += 1
    
    # 检查是否需要进位
    if build > 9:
        build = 0
        revision += 1
        
        if revision > 9:
            revision = 0
            minor += 1
            
            if minor > 9:
                minor = 0
                major += 1
                
                if major > 9:
                    # 如果主版本号也超过9，重置为1
                    major = 1
    
    return (major, minor, revision, build)

def update_main_py_version(new_version: str) -> bool:
    """
    更新main.py中的版本号
    
    Args:
        new_version: 新的版本号
        
    Returns:
        bool: 是否更新成功
    """
    try:
        main_py_path = "main.py"
        if not os.path.exists(main_py_path):
            print(f"错误：找不到 {main_py_path}")
            return False
        
        # 读取文件内容
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换版本号
        pattern = r'__version__ = "[\d\.]+"'
        replacement = f'__version__ = "{new_version}"'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            
            # 写回文件
            with open(main_py_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"已更新 main.py 中的版本号到: {new_version}")
            return True
        else:
            print("错误：在 main.py 中找不到版本号定义")
            return False
            
    except Exception as e:
        print(f"更新 main.py 版本号失败: {e}")
        return False

def get_current_version() -> Optional[str]:
    """
    获取当前版本号
    
    Returns:
        str: 当前版本号或None
    """
    try:
        main_py_path = "main.py"
        if not os.path.exists(main_py_path):
            return None
        
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找版本号定义
        pattern = r'__version__ = "([\d\.]+)"'
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        
        return None
        
    except Exception as e:
        print(f"获取当前版本号失败: {e}")
        return None

def main():
    """主函数"""
    print("工具版本递增脚本")
    print("=" * 50)
    
    # 获取当前版本
    current_version = get_current_version()
    if not current_version:
        print("错误：无法获取当前版本号")
        sys.exit(1)
    
    print(f"当前版本: {current_version}")
    
    # 解析版本号
    version_tuple = parse_version(current_version)
    if not version_tuple:
        print("错误：无法解析当前版本号")
        sys.exit(1)
    
    # 递增版本号
    new_version_tuple = increment_version(*version_tuple)
    new_version = format_version(*new_version_tuple)
    
    print(f"新版本: {new_version}")
    
    # 更新main.py中的版本号
    if update_main_py_version(new_version):
        print("版本号递增成功！")
        print(f"版本已从 {current_version} 更新到 {new_version}")
    else:
        print("版本号递增失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
