"""基础页面对象类"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger
from utils.screenshot import ScreenshotHelper

logger = setup_logger(__name__)


class BasePage:
    """基础页面对象"""
    
    def __init__(self, driver):
        """初始化页面对象
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.screenshot_helper = ScreenshotHelper()
    
    def open(self, url):
        """打开URL
        
        Args:
            url: 要打开的URL
        """
        logger.info(f"📖 打开页面: {url}")
        self.driver.get(url)
    
    def find_element(self, by, value, timeout=15):
        """查找元素
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间
        
        Returns:
            WebElement
        """
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value)),
                timeout=timeout
            )
            logger.debug(f"✅ 找到元素: {by}={value}")
            return element
        except Exception as e:
            logger.error(f"❌ 未找到元素: {by}={value}")
            self.screenshot_helper.take_screenshot(self.driver, "element_not_found")
            raise
    
    def find_elements(self, by, value):
        """查找多个元素
        
        Args:
            by: 定位方式
            value: 定位值
        
        Returns:
            WebElement列表
        """
        return self.driver.find_elements(by, value)
    
    def click(self, by, value):
        """点击元素
        
        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.find_element(by, value)
        self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        logger.info(f"👆 点击元素: {by}={value}")
    
    def input_text(self, by, value, text):
        """输入文本
        
        Args:
            by: 定位方式
            value: 定位值
            text: 要输入的文本
        """
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        logger.info(f"⌨️  输入文本: {by}={value}, 内容={text}")
    
    def get_text(self, by, value):
        """获取元素文本
        
        Args:
            by: 定位方式
            value: 定位值
        
        Returns:
            元素文本
        """
        element = self.find_element(by, value)
        text = element.text
        logger.debug(f"📄 获取文本: {by}={value}, 内容={text}")
        return text
    
    def is_element_visible(self, by, value, timeout=10):
        """检查元素是否可见
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间
        
        Returns:
            True/False
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located((by, value)),
                timeout=timeout
            )
            logger.debug(f"👁️  元素可见: {by}={value}")
            return True
        except:
            logger.warning(f"⚠️  元素不可见: {by}={value}")
            return False
    
    def is_element_present(self, by, value, timeout=10):
        """检查元素是否存在
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间
        
        Returns:
            True/False
        """
        try:
            self.wait.until(
                EC.presence_of_element_located((by, value)),
                timeout=timeout
            )
            return True
        except:
            return False
    
    def wait_for_element(self, by, value, timeout=15):
        """等待元素出现
        
        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间
        """
        self.wait.until(
            EC.presence_of_element_located((by, value)),
            timeout=timeout
        )
        logger.info(f"⏳ 等待元素出现: {by}={value}")
    
    def take_screenshot(self, name="screenshot"):
        """截图
        
        Args:
            name: 截图名称
        
        Returns:
            截图路径
        """
        return self.screenshot_helper.take_screenshot(self.driver, name)
