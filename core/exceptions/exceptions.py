class VendingMachineError(Exception):
    """售卖机通用异常"""
    pass

class InsufficientBalanceError(VendingMachineError):
    """用户余额不足"""
    pass

class OutOfStockError(VendingMachineError):
    """商品缺货"""
    pass

class InvalidSelectionError(VendingMachineError):
    """用户选择了不存在的商品"""
    pass
