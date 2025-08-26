"""
统一日志系统模块
提供全局日志配置和格式化功能
格式：时间 - 等级 - 文件名 - 函数名() - 行号 - 消息
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional

# 全局变量：默认日志等级
DEFAULT_LOG_LEVEL = logging.INFO

# 全局变量：日志文件路径
LOG_FILE_PATH = "logs/vending.log"

# 全局变量：日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - %(lineno)d - %(message)s"

# 全局变量：时间格式
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 便于导入的常用日志等级
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class UniversalLogger:
    """通用日志类"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(UniversalLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志系统"""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 创建logger
        self._logger = logging.getLogger('vending_machine')
        self._logger.setLevel(DEFAULT_LOG_LEVEL)
        
        # 避免重复添加handler
        if self._logger.handlers:
            return
        
        # 创建格式化器
        formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=TIME_FORMAT
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(DEFAULT_LOG_LEVEL)
        console_handler.setFormatter(formatter)
        
        # 创建文件处理器
        log_dir = Path(LOG_FILE_PATH).parent
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            LOG_FILE_PATH, 
            mode='a', 
            encoding='utf-8'
        )
        file_handler.setLevel(DEFAULT_LOG_LEVEL)
        file_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
    
    def get_logger(self):
        """获取logger实例"""
        return self._logger
    
    def set_level(self, level):
        """设置日志等级"""
        global DEFAULT_LOG_LEVEL
        DEFAULT_LOG_LEVEL = level
        self._logger.setLevel(level)
        
        # 更新所有处理器的等级
        for handler in self._logger.handlers:
            handler.setLevel(level)


# 全局logger实例
_universal_logger = UniversalLogger()


def get_logger(name: Optional[str] = None):
    """
    获取日志器实例
    
    Args:
        name: 日志器名称，如果为None则使用默认名称
    
    Returns:
        logging.Logger: 配置好的日志器实例
    """
    if name:
        # 创建子logger
        logger = logging.getLogger(f'vending_machine.{name}')
        logger.setLevel(DEFAULT_LOG_LEVEL)
        
        # 如果没有处理器，继承父logger的处理器
        if not logger.handlers:
            logger.parent = _universal_logger.get_logger()
        
        return logger
    else:
        return _universal_logger.get_logger()


def set_log_level(level):
    """
    设置全局日志等级
    
    Args:
        level: 日志等级 (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    """
    _universal_logger.set_level(level)




