from ast import main
import os
import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.logger import get_logger
from core.exceptions.exceptions import (
    InvalidSelectionError,
    OutOfStockError,
    InsufficientBalanceError
)

logger = get_logger("drink")


class Vending_machine:
    """售卖机类"""

    def __init__(self, inventory: List[Dict[str, Any]], sales_today: List[Dict[str, Any]], profit_today: float = 0.0):
        """
        初始化售卖机

        Args:
            inventory: 库存
            sales_today: 今日卖出清单
            profit_today: 今日利润

        """
        self.inventory = inventory
        self.sales_today = sales_today
        self.profit_today = profit_today

        logger.info(f"库存{self.inventory}初始化完成，今日卖出清单{self.sales_today},今日利润{self.profit_today}")

    def add_product(self, drink: str, quantity: int):
        """
        上架饮料
        
        returns:
           上架饮料

        """
        logger.info(f'上架饮料{drink},数量{quantity}')

    def sell_product(self, user, drink_name: str):
        """
        用户购买饮料逻辑：
        1. 检查商品是否存在
        2. 检查库存是否足够
        3. 检查用户余额是否足够
        4. 扣除库存，扣钱，记录销售，更新利润
        """
        # 找商品
        product = next((item for item in self.inventory if item["name"] == drink_name), None)
        if not product:
            logger.error(f"商品 {drink_name} 不存在")
            raise InvalidSelectionError(f"商品 {drink_name} 不存在")

        # 检查库存
        if product["quantity"] <= 0:
            logger.warning(f"商品 {drink_name} 缺货")
            raise OutOfStockError(f"{drink_name} 已售罄")

        # 检查余额
        if user.balance < product["price"]:
            logger.warning(f"用户 {user.name} 余额不足（余额:{user.balance}, 价格:{product['price']}）")
            raise InsufficientBalanceError(f"{user.name} 余额不足")

        # 正常购买流程
        product["quantity"] -= 1
        user.balance -= product["price"]
        user.purchase_history.append(drink_name)

        # 更新利润（售价 - 进货价）
        self.profit_today += (product["price"] - product["cost_price"])

        # 记录今日销售
        self.sales_today.append({
            "user": user.name,
            "product": drink_name,
            "price": product["price"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        logger.info(f"用户 {user.name} 成功购买 {drink_name}，余额 {user.balance} 元")
        return f"{user.name} 成功购买 {drink_name}"

    def get_profit(self):
        """
        返回今日利润

        returns:
            返回今日利润

        """
        logger.info(f'今日利润{self.profit_today}')
        return self.profit_today
        
    def get_sales(self):
        """
        返回今日销售记录

        returns:
            返回今日销售记录

        """
        logger.info(f'今日销售记录{self.sales_today}')
        return self.sales_today
    
    def get_inventory(self):
        """
        返回库存信息

        returns:
            返回库存信息

        """
        logger.info(f'库存信息{self.inventory}')
        return self.inventory