"""
用户类模块
管理用户信息、余额和购买记录
支持从配置文件加载和保存用户数据
"""

import os
import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.logger import get_logger

logger = get_logger("user")


class User:
    """用户类"""
    
    def __init__(self, name: str, balance: float = 0.0, history: Optional[List[Dict[str, Any]]] = None,
                 config_file: Optional[str] = None):
        """
        初始化用户
        
        Args:
            name: 用户姓名
            balance: 用户余额
            history: 购买记录列表
            config_file: 配置文件路径
        """
        self.name = name
        self.balance = balance
        self.history = history if history is not None else []
        self.config_file = config_file
        
        logger.info(f"用户 {self.name} 初始化完成，余额: {self.balance}")
    
    @classmethod
    def from_config(cls, config_file: str) -> 'User':
        """
        从配置文件创建用户实例
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            User: 用户实例
        """
        try:
            config_path = Path(config_file)
            if not config_path.exists():
                logger.error(f"配置文件不存在: {config_file}")
                raise FileNotFoundError(f"配置文件不存在: {config_file}")
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            user_data = config.get('user', {})
            name = user_data.get('name', '')
            balance = user_data.get('balance', 0.0)
            history = user_data.get('history', [])
            
            logger.info(f"从配置文件 {config_file} 加载用户 {name}")
            return cls(name=name, balance=balance, history=history, config_file=config_file)
            
        except Exception as e:
            logger.error(f"从配置文件加载用户失败: {e}")
            raise
    
    @classmethod
    def create_new_user(cls, name: str, balance: float = 0.0, config_dir: str = "config") -> 'User':
        """
        创建新用户并生成配置文件
        
        Args:
            name: 用户姓名
            balance: 初始余额
            config_dir: 配置文件目录
            
        Returns:
            User: 用户实例
        """
        # 生成配置文件名（将中文名转换为拼音或使用安全的文件名）
        safe_name = name.replace(" ", "_").replace(".", "_")
        config_file = os.path.join(config_dir, f"user_{safe_name}.yaml")
        
        user = cls(name=name, balance=balance, history=[], config_file=config_file)
        user.save_to_config()
        
        logger.info(f"创建新用户 {name}，配置文件: {config_file}")
        return user
    
    def save_to_config(self) -> bool:
        """
        保存用户数据到配置文件
        
        Returns:
            bool: 保存是否成功
        """
        if not self.config_file:
            logger.warning(f"用户 {self.name} 没有指定配置文件")
            return False
        
        try:
            config_data = {
                'user': {
                    'name': self.name,
                    'balance': self.balance,
                    'history': self.history
                }
            }
            
            # 确保目录存在
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.info(f"用户 {self.name} 数据已保存到 {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存用户 {self.name} 配置文件失败: {e}")
            return False
    
    def view_products(self, vending_machine) -> Dict[str, float]:
        """
        查看所有饮料的名称和售价
        
        Args:
            vending_machine: 售卖机实例
            
        Returns:
            Dict[str, float]: 商品名称和价格的字典
        """
        try:
            products = vending_machine.get_products_info()
            logger.info(f"用户 {self.name} 查看商品列表")
            
            print(f"\n=== {self.name} 查看商品列表 ===")
            for product_name, info in products.items():
                print(f"{product_name}: ¥{info['price']:.2f} (库存: {info['stock']})")
            
            return {name: info['price'] for name, info in products.items()}
            
        except Exception as e:
            logger.error(f"用户 {self.name} 查看商品列表失败: {e}")
            return {}
    
    def buy(self, product: str, vending_machine) -> bool:
        """
        购买饮料
        
        Args:
            product: 商品名称
            vending_machine: 售卖机实例
            
        Returns:
            bool: 购买是否成功
        """
        try:
            logger.info(f"用户 {self.name} 尝试购买 {product}")
            
            # 获取商品信息
            products_info = vending_machine.get_products_info()
            if product not in products_info:
                logger.warning(f"商品 {product} 不存在")
                print(f"商品 {product} 不存在！")
                return False
            
            product_info = products_info[product]
            price = product_info['price']
            stock = product_info['stock']
            
            # 检查库存
            if stock <= 0:
                logger.warning(f"商品 {product} 库存不足")
                print(f"商品 {product} 库存不足！")
                return False
            
            # 检查余额
            if self.balance < price:
                logger.warning(f"用户 {self.name} 余额不足，当前余额: {self.balance}, 商品价格: {price}")
                print(f"余额不足！当前余额: ¥{self.balance:.2f}, 商品价格: ¥{price:.2f}")
                return False
            
            # 执行购买
            success = vending_machine.sell_product(product)
            if success:
                # 更新余额
                self.balance -= price
                
                # 记录交易
                transaction_record = {
                    "product": product,
                    "price": price,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.history.append(transaction_record)
                
                # 保存到配置文件
                self.save_to_config()
                
                logger.info(f"用户 {self.name} 成功购买 {product}, 花费: {price}, 剩余余额: {self.balance}")
                print(f"购买成功！{product} ¥{price:.2f}, 剩余余额: ¥{self.balance:.2f}")
                return True
            else:
                logger.error(f"售卖机出货失败: {product}")
                print("售卖机出货失败，请联系管理员")
                return False
                
        except Exception as e:
            logger.error(f"用户 {self.name} 购买 {product} 时发生错误: {e}")
            print(f"购买过程中发生错误: {e}")
            return False
    
    def add_balance(self, amount: float) -> bool:
        """
        充值余额
        
        Args:
            amount: 充值金额
            
        Returns:
            bool: 充值是否成功
        """
        if amount <= 0:
            logger.warning(f"用户 {self.name} 尝试充值无效金额: {amount}")
            print("充值金额必须大于0")
            return False
        
        self.balance += amount
        self.save_to_config()  # 保存到配置文件
        
        logger.info(f"用户 {self.name} 充值 {amount}, 当前余额: {self.balance}")
        print(f"充值成功！充值金额: ¥{amount:.2f}, 当前余额: ¥{self.balance:.2f}")
        return True
    
    def view_history(self) -> List[Dict[str, Any]]:
        """
        查看购买记录
        
        Returns:
            List[Dict[str, Any]]: 购买记录列表
        """
        logger.info(f"用户 {self.name} 查看购买记录")
        
        print(f"\n=== {self.name} 的购买记录 ===")
        if not self.history:
            print("暂无购买记录")
        else:
            for i, record in enumerate(self.history, 1):
                print(f"{i}. {record['product']} - ¥{record['price']:.2f} - {record['timestamp']}")
        
        return self.history.copy()
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取用户信息
        
        Returns:
            Dict[str, Any]: 用户信息字典
        """
        return {
            "name": self.name,
            "balance": self.balance,
            "history": self.history.copy(),
            "config_file": self.config_file
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"User(name='{self.name}', balance={self.balance:.2f}, transactions={len(self.history)})"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return f"User(name='{self.name}', balance={self.balance}, history={self.history}, config_file='{self.config_file}')"


if __name__ == '__main__':
    user = User(name="wjc", balance=1.0)
    print(user.__repr__())
