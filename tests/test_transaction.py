"""
交易系统单元测试
"""

import unittest
from datetime import datetime
from core.transaction import Transaction, TransactionManager
from core.user.user import User
import tempfile
import os
import shutil

class TestTransaction(unittest.TestCase):
    """交易类测试"""
    
    def test_transaction_creation(self):
        """测试交易创建"""
        transaction = Transaction("123", "张三", "可乐", 3.5)
        self.assertEqual(transaction.transaction_id, "123")
        self.assertEqual(transaction.user_name, "张三")
        self.assertEqual(transaction.product_name, "可乐")
        self.assertEqual(transaction.amount, 3.5)
        self.assertEqual(transaction.status, "完成")
    
    def test_transaction_to_dict(self):
        """测试交易转换为字典"""
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        transaction = Transaction("123", "张三", "可乐", 3.5, timestamp)
        data = transaction.to_dict()
        
        self.assertEqual(data["transaction_id"], "123")
        self.assertEqual(data["user_name"], "张三")
        self.assertEqual(data["product_name"], "可乐")
        self.assertEqual(data["amount"], 3.5)
        self.assertEqual(data["timestamp"], "2023-01-01 12:00:00")
        self.assertEqual(data["status"], "完成")
    
    def test_transaction_from_dict(self):
        """测试从字典创建交易"""
        data = {
            "transaction_id": "123",
            "user_name": "张三",
            "product_name": "可乐",
            "amount": 3.5,
            "timestamp": "2023-01-01 12:00:00",
            "status": "完成"
        }
        
        transaction = Transaction.from_dict(data)
        self.assertEqual(transaction.transaction_id, "123")
        self.assertEqual(transaction.user_name, "张三")
        self.assertEqual(transaction.product_name, "可乐")
        self.assertEqual(transaction.amount, 3.5)
        self.assertEqual(transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "2023-01-01 12:00:00")
        self.assertEqual(transaction.status, "完成")


class TestTransactionManager(unittest.TestCase):
    """交易管理器测试"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.test_dir = tempfile.mkdtemp()
        self.transaction_manager = TransactionManager(self.test_dir)
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_create_transaction(self):
        """测试创建交易"""
        transaction = self.transaction_manager.create_transaction("张三", "可乐", 3.5)
        
        self.assertEqual(transaction.user_name, "张三")
        self.assertEqual(transaction.product_name, "可乐")
        self.assertEqual(transaction.amount, 3.5)
        self.assertEqual(len(self.transaction_manager.transactions), 1)
    
    def test_get_user_transactions(self):
        """测试获取用户交易"""
        self.transaction_manager.create_transaction("张三", "可乐", 3.5)
        self.transaction_manager.create_transaction("李四", "矿泉水", 2.0)
        self.transaction_manager.create_transaction("张三", "雪碧", 3.0)
        
        transactions = self.transaction_manager.get_user_transactions("张三")
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].product_name, "可乐")
        self.assertEqual(transactions[1].product_name, "雪碧")
    
    def test_daily_report(self):
        """测试每日报告"""
        # 创建今天的交易
        self.transaction_manager.create_transaction("张三", "可乐", 3.5)
        self.transaction_manager.create_transaction("李四", "矿泉水", 2.0)
        self.transaction_manager.create_transaction("张三", "可乐", 3.5)
        
        report = self.transaction_manager.get_daily_report()
        
        self.assertEqual(report["total_transactions"], 3)
        self.assertEqual(report["total_amount"], 9.0)
        self.assertEqual(report["product_stats"]["可乐"]["count"], 2)
        self.assertEqual(report["product_stats"]["可乐"]["amount"], 7.0)
        self.assertEqual(report["product_stats"]["矿泉水"]["count"], 1)
        self.assertEqual(report["product_stats"]["矿泉水"]["amount"], 2.0)
    
    def test_process_payment(self):
        """测试处理支付"""
        # 创建模拟用户和售货机
        user = User(name="张三", balance=10.0)
        
        class MockVendingMachine:
            def sell_product(self, product_name):
                return True
        
        mock_machine = MockVendingMachine()
        
        # 测试成功支付
        success = self.transaction_manager.process_payment(user, "可乐", 3.5, mock_machine)
        self.assertTrue(success)
        self.assertEqual(user.balance, 6.5)
        self.assertEqual(len(user.history), 1)
        
        # 测试余额不足
        success = self.transaction_manager.process_payment(user, "高级饮料", 10.0, mock_machine)
        self.assertFalse(success)
        self.assertEqual(user.balance, 6.5)  # 余额不变
        self.assertEqual(len(user.history), 1)  # 历史不变


if __name__ == "__main__":
    unittest.main()