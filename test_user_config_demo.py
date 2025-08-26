"""
User类配置文件功能演示
演示如何从配置文件加载用户和保存用户数据
"""

from core.user import User
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
    
    def get_products_info(self):
        return self.products.copy()
    
    def sell_product(self, product):
        if product in self.products and self.products[product]["stock"] > 0:
            self.products[product]["stock"] -= 1
            return True
        return False

def test_user_config_functionality():
    """测试User类的配置文件功能"""
    
    print("=== User类配置文件功能测试 ===\n")
    
    # 创建模拟售卖机
    vending_machine = MockVendingMachine()
    
    # 1. 从配置文件加载现有用户
    print("1. 从配置文件加载用户:")
    try:
        user_zhangsan = User.from_config("config/user_zhangsan.yaml")
        print(f"加载用户: {user_zhangsan}")
        print(f"用户余额: ¥{user_zhangsan.balance:.2f}")
        print(f"历史记录数量: {len(user_zhangsan.history)}")
        print()
    except Exception as e:
        print(f"加载用户失败: {e}")
        return
    
    # 2. 查看用户购买记录
    print("2. 查看用户购买记录:")
    user_zhangsan.view_history()
    print()
    
    # 3. 用户购买商品（会自动保存到配置文件）
    print("3. 用户购买商品:")
    user_zhangsan.buy("矿泉水", vending_machine)
    print()
    
    # 4. 用户充值（会自动保存到配置文件）
    print("4. 用户充值:")
    user_zhangsan.add_balance(20.0)
    print()
    
    # 5. 创建新用户
    print("5. 创建新用户:")
    new_user = User.create_new_user("赵六", balance=30.0)
    print(f"新用户: {new_user}")
    print(f"配置文件: {new_user.config_file}")
    print()
    
    # 6. 新用户购买商品
    print("6. 新用户购买商品:")
    new_user.view_products(vending_machine)
    new_user.buy("可乐", vending_machine)
    new_user.buy("雪碧", vending_machine)
    print()
    
    # 7. 查看新用户信息
    print("7. 新用户最终信息:")
    info = new_user.get_info()
    print(f"姓名: {info['name']}")
    print(f"余额: ¥{info['balance']:.2f}")
    print(f"交易次数: {len(info['history'])}")
    print(f"配置文件: {info['config_file']}")
    print()
    
    # 8. 重新加载用户验证数据持久化
    print("8. 重新加载用户验证数据持久化:")
    try:
        reloaded_user = User.from_config("config/user_zhangsan.yaml")
        print(f"重新加载的用户: {reloaded_user}")
        print("最新购买记录:")
        reloaded_user.view_history()
    except Exception as e:
        print(f"重新加载用户失败: {e}")

if __name__ == "__main__":
    test_user_config_functionality()