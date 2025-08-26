class InventoryManager:
    def __init__(self, vending_machine):
        self.vm = vending_machine

    def check_low_stock(self):
        """打印库存不足的商品"""
        print("\n=== 库存检查 ===")
        has_low = False
        for drink in self.vm.products:
            if drink.quantity <= 2:
                print(f"{drink.name} 库存不足，仅剩 {drink.quantity} 瓶")
                has_low = True
        if not has_low:
            print("所有库存充足")

    def auto_restock(self):
        """库存不足时，直接补货到10"""
        print("\n=== 自动补货 ===")
        for drink in self.vm.products:
            if drink.quantity <= 2:
                print(f"自动补货: {drink.name} -> 10 瓶")
                drink.quantity = 10

    def show_report(self):
        """直接打印库存报表"""
        print("\n=== 库存报表 ===")
        for drink in self.vm.products:
            print(f"{drink.name}: {drink.quantity} 瓶 (售价 ¥{drink.price})")
