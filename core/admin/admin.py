"""
管理员类模块
提供管理员功能：查看库存、销售记录、利润等
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional
from core.logger import get_logger

logger = get_logger("admin")


class Admin:
    """管理员类"""
    
    def __init__(self, name: str, password: str):
        """
        初始化管理员
        
        Args:
            name: 管理员账号名
            password: 管理员密码
        """
        self.name = name
        self.password = password
        
        logger.info(f"管理员 {self.name} 初始化完成")
    
    def authenticate(self, input_password: str) -> bool:
        """
        验证管理员密码
        
        Args:
            input_password: 输入的密码
            
        Returns:
            bool: 验证是否成功
        """
        is_valid = self.password == input_password
        if is_valid:
            logger.info(f"管理员 {self.name} 认证成功")
        else:
            logger.warning(f"管理员 {self.name} 认证失败")
        return is_valid
    
    def view_inventory(self, vending_machine) -> Dict[str, Any]:
        """
        查看所有商品库存
        
        Args:
            vending_machine: 售卖机实例
            
        Returns:
            Dict[str, Any]: 商品库存信息
        """
        try:
            logger.info(f"管理员 {self.name} 查看商品库存")
            
            inventory = vending_machine.get_products_info()
            
            print(f"\n=== 商品库存清单 (管理员: {self.name}) ===")
            print(f"{'商品名称':<15} {'价格':<10} {'库存':<10} {'状态':<10}")
            print("-" * 50)
            
            total_products = 0
            total_value = 0
            
            for product_name, info in inventory.items():
                price = info['price']
                stock = info['stock']
                status = "正常" if stock > 0 else "缺货"
                
                print(f"{product_name:<15} ¥{price:<9.2f} {stock:<10} {status:<10}")
                
                total_products += stock
                total_value += price * stock
            
            print("-" * 50)
            print(f"总商品数量: {total_products}")
            print(f"总库存价值: ¥{total_value:.2f}")
            
            return inventory
            
        except Exception as e:
            logger.error(f"管理员 {self.name} 查看库存失败: {e}")
            print(f"查看库存失败: {e}")
            return {}
    
    def view_sales(self, vending_machine) -> List[Dict[str, Any]]:
        """
        查看今日卖出的商品清单
        
        Args:
            vending_machine: 售卖机实例
            
        Returns:
            List[Dict[str, Any]]: 今日销售记录
        """
        try:
            logger.info(f"管理员 {self.name} 查看今日销售记录")
            
            # 获取今日销售记录
            today_sales = vending_machine.get_today_sales()
            
            print(f"\n=== 今日销售清单 (管理员: {self.name}) ===")
            print(f"日期: {date.today()}")
            print(f"{'时间':<20} {'商品名称':<15} {'价格':<10} {'用户':<10}")
            print("-" * 60)
            
            total_sales = 0
            total_revenue = 0
            product_count = {}
            
            for sale in today_sales:
                timestamp = sale.get('timestamp', '')
                product = sale.get('product', '')
                price = sale.get('price', 0)
                user = sale.get('user', '未知')
                
                print(f"{timestamp:<20} {product:<15} ¥{price:<9.2f} {user:<10}")
                
                total_sales += 1
                total_revenue += price
                product_count[product] = product_count.get(product, 0) + 1
            
            print("-" * 60)
            print(f"总销售笔数: {total_sales}")
            print(f"总销售金额: ¥{total_revenue:.2f}")
            
            if product_count:
                print("\n商品销售统计:")
                for product, count in product_count.items():
                    print(f"  {product}: {count} 件")
            
            return today_sales
            
        except Exception as e:
            logger.error(f"管理员 {self.name} 查看销售记录失败: {e}")
            print(f"查看销售记录失败: {e}")
            return []
    
    def view_profit(self, vending_machine) -> float:
        """
        查看今日利润
        
        Args:
            vending_machine: 售卖机实例
            
        Returns:
            float: 今日利润
        """
        try:
            logger.info(f"管理员 {self.name} 查看今日利润")
            
            # 获取今日销售数据
            today_sales = vending_machine.get_today_sales()
            
            # 计算收入
            total_revenue = sum(sale.get('price', 0) for sale in today_sales)
            
            # 获取成本信息（假设成本是售价的60%）
            total_cost = total_revenue * 0.6
            
            # 计算利润
            profit = total_revenue - total_cost
            
            print(f"\n=== 今日利润报告 (管理员: {self.name}) ===")
            print(f"日期: {date.today()}")
            print(f"总收入: ¥{total_revenue:.2f}")
            print(f"总成本: ¥{total_cost:.2f}")
            print(f"净利润: ¥{profit:.2f}")
            print(f"利润率: {(profit/total_revenue*100 if total_revenue > 0 else 0):.1f}%")
            
            return profit
            
        except Exception as e:
            logger.error(f"管理员 {self.name} 查看利润失败: {e}")
            print(f"查看利润失败: {e}")
            return 0.0
    
    def check_product(self, vending_machine, product_name: str) -> Optional[Dict[str, Any]]:
        """
        查看某个商品库存
        
        Args:
            vending_machine: 售卖机实例
            product_name: 商品名称
            
        Returns:
            Optional[Dict[str, Any]]: 商品信息，如果不存在则返回None
        """
        try:
            logger.info(f"管理员 {self.name} 查看商品 {product_name} 的库存")
            
            inventory = vending_machine.get_products_info()
            
            if product_name not in inventory:
                print(f"商品 '{product_name}' 不存在")
                logger.warning(f"商品 {product_name} 不存在")
                return None
            
            product_info = inventory[product_name]
            price = product_info['price']
            stock = product_info['stock']
            status = "正常" if stock > 0 else "缺货"
            
            print(f"\n=== 商品详情 (管理员: {self.name}) ===")
            print(f"商品名称: {product_name}")
            print(f"单价: ¥{price:.2f}")
            print(f"库存数量: {stock}")
            print(f"库存状态: {status}")
            print(f"库存价值: ¥{price * stock:.2f}")
            
            # 获取该商品今日销售情况
            today_sales = vending_machine.get_today_sales()
            product_sales_today = [sale for sale in today_sales if sale.get('product') == product_name]
            
            print(f"今日销售: {len(product_sales_today)} 件")
            if product_sales_today:
                today_revenue = sum(sale.get('price', 0) for sale in product_sales_today)
                print(f"今日收入: ¥{today_revenue:.2f}")
            
            return product_info
            
        except Exception as e:
            logger.error(f"管理员 {self.name} 查看商品 {product_name} 失败: {e}")
            print(f"查看商品信息失败: {e}")
            return None
    
    def get_info(self) -> Dict[str, str]:
        """
        获取管理员信息
        
        Returns:
            Dict[str, str]: 管理员信息（不包含密码）
        """
        return {
            "name": self.name,
            "role": "管理员"
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Admin(name='{self.name}')"
    
    def __repr__(self) -> str:
        """详细字符串表示"""
        return f"Admin(name='{self.name}', role='管理员')"