#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IAR编译模块
负责调用IAR编译系统生成bin文件
"""

import subprocess
import os
import logging
import time
from typing import Tuple, Optional
from pathlib import Path


class IARBuilder:
    """IAR编译管理类"""
    
    def __init__(self, config: dict):
        """
        初始化IAR编译器
        
        Args:
            config: 配置字典，包含IAR相关设置
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 从配置中获取路径
        iar_installation_path = config.get('iar_installation_path', '')
        self.iar_exe_path = self._find_iar_executable(iar_installation_path)
        self.workspace_path = config.get('iar_workspace_path', '')
        self.project_path = config.get('iar_project_path', '')
        self.output_bin_path = config.get('output_bin_path', '')
        self.build_config = config.get('build_configuration', 'Debug')
        self.clean_before_build = config.get('clean_before_build', False)  # 默认使用增量编译
        self.timeout_seconds = config.get('timeout_seconds', 300)
        
        # 验证路径
        self._validate_paths()
    
    def _find_iar_executable(self, iar_dir: str) -> str:
        """
        在IAR安装目录中查找IarBuild.exe
        
        Args:
            iar_dir: IAR安装目录
            
        Returns:
            str: IarBuild.exe的完整路径，未找到返回默认路径
        """
        if not iar_dir:
            return 'C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.3/common/bin/IarBuild.exe'
        
        possible_paths = [
            os.path.join(iar_dir, "bin", "IarBuild.exe"),
            os.path.join(iar_dir, "IarBuild.exe"),
            os.path.join(iar_dir, "arm", "bin", "IarBuild.exe"),
            os.path.join(iar_dir, "EWARM", "bin", "IarBuild.exe"),
            os.path.join(iar_dir, "common", "bin", "IarBuild.exe")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.logger.info(f"找到IAR可执行文件: {path}")
                return path
        
        # 如果没找到，返回原始路径（可能是直接指定的exe路径）
        if iar_dir.endswith('.exe') and os.path.exists(iar_dir):
            return iar_dir
        
        self.logger.warning(f"在IAR目录中未找到IarBuild.exe: {iar_dir}")
        return iar_dir
    
    def _validate_paths(self):
        """验证IAR相关路径是否存在"""
        # 检查IAR可执行文件
        if not os.path.exists(self.iar_exe_path):
            self.logger.warning(f"IAR可执行文件不存在: {self.iar_exe_path}")
        
        # 检查工作区文件
        if self.workspace_path and not os.path.exists(self.workspace_path):
            self.logger.warning(f"IAR工作区文件不存在: {self.workspace_path}")
        
        # 检查项目文件
        if self.project_path and not os.path.exists(self.project_path):
            self.logger.warning(f"IAR项目文件不存在: {self.project_path}")
    
    def clean_project(self) -> bool:
        """
        清理项目
        
        Returns:
            bool: 清理是否成功
        """
        try:
            self.logger.info("开始清理项目...")
            
            # 构建清理命令
            cmd = [
                self.iar_exe_path,
                self.project_path,
                '-clean',
                self.build_config
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            if result.returncode == 0:
                self.logger.info("项目清理成功")
                return True
            else:
                self.logger.error(f"项目清理失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("项目清理超时")
            return False
        except Exception as e:
            self.logger.error(f"项目清理异常: {e}")
            return False
    
    def build_project(self, force_rebuild: bool = False) -> Tuple[bool, str]:
        """
        编译项目
        
        Args:
            force_rebuild: 是否强制重新编译（清理后编译）
        
        Returns:
            Tuple[bool, str]: (编译是否成功, 输出信息)
        """
        try:
            self.logger.info(f"开始编译项目: {self.project_path}")
            self.logger.info(f"编译配置: {self.build_config}")
            
            # 决定是否清理项目
            should_clean = self.clean_before_build or force_rebuild
            if should_clean:
                self.logger.info("执行清理编译（rebuild all）")
                if not self.clean_project():
                    return False, "项目清理失败"
                # 使用build命令进行全量编译
                cmd = [
                    self.iar_exe_path,
                    self.project_path,
                    '-build',
                    self.build_config
                ]
            else:
                self.logger.info("执行增量编译（make）")
                # 使用make命令进行增量编译
                cmd = [
                    self.iar_exe_path,
                    self.project_path,
                    self.build_config  # 不指定-build参数，默认为make操作
                ]
            
            self.logger.info(f"执行命令: {' '.join(cmd)}")
            
            # 执行编译
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            end_time = time.time()
            
            compile_time = end_time - start_time
            self.logger.info(f"编译耗时: {compile_time:.2f}秒")
            
            # 分析编译结果
            if result.returncode == 0:
                self.logger.info("编译成功")
                output_info = f"编译成功\n耗时: {compile_time:.2f}秒\n\n输出信息:\n{result.stdout}"
                return True, output_info
            else:
                self.logger.error("编译失败")
                error_info = f"编译失败\n返回码: {result.returncode}\n\n错误信息:\n{result.stderr}\n\n输出信息:\n{result.stdout}"
                return False, error_info
                
        except subprocess.TimeoutExpired:
            self.logger.error("编译超时")
            return False, f"编译超时 (>{self.timeout_seconds}秒)"
        except Exception as e:
            self.logger.error(f"编译异常: {e}")
            return False, f"编译异常: {str(e)}"
    
    def check_bin_file(self) -> bool:
        """
        检查生成的bin文件是否存在
        
        Returns:
            bool: bin文件是否存在
        """
        if not self.output_bin_path:
            self.logger.warning("未配置输出bin文件路径")
            return False
        
        bin_exists = os.path.exists(self.output_bin_path)
        if bin_exists:
            file_size = os.path.getsize(self.output_bin_path)
            self.logger.info(f"找到bin文件: {self.output_bin_path}, 大小: {file_size} 字节")
        else:
            self.logger.warning(f"未找到bin文件: {self.output_bin_path}")
        
        return bin_exists
    
    def get_bin_file_info(self) -> dict:
        """
        获取bin文件信息
        
        Returns:
            dict: bin文件信息
        """
        info = {
            'exists': False,
            'path': self.output_bin_path,
            'size': 0,
            'modified_time': None
        }
        
        if self.check_bin_file():
            try:
                stat = os.stat(self.output_bin_path)
                info['exists'] = True
                info['size'] = stat.st_size
                info['modified_time'] = time.ctime(stat.st_mtime)
            except Exception as e:
                self.logger.error(f"获取bin文件信息失败: {e}")
        
        return info
    
    def build_and_check(self) -> Tuple[bool, str, dict]:
        """
        编译项目并检查结果
        
        Returns:
            Tuple[bool, str, dict]: (是否成功, 消息, bin文件信息)
        """
        # 执行编译
        success, message = self.build_project()
        
        # 获取bin文件信息
        bin_info = self.get_bin_file_info()
        
        if success and not bin_info['exists']:
            success = False
            message += "\n警告: 编译成功但未找到输出bin文件"
        
        return success, message, bin_info
    
    def smart_build(self, only_version_changed: bool = True) -> Tuple[bool, str]:
        """
        智能编译：根据修改内容决定编译策略
        
        Args:
            only_version_changed: 是否只有版本号发生变化
        
        Returns:
            Tuple[bool, str]: (编译是否成功, 输出信息)
        """
        if only_version_changed:
            self.logger.info("检测到仅版本号变化，使用增量编译（make）")
            return self.build_project(force_rebuild=False)
        else:
            self.logger.info("检测到代码变化，使用清理编译（rebuild all）")
            return self.build_project(force_rebuild=True)


def test_iar_builder():
    """测试IAR编译器功能"""
    # 测试配置
    test_config = {
        'iar_installation_path': 'C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.3/common/bin/IarBuild.exe',
        'iar_workspace_path': '../EWARM/Project_N32A455.eww',
        'iar_project_path': '../EWARM/MCU.ewp',
        'output_bin_path': '../EWARM/Debug/Exe/MCU.bin',
        'build_configuration': 'Debug',
        'clean_before_build': True,
        'timeout_seconds': 300
    }
    
    builder = IARBuilder(test_config)
    
    print("IAR编译器测试")
    print(f"IAR可执行文件: {builder.iar_exe_path}")
    print(f"项目文件: {builder.project_path}")
    print(f"输出bin文件: {builder.output_bin_path}")
    
    # 检查bin文件
    bin_info = builder.get_bin_file_info()
    print(f"Bin文件信息: {bin_info}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_iar_builder()
