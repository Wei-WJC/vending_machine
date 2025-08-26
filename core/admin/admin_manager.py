"""
管理员管理器模块
提供管理员配置文件的管理功能
"""

import yaml
from typing import List, Dict, Optional
from pathlib import Path
from core.admin import Admin
from core.logger import get_logger

logger = get_logger("admin_manager")


class AdminManager:
    """管理员管理器类"""

    def __init__(self, config_file: str = "config/admin/admin_config.yaml"):
        """
        初始化管理员管理器
        
        Args:
            config_file: 管理员配置文件路径
        """
        self.config_file = config_file
        self.admins_config = self._load_config()
        logger.info(f"管理员管理器初始化完成，配置文件: {config_file}")

    def _load_config(self) -> Dict:
        """
        加载管理员配置文件
        
        Returns:
            Dict: 配置数据
        """
        try:
            config_path = Path(self.config_file)
            if not config_path.exists():
                logger.error(f"管理员配置文件不存在: {self.config_file}")
                return {"admins": [], "default_admin": {}}

            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            logger.info(f"成功加载管理员配置文件")
            return config

        except Exception as e:
            logger.error(f"加载管理员配置文件失败: {e}")
            return {"admins": [], "default_admin": {}}

    def authenticate_admin(self, username: str, password: str) -> Optional[Admin]:
        """
        验证管理员登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            Optional[Admin]: 验证成功返回Admin实例，失败返回None
        """
        try:
            admins_list = self.admins_config.get("admins", [])

            for admin_data in admins_list:
                if admin_data.get("name") == username:
                    admin = Admin(admin_data["name"], admin_data["password"])
                    if admin.authenticate(password):
                        logger.info(f"管理员 {username} 登录成功")
                        return admin
                    else:
                        logger.warning(f"管理员 {username} 密码错误")
                        return None

            logger.warning(f"管理员 {username} 不存在")
            return None

        except Exception as e:
            logger.error(f"管理员认证失败: {e}")
            return None

    def list_admins(self) -> List[str]:
        """
        列出所有管理员用户名
        
        Returns:
            List[str]: 管理员用户名列表
        """
        try:
            admins_list = self.admins_config.get("admins", [])
            usernames = [admin.get("name", "") for admin in admins_list]
            logger.info(f"获取管理员列表，共 {len(usernames)} 个管理员")
            return usernames

        except Exception as e:
            logger.error(f"获取管理员列表失败: {e}")
            return []

    def get_admin_info(self, username: str) -> Optional[Dict]:
        """
        获取管理员信息（不包含密码）
        
        Args:
            username: 管理员用户名
            
        Returns:
            Optional[Dict]: 管理员信息
        """
        try:
            admins_list = self.admins_config.get("admins", [])

            for admin_data in admins_list:
                if admin_data.get("name") == username:
                    # 返回信息但不包含密码
                    info = admin_data.copy()
                    info.pop("password", None)
                    return info

            logger.warning(f"管理员 {username} 不存在")
            return None

        except Exception as e:
            logger.error(f"获取管理员信息失败: {e}")
            return None

    def print_admins_summary(self):
        """打印所有管理员的摘要信息"""
        try:
            admins_list = self.admins_config.get("admins", [])

            if not admins_list:
                print("没有找到任何管理员")
                return

            print(f"\n=== 管理员摘要 (共 {len(admins_list)} 个管理员) ===")
            for admin_data in admins_list:
                name = admin_data.get("name", "未知")
                role = admin_data.get("role", "管理员")
                permissions = admin_data.get("permissions", [])
                print(f"{name}: {role}, 权限数量: {len(permissions)}")

        except Exception as e:
            logger.error(f"打印管理员摘要失败: {e}")
            print(f"获取管理员信息失败: {e}")


if __name__ == '__main__':
    adminManager = AdminManager()
