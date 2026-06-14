"""截图工具"""
import os
from datetime import datetime
from pathlib import Path


class ScreenshotHelper:
    """截图辅助类"""
    
    def __init__(self, save_path="screenshots"):
        """初始化截图辅助类
        
        Args:
            save_path: 截图保存路径
        """
        self.save_path = Path(save_path)
        self.save_path.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(self, driver, name="screenshot"):
        """截取屏幕截图
        
        Args:
            driver: WebDriver 或 Appium Driver
            name: 截图名称
        
        Returns:
            截图文件路径
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{name}_{timestamp}.png"
            file_path = self.save_path / filename
            
            driver.save_screenshot(str(file_path))
            return str(file_path)
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def take_screenshot_on_failure(self, driver, test_name):
        """测试失败时截图
        
        Args:
            driver: WebDriver 或 Appium Driver
            test_name: 测试名称
        """
        return self.take_screenshot(driver, f"failure_{test_name}")
    
    def take_screenshot_on_success(self, driver, test_name):
        """测试成功时截图
        
        Args:
            driver: WebDriver 或 Appium Driver
            test_name: 测试名称
        """
        return self.take_screenshot(driver, f"success_{test_name}")
