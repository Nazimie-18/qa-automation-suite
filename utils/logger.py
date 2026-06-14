"""日志工具"""
import logging
import os
from datetime import datetime
import colorlog
from pathlib import Path

# 日志输出目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(name, log_file=None, level=logging.DEBUG):
    """配置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 移除现有的处理器
    logger.handlers.clear()
    
    # 控制台处理器 - 彩色输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s]%(reset)s [%(levelname)-8s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file is None:
        log_file = LOG_DIR / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-8s] %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


# 创建全局日志记录器
logger = setup_logger(__name__)
