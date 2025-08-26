"""
Admin类功能演示
演示管理员功能：查看库存、销售记录、利润等
"""

from core.admin import Admin, AdminManager
from core.user import User, UserManager
from core.logger import get_logger

# 创建一个模拟的售卖机类用于测试
class MockVendingMachine:
    def __init__(self):
        self.products = {
            "可乐": {"price": 3.5, "stock": 10},
            "雪碧": {"price": 3.0, "stock": 5},
            "橙汁": {"price": 4.0, "stock": 8},
            "矿泉水": {"price": 2.0, "stock": 3}
        }
        
        # 模拟今日销售记录
        self.today_sales = [
            {"timestamp": "2025-08-23 09:30:00", "product": "可乐", "price": 3.5, "user": "张三"},
            {"timestamp": "2025-08-23 10:15:00", "product": "雪碧", "price": 3.0, "user": "李四"},
            {"timestamp": "2025-08-23 11:20:00", "product": "橙汁", "price": 4.0, "user": "王五"},
            {"timestamp": "2025-08-23 14:30:00", "product": "可乐", "price": 3.5, "user": "赵六"},
            {"timestamp": "2025-08-23 15:45:00", "product": "矿泉水", "price": 2.0, "user": "孙七"},
        ]
    
    def get_products_info(self):
        return self.products.copy()
    
    def get_today_sales(self):
        return self.today_sales.copy()
    
    def sell_product(self, product):
        if product in self.products and self.products[product]["stock"] > 0:
            self.products[product]["stock"] -= 1
            return True
        return False

def test_admin_functionality():
    """测试Admin类的各种功能"""
    
    print("=== Admin类功能测试 ===\n")
    
    # 创建管理员管理器
    admin_manager = AdminManager()
    
    # 1. 显示管理员摘要
    print("1. 管理员摘要:")
    admin_manager.print_admins_summary()
    print()
    
    # 2. 管理员登录
    print("2. 管理员登录测试:")
    admin = admin_manager.authenticate_admin("admin", "admin123")
    if admin:
        print(f"登录成功: {admin}")
    else:
        print("登录失败")
        return
    print()
    
    # 创建模拟售卖机
    vending_machine = MockVendingMachine()
    
    # 3. 查看商品库存
    print("3. 查看商品库存:")
    admin.view_inventory(vending_machine)
    print()
    
    # 4. 查看今日销售记录
    print("4. 查看今日销售记录:")
    admin.view_sales(vending_machine)
    print()
    
    # 5. 查看今日利润
    print("5. 查看今日利润:")
    admin.view_profit(vending_machine)
    print()
    
    # 6. 查看特定商品库存
    print("6. 查看特定商品库存:")
    admin.check_product(vending_machine, "可乐")
    print()
    
    # 7. 查看不存在的商品
    print("7. 查看不存在的商品:")
    admin.check_product(vending_machine, "咖啡")
    print()
    
    # 8. 测试错误密码登录
    print("8. 测试错误密码登录:")
    failed_admin = admin_manager.authenticate_admin("admin", "wrong_password")
    if failed_admin:
        print("登录成功（不应该发生）")
    else:
        print("登录失败（正确行为）")
    print()
    
    # 9. 获取管理员信息
    print("9. 获取管理员信息:")
    admin_info = admin_manager.get_admin_info("admin")
    if admin_info:
        print(f"管理员信息: {admin_info}")
    print()

def test_config_structure():
    """测试新的配置文件结构"""
    
    print("=== 配置文件结构测试 ===\n")
    
    # 测试用户管理器（新路径）
    print("1. 测试用户管理器（新路径）:")
    user_manager = UserManager()  # 现在默认使用 config/users
    user_manager.print_users_summary()
    print()
    
    # 测试加载用户
    print("2. 测试加载用户:")
    user = user_manager.load_user("张三")
    if user:
        print(f"成功加载用户: {user}")
        print(f"配置文件路径: {user.config_file}")
    print()

if __name__ == "__main__":
    test_admin_functionality()
    print("\n" + "="*50 + "\n")
    test_config_structure()