"""
交易系统功能演示
演示如何使用交易系统记录交易、处理支付和生成报告
"""

from core.transaction import TransactionManager
from core.user.user import User
from core.drink.drink import Drink
from datetime import datetime, timedelta

def test_transaction_manager():
    """测试交易管理器功能"""
    
    print("=== 交易系统功能测试 ===\n")
    
    # 创建交易管理器
    transaction_manager = TransactionManager()
    
    # 1. 创建测试用户和商品
    print("1. 创建测试数据:")
    user1 = User(name="张三", balance=100.0)
    user2 = User(name="李四", balance=50.0)
    drink1 = Drink(name="可乐", price=3.5, cost=2.0)
    drink2 = Drink(name="矿泉水", price=2.0, cost=1.0)
    print(f"用户: {user1.name} (余额: ¥{user1.balance:.2f})")
    print(f"用户: {user2.name} (余额: ¥{user2.balance:.2f})")
    print(f"商品: {drink1.name} (价格: ¥{drink1.price:.2f})")
    print(f"商品: {drink2.name} (价格: ¥{drink2.price:.2f})")
    print()
    
    # 2. 创建交易
    print("2. 创建交易:")
    transaction1 = transaction_manager.create_transaction(user1.name, drink1.name, drink1.price)
    transaction2 = transaction_manager.create_transaction(user2.name, drink2.name, drink2.price)
    transaction3 = transaction_manager.create_transaction(user1.name, drink2.name, drink2.price)
    print(f"交易1: {transaction1}")
    print(f"交易2: {transaction2}")
    print(f"交易3: {transaction3}")
    print()
    
    # 3. 获取用户交易记录
    print("3. 获取用户交易记录:")
    user1_transactions = transaction_manager.get_user_transactions(user1.name)
    print(f"{user1.name}的交易记录:")
    for t in user1_transactions:
        print(f"  - {t.product_name}: ¥{t.amount:.2f} ({t.timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
    print()
    
    # 4. 生成每日报告
    print("4. 生成每日报告:")
    transaction_manager.print_daily_report()
    print()
    
    # 5. 模拟支付过程
    print("5. 模拟支付过程:")
    
    # 创建一个简单的模拟售货机对象
    class MockVendingMachine:
        def sell_product(self, product_name):
            print(f"售货机出售商品: {product_name}")
            return True
    
    mock_machine = MockVendingMachine()
    
    # 成功支付
    print("\n尝试购买可乐(¥3.5):")
    before_balance = user1.balance
    success = transaction_manager.process_payment(user1, drink1.name, drink1.price, mock_machine)
    if success:
        print(f"支付成功! {user1.name}余额: ¥{before_balance:.2f} -> ¥{user1.balance:.2f}")
    else:
        print("支付失败!")
    
    # 余额不足
    print("\n尝试购买昂贵商品(¥200):")
    before_balance = user2.balance
    success = transaction_manager.process_payment(user2, "高级饮料", 200.0, mock_machine)
    if success:
        print(f"支付成功! {user2.name}余额: ¥{before_balance:.2f} -> ¥{user2.balance:.2f}")
    else:
        print(f"支付失败! {user2.name}余额不变: ¥{user2.balance:.2f}")
    
    # 6. 再次生成报告
    print("\n6. 更新后的每日报告:")
    transaction_manager.print_daily_report()

if __name__ == "__main__":
    test_transaction_manager()