"""
Logger utility for the story collection system
"""

import os
import logging
from typing import Any
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 设置日志级别
        logger.setLevel(logging.INFO)
    
    return logger

def log_operation(logger: logging.Logger, operation: str, status: str, details: str = None):
    """记录操作日志
    
    Args:
        logger: 日志记录器
        operation: 操作名称
        status: 操作状态
        details: 详细信息
    """
    message = f"操作: {operation} - 状态: {status}"
    if details:
        message += f" - 详情: {details}"
    logger.info(message)

def log_exception(logger: logging.Logger, exception: Exception, context: str = None):
    """记录异常日志
    
    Args:
        logger: 日志记录器
        exception: 异常对象
        context: 上下文信息
    """
    message = f"异常: {type(exception).__name__} - {str(exception)}"
    if context:
        message = f"{context} - {message}"
    logger.error(message)

def setup_logger(name):
    """Setup logger with file and console handlers"""
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # File handler
    log_file = os.path.join(
        logs_dir,
        f'notion_integration_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 