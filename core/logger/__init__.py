"""
日志系统包初始化文件
提供统一的日志接口
"""

from .logger import (
    get_logger,
    set_log_level,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)

# 默认导出
__all__ = [
    'get_logger',
    'set_log_level',
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL'
]
