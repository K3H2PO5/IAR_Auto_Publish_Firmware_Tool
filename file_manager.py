#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件管理模块
负责文件重命名、移动、目录管理等操作
"""

import os
import sys
import shutil
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, List


class FileManager:
    """文件管理器"""
    
    def __init__(self, config: dict, project_path: str = None):
        """
        初始化文件管理器
        
        Args:
            config: 配置字典，包含文件管理相关设置
            project_path: 项目目录路径，用于解析相对路径
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # 保存项目路径
        self.project_path = project_path
        
        # 从配置中获取设置
        self.fw_publish_directory = config.get('fw_publish_directory', './fw_publish')
        self.remote_publish_directory = config.get('remote_publish_directory', '')
        
        # 使用项目路径的文件夹名称作为项目名称
        if project_path:
            self.project_name = os.path.basename(os.path.abspath(project_path))
            self.logger.info(f"使用项目路径文件夹名称作为项目名称: {self.project_name}")
        else:
            self.project_name = config.get('project_name', 'MCU')
            self.logger.info(f"使用配置中的项目名称: {self.project_name}")
        
        # 将相对路径转换为绝对路径（基于项目目录）
        if project_path:
            project_root = os.path.abspath(project_path)
        else:
            # 如果没有提供项目路径，使用工具目录的上级目录作为默认值
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.logger.info(f"项目根目录: {project_root}")
        self.logger.info(f"原始fw_publish路径: {self.fw_publish_directory}")
        
        if os.path.isabs(self.fw_publish_directory):
            # 如果是绝对路径，直接使用
            self.fw_publish_directory = os.path.abspath(self.fw_publish_directory)
            self.logger.info(f"绝对路径fw_publish: {self.fw_publish_directory}")
        else:
            # 如果是相对路径，基于项目根目录解析
            # ./fw_publish -> 项目目录/fw_publish
            # ../fw_publish -> 项目目录/../fw_publish
            self.fw_publish_directory = os.path.join(project_root, self.fw_publish_directory)
            self.fw_publish_directory = os.path.abspath(self.fw_publish_directory)
            self.logger.info(f"解析后的fw_publish路径: {self.fw_publish_directory}")
        
        self._ensure_fw_publish_directory()
    
    
    def _ensure_fw_publish_directory(self):
        """确保fw_publish目录存在"""
        try:
            os.makedirs(self.fw_publish_directory, exist_ok=True)
            self.logger.info(f"固件发布目录已准备: {self.fw_publish_directory}")
        except Exception as e:
            self.logger.error(f"创建固件发布目录失败: {e}")
    
    def generate_filename(self, commit_id: str, timestamp: Optional[datetime] = None, 
                         version: str = None, project_path: str = None, add_timestamp: bool = True, 
                         file_extension: str = ".bin") -> str:
        """
        生成带时间戳、commit ID和git分支的文件名
        
        Args:
            commit_id: commit ID
            timestamp: 时间戳，如果为None则使用当前时间
            version: 版本号，如果提供则包含在文件名中
            project_path: 项目路径，用于获取git分支
            add_timestamp: 是否在文件名中添加时间戳
            file_extension: 文件扩展名，默认为".bin"
            
        Returns:
            str: 生成的文件名
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # 截取短commit ID
        short_commit_id = commit_id[:8] if commit_id else "unknown"
        
        # 获取git分支名称
        branch_name = self.get_git_branch(project_path)
        
        # 生成文件名
        if add_timestamp:
            # 格式化时间戳
            time_str = timestamp.strftime("%Y%m%d_%H%M%S")
            if version:
                # 包含版本号的文件名格式: 项目名_分支名_版本号_时间戳_commitID.扩展名
                filename = f"{self.project_name}_{branch_name}_{version}_{time_str}_{short_commit_id}{file_extension}"
            else:
                # 不包含版本号的文件名格式: 项目名_分支名_时间戳_commitID.扩展名
                filename = f"{self.project_name}_{branch_name}_{time_str}_{short_commit_id}{file_extension}"
        else:
            if version:
                # 包含版本号但不包含时间戳的文件名格式: 项目名_分支名_版本号_commitID.扩展名
                filename = f"{self.project_name}_{branch_name}_{version}_{short_commit_id}{file_extension}"
            else:
                # 不包含版本号和时间戳的文件名格式: 项目名_分支名_commitID.扩展名
                filename = f"{self.project_name}_{branch_name}_{short_commit_id}{file_extension}"
        
        self.logger.info(f"生成文件名: {filename}")
        return filename
    
    def get_git_branch(self, project_path: str = None) -> str:
        """
        获取当前git分支名称
        
        Args:
            project_path: 项目路径，如果为None则使用当前目录
            
        Returns:
            str: 分支名称，如果获取失败返回"unknown"
        """
        try:
            if project_path is None:
                project_path = os.getcwd()
            
            # 使用git命令获取当前分支
            kwargs = {
                'cwd': project_path,
                'capture_output': True,
                'text': True,
                'encoding': 'utf-8',
                'errors': 'replace',
                'timeout': 10
            }
            if sys.platform == 'win32' and hasattr(subprocess, 'CREATE_NO_WINDOW'):
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                **kwargs
            )
            
            if result.returncode == 0 and result.stdout.strip():
                branch_name = result.stdout.strip()
                # 处理中文分支名，转换为安全的文件名格式
                safe_branch_name = self._sanitize_branch_name(branch_name)
                self.logger.info(f"获取到git分支: {branch_name} -> 安全格式: {safe_branch_name}")
                return safe_branch_name
            else:
                self.logger.warning("无法获取git分支，使用默认值")
                return "unknown"
                
        except Exception as e:
            self.logger.warning(f"获取git分支失败: {e}")
            return "unknown"
    
    def _sanitize_branch_name(self, branch_name: str) -> str:
        """
        将分支名转换为安全的文件名格式，保留中文
        
        Args:
            branch_name: 原始分支名
            
        Returns:
            str: 安全的文件名格式
        """
        import re
        
        # 保留中文，只处理文件名中不允许的字符
        # 替换Windows文件名中不允许的字符: < > : " | ? * \ /
        # 以及一些其他可能有问题的字符
        safe_name = re.sub(r'[<>:"|?*\\/]', '_', branch_name)
        
        # 去除首尾空格和点号
        safe_name = safe_name.strip(' .')
        
        # 如果处理后为空，使用默认值
        if not safe_name:
            return "branch"
        
        # 限制长度，避免文件名过长
        if len(safe_name) > 50:
            safe_name = safe_name[:50]
            
        return safe_name
    
    def copy_file(self, source_path: str, destination_path: str) -> bool:
        """
        复制文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            
        Returns:
            bool: 复制是否成功
        """
        try:
            # 确保目标目录存在
            dest_dir = os.path.dirname(destination_path)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
            
            # 复制文件
            shutil.copy2(source_path, destination_path)
            
            self.logger.info(f"文件复制成功: {source_path} -> {destination_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"文件复制失败: {e}")
            return False
    
    def move_file(self, source_path: str, destination_path: str) -> bool:
        """
        移动文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            
        Returns:
            bool: 移动是否成功
        """
        try:
            # 确保目标目录存在
            dest_dir = os.path.dirname(destination_path)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)
            
            # 移动文件
            shutil.move(source_path, destination_path)
            
            self.logger.info(f"文件移动成功: {source_path} -> {destination_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"文件移动失败: {e}")
            return False
    
    def rename_file(self, old_path: str, new_name: str) -> Tuple[bool, str]:
        """
        重命名文件
        
        Args:
            old_path: 原文件路径
            new_name: 新文件名
            
        Returns:
            Tuple[bool, str]: (是否成功, 新文件路径)
        """
        try:
            # 获取原文件目录
            old_dir = os.path.dirname(old_path)
            new_path = os.path.join(old_dir, new_name)
            
            # 重命名文件
            os.rename(old_path, new_path)
            
            self.logger.info(f"文件重命名成功: {old_path} -> {new_path}")
            return True, new_path
            
        except Exception as e:
            self.logger.error(f"文件重命名失败: {e}")
            return False, old_path
    
    def process_bin_file(self, source_bin_path: str, commit_id: str, 
                        timestamp: Optional[datetime] = None, version: str = None) -> Tuple[bool, str, dict]:
        """
        处理bin文件：重命名并移动到输出目录
        
        Args:
            source_bin_path: 源bin文件路径
            commit_id: commit ID
            timestamp: 时间戳
            version: 版本号
            
        Returns:
            Tuple[bool, str, dict]: (是否成功, 消息, 文件信息)
        """
        result_info = {
            'source_path': source_bin_path,
            'commit_id': commit_id,
            'timestamp': timestamp or datetime.now(),
            'version': version,
            'new_filename': None,
            'destination_path': None,
            'file_size': 0,
            'operation': 'unknown'
        }
        
        try:
            # 检查源文件是否存在
            if not os.path.exists(source_bin_path):
                return False, f"源文件不存在: {source_bin_path}", result_info
            
            result_info['file_size'] = os.path.getsize(source_bin_path)
            
            # 生成新文件名
            new_filename = self.generate_filename(commit_id, timestamp, version, self.project_path)
            result_info['new_filename'] = new_filename
            
            # 直接返回成功，不复制到输出目录
            result_info['operation'] = 'processed'
            success_msg = f"文件处理成功\n"
            success_msg += f"源文件: {source_bin_path}\n"
            success_msg += f"文件大小: {result_info['file_size']} 字节\n"
            success_msg += f"Commit ID: {commit_id}\n"
            if version:
                success_msg += f"版本号: {version}\n"
            success_msg += f"时间戳: {result_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
            
            return True, success_msg, result_info
                
        except Exception as e:
            error_msg = f"处理bin文件失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg, result_info
    
    def publish_firmware(self, source_bin_path: str, commit_id: str, version: str,
                        timestamp: Optional[datetime] = None, add_timestamp: bool = True, 
                        publish_out_file: bool = False) -> Tuple[bool, str, dict]:
        """
        发布固件到fw_publish目录
        
        Args:
            source_bin_path: 源bin文件路径
            commit_id: commit ID
            version: 版本号
            timestamp: 时间戳
            add_timestamp: 是否在文件名中添加时间戳
            publish_out_file: 是否同时发布.out文件
            
        Returns:
            Tuple[bool, str, dict]: (是否成功, 消息, 文件信息)
        """
        result_info = {
            'source_path': source_bin_path,
            'commit_id': commit_id,
            'version': version,
            'timestamp': timestamp or datetime.now(),
            'new_filename': None,
            'destination_path': None,
            'file_size': 0,
            'operation': 'publish'
        }
        
        try:
            # 检查源文件是否存在
            if not os.path.exists(source_bin_path):
                return False, f"源文件不存在: {source_bin_path}", result_info
            
            result_info['file_size'] = os.path.getsize(source_bin_path)
            
            # 生成发布文件名
            new_filename = self.generate_filename(commit_id, timestamp, version, self.project_path, add_timestamp)
            result_info['new_filename'] = new_filename
            
            # 生成发布路径
            destination_path = os.path.join(self.fw_publish_directory, new_filename)
            result_info['destination_path'] = destination_path
            
            # 复制bin文件到发布目录
            if self.copy_file(source_bin_path, destination_path):
                result_info['operation'] = 'publish'
                success_msg = f"固件发布成功\n"
                success_msg += f"源文件: {source_bin_path}\n"
                success_msg += f"发布文件: {destination_path}\n"
                success_msg += f"文件大小: {result_info['file_size']} 字节\n"
                success_msg += f"版本号: {version}\n"
                success_msg += f"Commit ID: {commit_id}\n"
                success_msg += f"时间戳: {result_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                
                # 如果需要发布.out文件
                if publish_out_file:
                    out_file_path = self._find_out_file(source_bin_path)
                    if out_file_path and os.path.exists(out_file_path):
                        # 生成.out文件名（与bin文件名相同，但扩展名为.out）
                        out_filename = new_filename.replace('.bin', '.out')
                        out_destination_path = os.path.join(self.fw_publish_directory, out_filename)
                        
                        if self.copy_file(out_file_path, out_destination_path):
                            success_msg += f"\n.out文件发布成功: {out_destination_path}"
                            self.logger.info(f".out文件发布成功: {out_file_path} -> {out_destination_path}")
                        else:
                            success_msg += f"\n.out文件发布失败: {out_file_path}"
                            self.logger.warning(f".out文件发布失败: {out_file_path}")
                    else:
                        success_msg += f"\n未找到对应的.out文件"
                        self.logger.warning(f"未找到对应的.out文件，源bin文件: {source_bin_path}")
                
                return True, success_msg, result_info
            else:
                return False, "固件发布失败", result_info
                
        except Exception as e:
            error_msg = f"发布固件失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg, result_info
    
    def _find_out_file(self, bin_file_path: str) -> Optional[str]:
        """
        根据bin文件路径查找对应的.out文件
        
        Args:
            bin_file_path: bin文件路径
            
        Returns:
            str: .out文件路径，如果未找到返回None
        """
        try:
            # 获取bin文件所在目录
            bin_dir = os.path.dirname(bin_file_path)
            bin_filename = os.path.basename(bin_file_path)
            
            # 将.bin替换为.out
            out_filename = bin_filename.replace('.bin', '.out')
            out_file_path = os.path.join(bin_dir, out_filename)
            
            if os.path.exists(out_file_path):
                self.logger.info(f"找到.out文件: {out_file_path}")
                return out_file_path
            else:
                self.logger.warning(f"未找到.out文件: {out_file_path}")
                return None
                
        except Exception as e:
            self.logger.error(f"查找.out文件失败: {e}")
            return None
    
    def list_published_firmware(self) -> List[dict]:
        """
        列出fw_publish目录中的所有固件文件
        
        Returns:
            List[dict]: 固件文件信息列表
        """
        files = []
        
        try:
            if not os.path.exists(self.fw_publish_directory):
                return files
            
            for filename in os.listdir(self.fw_publish_directory):
                file_path = os.path.join(self.fw_publish_directory, filename)
                if os.path.isfile(file_path) and filename.endswith('.bin'):
                    stat = os.stat(file_path)
                    files.append({
                        'name': filename,
                        'path': file_path,
                        'size': stat.st_size,
                        'modified_time': datetime.fromtimestamp(stat.st_mtime),
                        'created_time': datetime.fromtimestamp(stat.st_ctime)
                    })
            
            # 按修改时间排序（最新的在前）
            files.sort(key=lambda x: x['modified_time'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"列出已发布固件失败: {e}")
        
        return files
    
    def publish_to_remote(self, bin_file_path: str, release_note_path: str, branch_name: str = "main", 
                         publish_out_file: bool = False) -> Tuple[bool, str, dict]:
        """
        发布到远程目录
        
        Args:
            bin_file_path: bin文件路径
            release_note_path: release note文件路径
            branch_name: 分支名称
            publish_out_file: 是否同时发布.out文件
            
        Returns:
            Tuple[bool, str, dict]: (成功标志, 消息, 结果信息)
        """
        result_info = {
            'remote_directory': '',
            'bin_file_copied': False,
            'release_note_copied': False,
            'out_file_copied': False,
            'files': []
        }
        
        try:
            # 标准化路径
            self.remote_publish_directory = os.path.normpath(self.remote_publish_directory)
            self.logger.info(f"远程发布目录配置: '{self.remote_publish_directory}'")
            
            if not self.remote_publish_directory:
                return False, "远程发布目录未配置", result_info
            
            if not os.path.exists(self.remote_publish_directory):
                return False, f"远程发布目录不存在: {self.remote_publish_directory}", result_info
            
            # 创建项目名称+分支名称的子目录
            sub_directory = f"{self.project_name}_{branch_name}"
            remote_sub_dir = os.path.join(self.remote_publish_directory, sub_directory)
            
            self.logger.info(f"项目名称: {self.project_name}")
            self.logger.info(f"分支名称: {branch_name}")
            self.logger.info(f"子目录名称: {sub_directory}")
            self.logger.info(f"远程子目录路径: {remote_sub_dir}")
            
            # 确保子目录存在
            os.makedirs(remote_sub_dir, exist_ok=True)
            result_info['remote_directory'] = remote_sub_dir
            
            self.logger.info(f"远程子目录创建成功: {remote_sub_dir}")
            
            # 复制bin文件
            if os.path.exists(bin_file_path):
                bin_filename = os.path.basename(bin_file_path)
                remote_bin_path = os.path.join(remote_sub_dir, bin_filename)
                
                if self.copy_file(bin_file_path, remote_bin_path):
                    result_info['bin_file_copied'] = True
                    result_info['files'].append({
                        'type': 'bin',
                        'local_path': bin_file_path,
                        'remote_path': remote_bin_path,
                        'filename': bin_filename
                    })
                    self.logger.info(f"bin文件已复制到远程目录: {remote_bin_path}")
                else:
                    return False, f"复制bin文件失败: {bin_file_path}", result_info
            else:
                return False, f"bin文件不存在: {bin_file_path}", result_info
            
            # 复制release note文件
            if os.path.exists(release_note_path):
                release_note_filename = os.path.basename(release_note_path)
                remote_release_note_path = os.path.join(remote_sub_dir, release_note_filename)
                
                if self.copy_file(release_note_path, remote_release_note_path):
                    result_info['release_note_copied'] = True
                    result_info['files'].append({
                        'type': 'release_note',
                        'local_path': release_note_path,
                        'remote_path': remote_release_note_path,
                        'filename': release_note_filename
                    })
                    self.logger.info(f"Release Notes已复制到远程目录: {remote_release_note_path}")
                else:
                    self.logger.warning(f"复制Release Notes失败: {release_note_path}")
            else:
                self.logger.warning(f"Release Notes文件不存在: {release_note_path}")
            
            # 复制.out文件（如果需要）
            if publish_out_file:
                out_file_path = self._find_out_file(bin_file_path)
                if out_file_path and os.path.exists(out_file_path):
                    out_filename = os.path.basename(out_file_path)
                    remote_out_path = os.path.join(remote_sub_dir, out_filename)
                    
                    if self.copy_file(out_file_path, remote_out_path):
                        result_info['out_file_copied'] = True
                        result_info['files'].append({
                            'type': 'out',
                            'local_path': out_file_path,
                            'remote_path': remote_out_path,
                            'filename': out_filename
                        })
                        self.logger.info(f".out文件已复制到远程目录: {remote_out_path}")
                    else:
                        self.logger.warning(f"复制.out文件失败: {out_file_path}")
                else:
                    self.logger.warning(f"未找到对应的.out文件: {bin_file_path}")
            
            success_msg = f"远程发布成功\n"
            success_msg += f"远程目录: {remote_sub_dir}\n"
            success_msg += f"bin文件: {'已复制' if result_info['bin_file_copied'] else '复制失败'}\n"
            success_msg += f"Release Notes: {'已复制' if result_info['release_note_copied'] else '复制失败'}\n"
            if publish_out_file:
                success_msg += f".out文件: {'已复制' if result_info['out_file_copied'] else '复制失败'}\n"
            success_msg += f"文件数量: {len(result_info['files'])}"
            
            return True, success_msg, result_info
            
        except Exception as e:
            error_msg = f"远程发布失败: {e}"
            self.logger.error(error_msg)
            return False, error_msg, result_info
    
    def backup_file(self, file_path: str, backup_suffix: str = ".backup") -> Tuple[bool, str]:
        """
        备份文件
        
        Args:
            file_path: 要备份的文件路径
            backup_suffix: 备份文件后缀
            
        Returns:
            Tuple[bool, str]: (是否成功, 备份文件路径)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"文件不存在: {file_path}"
            
            backup_path = file_path + backup_suffix
            if self.copy_file(file_path, backup_path):
                return True, backup_path
            else:
                return False, "备份失败"
                
        except Exception as e:
            self.logger.error(f"备份文件失败: {e}")
            return False, f"备份异常: {e}"


def test_file_manager():
    """测试文件管理器功能"""
    # 测试配置
    test_config = {
        'project_name': 'TEST_MCU'
    }
    
    manager = FileManager(test_config)
    
    print("文件管理器测试")
    print(f"项目名称: {manager.project_name}")
    
    # 测试文件名生成
    test_commit_id = "a1b2c3d4e5f6"
    filename = manager.generate_filename(test_commit_id, project_path=".")
    print(f"生成的文件名: {filename}")
    
    # 获取目录信息
    dir_info = manager.get_directory_info()
    print(f"目录信息: {dir_info}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_file_manager()
