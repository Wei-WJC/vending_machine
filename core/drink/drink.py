from ast import main
import os
import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.logger import get_logger

logger = get_logger("drink")


class Drink:
    """饮料类"""

    def __init__(self, name: str, price: float = 0.0, cost: float = 0.0):
        """
        初始化饮料

        Args:
            name: 饮料名字
            price: 售卖价格
            cost: 成本价
        """
        self.name = name
        self.price = price
        self.cost = cost

        logger.info(f"饮料 {self.name} 初始化完成")

    def __str__(self):
        """
        打印饮料信息
        
        returns:
            Drink:饮料信息

        """
        logger.info(f'饮料名称{self.name}，售卖价格{self.price},进货价{self.cost}')


if __name__ == '__main__':
    # drink = Drink(name='wjc', price=5.0, cost=2.5)
    # drink = Drink.__init__(name='wjc', price=5.0, cost=2.5)
    drink = Drink(name='wjc', price=5.0, cost=2.5)
    print(drink.name)
    # print(drink.name)
    # print(drink.__str__())
