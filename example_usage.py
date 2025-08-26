"""
日志系统使用示例
演示如何在项目中使用统一的日志系统
"""

# 导入日志系统
from core.logger import get_logger, set_log_level, DEBUG, INFO

def example_module_logging():
    """使用模块特定logger的示例"""
    logger = get_logger("example_module")
    
    logger.info("模块特定的信息日志")
    logger.warning("模块特定的警告日志")
    logger.error("模块特定的错误日志")
    logger.debug("模块特定的调试日志（可能不显示）")

def example_default_logging():
    """使用默认logger的示例"""
    logger = get_logger()
    
    logger.info("默认logger的信息日志")
    logger.warning("默认logger的警告日志")
    logger.error("默认logger的错误日志")

def example_level_change():
    """演示动态改变日志等级"""
    logger = get_logger("level_test")
    
    logger.info("当前等级下的信息日志")
    logger.debug("当前等级下的调试日志（可能不显示）")
    
    # 改变日志等级为DEBUG
    set_log_level(DEBUG)
    logger.info("改变等级后的信息日志")
    logger.debug("改变等级后的调试日志（现在应该显示）")

if __name__ == "__main__":
    print("=== 日志系统使用示例 ===")
    
    print("\n1. 模块特定logger示例:")
    example_module_logging()
    
    print("\n2. 默认logger示例:")
    example_default_logging()
    
    print("\n3. 动态改变日志等级示例:")
    example_level_change()