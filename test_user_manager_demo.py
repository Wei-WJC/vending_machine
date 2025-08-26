"""
用户管理器功能演示
演示如何使用UserManager管理多个用户
"""

from core.user import User, UserManager
from core.logger import get_logger

def test_user_manager():
    """测试用户管理器功能"""
    
    print("=== 用户管理器功能测试 ===\n")
    
    # 创建用户管理器
    user_manager = UserManager()
    
    # 1. 显示所有用户摘要
    print("1. 当前所有用户摘要:")
    user_manager.print_users_summary()
    print()
    
    # 2. 列出所有用户名
    print("2. 所有用户名列表:")
    users = user_manager.list_users()
    for user in users:
        print(f"- {user}")
    print()
    
    # 3. 加载特定用户
    print("3. 加载特定用户:")
    user = user_manager.load_user("张三")
    if user:
        print(f"成功加载用户: {user}")
        user.view_history()
    else:
        print("用户不存在")
    print()
    
    # 4. 创建新用户
    print("4. 创建新用户:")
    new_user = user_manager.create_user("孙七", balance=50.0)
    if new_user:
        print(f"成功创建用户: {new_user}")
    print()
    
    # 5. 尝试创建重复用户
    print("5. 尝试创建重复用户:")
    duplicate_user = user_manager.create_user("张三", balance=100.0)
    print()
    
    # 6. 获取所有用户信息
    print("6. 所有用户详细信息:")
    users_info = user_manager.get_users_info()
    for name, info in users_info.items():
        print(f"{name}:")
        print(f"  余额: ¥{info['balance']:.2f}")
        print(f"  交易次数: {info['transactions']}")
        print(f"  配置文件: {info['config_file']}")
    print()
    
    # 7. 最终用户摘要
    print("7. 最终用户摘要:")
    user_manager.print_users_summary()

if __name__ == "__main__":
    test_user_manager()