#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IAR固件发布工具 - 打包脚本
使用PyInstaller将Python程序打包成exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from tool_version_manager import ToolVersionManager

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        kwargs = {}
        if sys.platform == 'win32' and hasattr(subprocess, 'CREATE_NO_WINDOW'):
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], **kwargs)
        print("✓ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller安装失败: {e}")
        return False

def increment_version():
    """递增工具版本号"""
    print("正在递增工具版本号...")
    try:
        manager = ToolVersionManager()
        new_version = manager.auto_increment_version()
        if new_version:
            print(f"✓ 工具版本已递增到: {new_version}")
            return new_version
        else:
            print("✗ 版本号递增失败")
            return "1.0.0.0"
    except Exception as e:
        print(f"✗ 版本号递增失败: {e}")
        return "1.0.0.0"

def get_current_version():
    """获取当前版本号"""
    try:
        manager = ToolVersionManager()
        version = manager.get_current_version()
        return version or "1.0.0.0"
    except Exception as e:
        print(f"✗ 获取版本号失败: {e}")
        return "1.0.0.0"

def create_spec_file():
    """创建PyInstaller spec文件（备用方法）"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkinter.ttk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IAR固件发布工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version_file=None,
)
'''
    
    with open("IAR_Firmware_Publish_Tool.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✓ 创建spec文件成功（备用）")

# 固定spec文件名称
SPEC_NAME_BASE = "IAR_Firmware_Publish_Tool"

def create_fixed_spec_file(spec_name=SPEC_NAME_BASE):
    """创建固定名称的spec文件"""
    print(f"正在创建spec文件: {spec_name}.spec...")
    
    # 清理之前的构建文件
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    try:
        # 第一步：生成spec文件（不构建exe）
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", spec_name,  # 使用固定名称
            "--onefile",
            "--windowed",
            "--add-data", "config.json;.",
            "--add-data", "README.md;.",
            "--hidden-import", "tkinter.filedialog",
            "--hidden-import", "tkinter.messagebox",
            "--hidden-import", "tkinter.scrolledtext",
            "--hidden-import", "tkinter.ttk",
            "--specpath", ".",
            "--noconfirm",
            "--clean",
            "--log-level", "WARN",
            "main.py"
        ]
        kwargs = {}
        if sys.platform == 'win32' and hasattr(subprocess, 'CREATE_NO_WINDOW'):
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        subprocess.check_call(cmd, **kwargs)
        print(f"✓ spec文件创建成功: {spec_name}.spec")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ spec文件创建失败: {e}")
        return False

def build_exe_from_spec(version, spec_name=SPEC_NAME_BASE):
    """从spec文件构建exe文件"""
    print(f"正在从spec文件构建exe文件...")
    
    exe_name = f"{spec_name}_v{version}"
    
    # 修改spec文件中的exe名称
    spec_file = f"{spec_name}.spec"
    if os.path.exists(spec_file):
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        # 替换exe名称
        spec_content = spec_content.replace(
            f"name='{spec_name}'",
            f"name='{exe_name}'"
        )
        
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
    
    try:
        # 第二步：从spec文件构建exe
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--distpath", "release",
            "--workpath", "build",
            f"{spec_name}.spec"
        ]
        kwargs = {}
        if sys.platform == 'win32' and hasattr(subprocess, 'CREATE_NO_WINDOW'):
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        subprocess.check_call(cmd, **kwargs)
        print(f"✓ exe文件构建成功: {exe_name}.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ exe文件构建失败: {e}")
        return False

def build_exe():
    """构建exe文件（两步过程）"""
    print("开始构建exe文件...")
    
    # 递增版本号
    version = increment_version()
    
    # 第一步：创建固定名称的spec文件
    if not create_fixed_spec_file():
        return False
    
    # 第二步：从spec文件构建exe
    if not build_exe_from_spec(version):
        return False
    
    return True

def create_installer(version=None):
    """创建安装包"""
    print("创建安装包...")
    
    # 获取版本号
    if not version:
        version = get_current_version()
    
    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # exe文件已经直接生成在release目录中，无需复制
    exe_name = f"IAR固件发布工具_v{version}.exe"
    exe_path = release_dir / exe_name
    if exe_path.exists():
        print(f"✓ exe文件已在发布目录: {exe_name}")
    else:
        print("✗ 未找到exe文件")
    
    # 复制配置文件
    config_files = ["config.json", "README.md"]
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, release_dir / file)
            print(f"✓ 复制{file}到发布目录")
    
    # 创建用户配置目录
    user_config_dir = release_dir / "user_config"
    user_config_dir.mkdir(exist_ok=True)
    
    # 创建示例用户配置
    example_user_config = {
        "project_settings": {
            "iar_installation_path": "",
            "project_path": "",
            "output_directory": "./output",
            "fw_publish_directory": "./fw_publish",
            "main_file": ""
        },
        "binary_settings": {
            "config_file": "",
            "bin_start_address": 0
        }
    }
    
    import json
    with open(release_dir / "user_config" / "example_user_config.json", "w", encoding="utf-8") as f:
        json.dump(example_user_config, f, indent=4, ensure_ascii=False)
    
    print("✓ 创建示例用户配置文件")
    
    # 创建使用说明
    usage_guide = """# IAR固件发布工具 - 使用说明

## 首次使用

1. 运行 IAR固件发布工具.exe
2. 点击"设置"按钮
3. 配置以下项目：
   - IAR安装路径：选择IAR安装目录
   - 项目路径：选择您的MCU项目目录
   - 配置文件：选择包含#pragma location定义的C文件
   - bin起始地址：设置bin文件的起始地址

## 日常使用

1. 确保项目路径正确
2. 点击"检查Git状态"查看代码状态
3. 点击"检查版本"查看当前固件版本
4. 点击"开始编译"进行编译和发布

## 文件说明

- config.json：工具默认配置（不要修改）
- user_config/：用户配置目录
- logs/：日志文件目录
- output/：编译输出目录
- fw_publish/：固件发布目录

## 注意事项

- 确保IAR已正确安装
- 确保项目包含正确的#pragma location定义
- 确保bin起始地址配置正确
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(usage_guide)
    
    print("✓ 创建使用说明")
    print(f"✓ 发布包已创建在: {release_dir.absolute()}")

def main():
    """主函数"""
    print("=" * 50)
    print("IAR固件发布工具 - 打包脚本")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("无法安装PyInstaller，请手动安装：pip install pyinstaller")
            return False
    
    # 构建exe
    if not build_exe():
        return False
    
    # 获取当前版本号
    current_version = get_current_version()
    
    # 创建安装包
    create_installer(current_version)
    
    # 获取最终版本号
    final_version = get_current_version()
    
    print("=" * 50)
    print("✓ 打包完成！")
    print(f"发布文件位于 release/ 目录")
    print(f"可执行文件: release/{SPEC_NAME_BASE}_v{final_version}.exe")
    print(f"版本号: {final_version}")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
