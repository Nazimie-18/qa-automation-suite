"""通用工具函数"""
import time
import random
import string
from datetime import datetime, timedelta


def wait_time(seconds):
    """等待指定时间
    
    Args:
        seconds: 等待秒数
    """
    time.sleep(seconds)


def get_random_string(length=10):
    """生成随机字符串
    
    Args:
        length: 字符串长度
    
    Returns:
        随机字符串
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_random_email():
    """生成随机邮箱
    
    Returns:
        随机邮箱地址
    """
    return f"{get_random_string()}@test.com"


def get_random_phone():
    """生成随机电话号码
    
    Returns:
        随机电话号码
    """
    return ''.join(random.choices(string.digits, k=11))


def get_random_number(start=1, end=1000):
    """生成随机数字
    
    Args:
        start: 起始数字
        end: 结束数字
    
    Returns:
        随机数字
    """
    return random.randint(start, end)


def get_current_timestamp():
    """获取当前时间戳
    
    Returns:
        当前时间戳（秒）
    """
    return int(time.time())


def get_current_datetime(format_str="%Y-%m-%d %H:%M:%S"):
    """获取当前日期时间
    
    Args:
        format_str: 时间格式
    
    Returns:
        格式化后的当前时间
    """
    return datetime.now().strftime(format_str)


def get_future_date(days=1, format_str="%Y-%m-%d"):
    """获取未来日期
    
    Args:
        days: 天数
        format_str: 时间格式
    
    Returns:
        未来日期
    """
    future_date = datetime.now() + timedelta(days=days)
    return future_date.strftime(format_str)


def get_past_date(days=1, format_str="%Y-%m-%d"):
    """获取过去日期
    
    Args:
        days: 天数
        format_str: 时间格式
    
    Returns:
        过去日期
    """
    past_date = datetime.now() - timedelta(days=days)
    return past_date.strftime(format_str)


def retry_operation(func, max_retries=3, delay=1, *args, **kwargs):
    """重试操作
    
    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        delay: 重试延迟（秒）
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        函数执行结果
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
    return None
