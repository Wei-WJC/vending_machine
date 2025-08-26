import datetime

class Transaction:
    def __init__(self, user_name, product_name, price):
        self.user_name = user_name
        self.product_name = product_name
        self.price = price
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"[{self.time}] {self.user_name} 购买 {self.product_name} (¥{self.price})"
