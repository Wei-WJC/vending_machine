"""
用户管理器模块
管理多个用户，提供用户的创建、加载、列表等功能
"""

import os
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path
from .user import User
from core.logger import get_logger

logger = get_logger("user_manager")


class UserManager:
    """用户管理器类"""
    
    def __init__(self, config_dir: str = "config/users"):
        """
        初始化用户管理器
        
        Args:
            config_dir: 用户配置文件目录
        """
        self.config_dir = config_dir
        # 确保配置目录存在
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"用户管理器初始化，配置目录: {config_dir}")
    
    def list_users(self) -> List[str]:
        """
        列出所有用户名
        
        Returns:
            List[str]: 用户名列表
        """
        try:
            users = []
            # 遍历配置目录中的所有yaml文件
            for file in os.listdir(self.config_dir):
                if file.startswith("user_") and file.endswith(".yaml"):
                    # 从文件名中提取用户名
                    user_name = file[5:-5]  # 去掉"user_"前缀和".yaml"后缀
                    users.append(user_name)
            
            logger.info(f"找到 {len(users)} 个用户")
            return users
        except Exception as e:
            logger.error(f"列出用户失败: {e}")
            return []
    
    def load_user(self, name: str) -> Optional[User]:
        """
        加载特定用户
        
        Args:
            name: 用户名
            
        Returns:
            Optional[User]: 用户实例，如果不存在则返回None
        """
        try:
            # 构建配置文件路径
            safe_name = name.replace(" ", "_").replace(".", "_")
            config_file = os.path.join(self.config_dir, f"user_{safe_name}.yaml")
            
            if os.path.exists(config_file):
                user = User.from_config(config_file)
                logger.info(f"成功加载用户: {name}")
                return user
            else:
                logger.warning(f"未找到用户: {name}")
                return None
        except Exception as e:
            logger.error(f"加载用户 {name} 失败: {e}")
            return None
    
    def create_user(self, name: str, balance: float = 0.0) -> Optional[User]:
        """
        创建新用户
        
        Args:
            name: 用户名
            balance: 初始余额
            
        Returns:
            Optional[User]: 新创建的用户实例，如果用户已存在则返回None
        """
        try:
            # 检查用户是否已存在
            if self.load_user(name) is not None:
                logger.warning(f"用户 {name} 已存在")
                return None
            
            # 创建新用户
            user = User.create_new_user(name=name, balance=balance, config_dir=self.config_dir)
            logger.info(f"成功创建用户: {name}")
            return user
        except Exception as e:
            logger.error(f"创建用户 {name} 失败: {e}")
            return None
    
    def delete_user(self, name: str) -> bool:
        """
        删除用户
        
        Args:
            name: 用户名
            
        Returns:
            bool: 删除是否成功
        """
        try:
            # 构建配置文件路径
            safe_name = name.replace(" ", "_").replace(".", "_")
            config_file = os.path.join(self.config_dir, f"user_{safe_name}.yaml")
            
            if os.path.exists(config_file):
                os.remove(config_file)
                logger.info(f"成功删除用户: {name}")
                return True
            else:
                logger.warning(f"未找到用户: {name}")
                return False
        except Exception as e:
            logger.error(f"删除用户 {name} 失败: {e}")
            return False
    
    def get_users_info(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有用户的信息
        
        Returns:
            Dict[str, Dict[str, Any]]: 用户信息字典，键为用户名，值为用户信息
        """
        try:
            users_info = {}
            user_names = self.list_users()
            
            for name in user_names:
                user = self.load_user(name)
                if user:
                    info = user.get_info()
                    users_info[user.name] = {
                        "balance": info["balance"],
                        "transactions": len(info["history"]),
                        "config_file": info["config_file"]
                    }
            
            logger.info(f"获取了 {len(users_info)} 个用户的信息")
            return users_info
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            return {}
    
    def print_users_summary(self) -> None:
        """打印所有用户的摘要信息"""
        try:
            users_info = self.get_users_info()
            
            print(f"=== 用户摘要 (共 {len(users_info)} 个) ===")
            for name, info in users_info.items():
                print(f"{name}: 余额 ¥{info['balance']:.2f}, 交易次数: {info['transactions']}")
        except Exception as e:
            logger.error(f"打印用户摘要失败: {e}")
            print(f"获取用户摘要失败: {e}")


if __name__ == "__main__":
    # 简单测试
    manager = UserManager()
    users = manager.list_users()
    print(f"找到 {len(users)} 个用户: {users}")