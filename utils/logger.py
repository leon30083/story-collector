"""
日志工具模块
提供日志记录功能
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 导入配置
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import LOGS_DIR, LOG_FORMAT, LOG_LEVEL

def get_logger(name='story_collector'):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logger: 配置好的日志记录器实例
    """
    # 创建日志文件名，使用日期时间
    log_filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(LOGS_DIR, log_filename)
    
    # 确保日志目录存在
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 设置日志级别
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 如果已经配置了处理器，则不再添加
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_filepath, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def log_exception(logger, exception, context=None):
    """
    记录异常信息
    
    Args:
        logger: 日志记录器
        exception: 异常对象
        context: 上下文信息
    """
    if context:
        logger.error(f"发生错误 - 上下文: {context}")
    logger.exception(exception)
    
def log_operation(logger, operation, status, details=None):
    """
    记录操作信息
    
    Args:
        logger: 日志记录器
        operation: 操作名称
        status: 操作状态
        details: 详细信息
    """
    message = f"操作: {operation} - 状态: {status}"
    if details:
        message += f" - 详情: {details}"
    
    if status.lower() == "成功":
        logger.info(message)
    elif status.lower() == "警告":
        logger.warning(message)
    elif status.lower() == "失败":
        logger.error(message)
    else:
        logger.debug(message) 