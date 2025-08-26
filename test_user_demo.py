"""
User类功能演示
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
            "矿泉水": {"price": 2.0, "stock": 0}  # 库存为0用于测试
        }
    
    def get_products_info(self):
        return self.products.copy()
    
    def sell_product(self, product):
        if product in self.products and self.products[product]["stock"] > 0:
            self.products[product]["stock"] -= 1
            return True
        return False

def test_user_functionality():
    """测试User类的各种功能"""
    
    # 创建用户
    user = User("张三", balance=20.0)
    
    # 创建模拟售卖机
    vending_machine = MockVendingMachine()
    
    print("=== User类功能测试 ===\n")
    
    # 1. 查看用户信息
    print("1. 用户信息:")
    print(user)
    print()
    
    # 2. 查看商品
    print("2. 查看商品:")
    user.view_products(vending_machine)
    print()
    
    # 3. 购买商品 - 成功
    print("3. 购买商品 - 可乐:")
    user.buy("可乐", vending_machine)
    print()
    
    # 4. 购买商品 - 余额不足
    print("4. 购买商品 - 多次购买测试余额:")
    user.buy("橙汁", vending_machine)  # 4.0
    user.buy("橙汁", vending_machine)  # 4.0
    user.buy("橙汁", vending_machine)  # 4.0 - 应该余额不足
    print()
    
    # 5. 充值
    print("5. 充值测试:")
    user.add_balance(10.0)
    print()
    
    # 6. 购买库存为0的商品
    print("6. 购买库存为0的商品:")
    user.buy("矿泉水", vending_machine)
    print()
    
    # 7. 查看购买记录
    print("7. 查看购买记录:")
    user.view_history()
    print()
    
    # 8. 获取用户信息
    print("8. 用户最终信息:")
    info = user.get_info()
    print(f"姓名: {info['name']}")
    print(f"余额: ¥{info['balance']:.2f}")
    print(f"交易次数: {len(info['history'])}")

if __name__ == "__main__":
    test_user_functionality()