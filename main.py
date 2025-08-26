from core.machine.vending_machine import Vending_machine
from core.user.user import User
from core.admin.admin import Admin
from core.exceptions.exceptions import VendingMachineError
from core.exceptions.exceptions import InvalidSelectionError, OutOfStockError, InsufficientBalanceError
import json
import os

def user_menu(user, vm):
    """用户界面"""
    while True:
        print(f"\n=== 用户界面 ({user.name}, 余额: {user.balance} 元) ===")
        print("1. 查看所有商品")
        print("2. 购买商品")
        print("3. 查看购买记录")
        print("0. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            inventory = vm.get_inventory()
            print("\n=== 商品列表 ===")
            for item in inventory:
                print(f"{item['name']}: ¥{item['price']} (库存: {item['quantity']})")
        elif choice == "2":
            product_name = input("输入要购买的商品名: ")
            try:
                result = vm.sell_product(user, product_name)
                print(result)
            except InvalidSelectionError as e:
                print(f"输入错误: {e}")
            except OutOfStockError as e:
                print(f"缺货: {e}")
            except InsufficientBalanceError as e:
                print(f"余额不足: {e}")
            except VendingMachineError as e:
                print(f"其他售货机错误: {e}")
        elif choice == "3":
            print("\n=== 购买记录 ===")
            if not hasattr(user, 'history') or not user.history:
                print("暂无购买记录")
            else:
                for item in user.history:
                    print(f"- {item}")
        elif choice == "0":
            break
        else:
            print("无效选择，请重新输入！")


def admin_menu(admin, vm):
    """管理员界面"""
    while True:
        print(f"\n=== 管理员界面 ({admin.name}) ===")
        print("1. 查看库存")
        print("2. 查看今日卖出记录")
        print("3. 查看今日利润")
        print("0. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            inventory = vm.get_inventory()
            print("\n=== 库存列表 ===")
            for item in inventory:
                print(f"{item['name']}: ¥{item['price']} (库存: {item['quantity']})")
        elif choice == "2":
            sales = vm.get_sales()
            print("\n=== 今日销售记录 ===")
            if not sales:
                print("今日暂无销售")
            else:
                for sale in sales:
                    print(f"{sale['time']} - {sale['user']} 购买 {sale['product']} (¥{sale['price']})")
        elif choice == "3":
            profit = vm.get_profit()
            print(f"今日利润: {profit} 元")
        elif choice == "0":
            break
        else:
            print("无效选择，请重新输入！")


def load_products():
    """从配置文件加载商品数据"""
    try:
        products_path = "config/products/products.json"
        if not os.path.exists(products_path):
            # 如果文件不存在，创建示例数据
            inventory = [
                {"name": "可乐", "price": 3.5, "quantity": 10, "cost_price": 2.0},
                {"name": "雪碧", "price": 3.0, "quantity": 8, "cost_price": 1.8},
                {"name": "矿泉水", "price": 2.0, "quantity": 15, "cost_price": 1.0},
                {"name": "橙汁", "price": 4.0, "quantity": 5, "cost_price": 2.5}
            ]
            # 确保目录存在
            os.makedirs(os.path.dirname(products_path), exist_ok=True)
            # 保存示例数据
            with open(products_path, 'w', encoding='utf-8') as f:
                json.dump(inventory, f, ensure_ascii=False, indent=2)
        else:
            # 从文件加载数据
            with open(products_path, 'r', encoding='utf-8') as f:
                inventory = json.load(f)
        return inventory
    except Exception as e:
        print(f"加载商品数据失败: {e}")
        # 返回默认数据
        return [
            {"name": "可乐", "price": 3.5, "quantity": 10, "cost_price": 2.0},
            {"name": "雪碧", "price": 3.0, "quantity": 8, "cost_price": 1.8}
        ]


if __name__ == "__main__":
    # 1. 初始化售货机
    inventory = load_products()
    vm = Vending_machine(inventory=inventory, sales_today=[], profit_today=0.0)

    # 2. 登录选择
    print("=== 欢迎使用饮料售货机 ===")
    role = input("请选择身份 (user/admin): ")

    if role == "user":
        name = input("请输入用户名: ")
        user = User(name, 100.0)  
        user_menu(user, vm)

    elif role == "admin":
        password = input("请输入管理员密码: ")
        admin = Admin("system_admin", password)
        admin_menu(admin, vm)

    else:
        print("无效身份，退出程序。")