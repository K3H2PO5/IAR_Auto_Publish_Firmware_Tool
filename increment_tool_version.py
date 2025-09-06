#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Version Increment Script
Called during exe packaging to increment tool version number
"""

import os
import sys
import re
from typing import Optional, Tuple

def parse_version(version_str: str) -> Optional[Tuple[int, int, int, int]]:
    """
    Parse version string
    
    Args:
        version_str: Version string, format like "1.0.1.9"
        
    Returns:
        tuple: (major, minor, revision, build) or None
    """
    pattern = r'(\d+)\.(\d+)\.(\d+)\.(\d+)'
    match = re.match(pattern, version_str)
    if match:
        return tuple(int(x) for x in match.groups())
    return None

def format_version(major: int, minor: int, revision: int, build: int) -> str:
    """
    Format version number
    
    Args:
        major, minor, revision, build: Version number parts
        
    Returns:
        str: Formatted version number
    """
    return f"{major}.{minor}.{revision}.{build}"

def increment_version(major: int, minor: int, revision: int, build: int) -> Tuple[int, int, int, int]:
    """
    Increment version number
    Note: Each version part is limited to 0-9
    
    Args:
        major, minor, revision, build: Current version number
        
    Returns:
        tuple: Incremented version number
    """
    # Ensure version parts are within 0-9 range
    major = min(major, 9)
    minor = min(minor, 9)
    revision = min(revision, 9)
    build = min(build, 9)
    
    # Increment from the last digit
    build += 1
    
    # Check if carry is needed
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
                    # If major version also exceeds 9, reset to 1
                    major = 1
    
    return (major, minor, revision, build)

def update_main_py_version(new_version: str) -> bool:
    """
    Update version number in main.py
    
    Args:
        new_version: New version number
        
    Returns:
        bool: Whether update was successful
    """
    try:
        main_py_path = "main.py"
        if not os.path.exists(main_py_path):
            print(f"Error: Cannot find {main_py_path}")
            return False
        
        # Read file content
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace version number
        pattern = r'__version__ = "[\d\.]+"'
        replacement = f'__version__ = "{new_version}"'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            
            # Write back to file
            with open(main_py_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Updated version in main.py to: {new_version}")
            return True
        else:
            print("Error: Cannot find version definition in main.py")
            return False
            
    except Exception as e:
        print(f"Failed to update version in main.py: {e}")
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
        print(f"Failed to get current version: {e}")
        return None

def main():
    """Main function"""
    print("Tool Version Increment Script")
    print("=" * 50)
    
    # Get current version
    current_version = get_current_version()
    if not current_version:
        print("Error: Cannot get current version")
        sys.exit(1)
    
    print(f"Current version: {current_version}")
    
    # Parse version
    version_tuple = parse_version(current_version)
    if not version_tuple:
        print("Error: Cannot parse current version")
        sys.exit(1)
    
    # Increment version
    new_version_tuple = increment_version(*version_tuple)
    new_version = format_version(*new_version_tuple)
    
    print(f"New version: {new_version}")
    
    # Update version in main.py
    if update_main_py_version(new_version):
        print("Version increment successful!")
        print(f"Version updated from {current_version} to {new_version}")
        # Output the new version for build_exe.py to capture
        print(new_version)
    else:
        print("Version increment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
