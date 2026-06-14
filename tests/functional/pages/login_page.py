"""登录页面对象"""
from selenium.webdriver.common.by import By
from tests.functional.pages.base_page import BasePage
from utils.logger import setup_logger
from utils.config import get_api_config

logger = setup_logger(__name__)


class LoginPage(BasePage):
    """登录页面"""

    # 定位器
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login_btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")

    @property
    def LOGIN_URL(self):
        api_config = get_api_config("python")
        base_url = api_config.get("base_url", "http://localhost:8000")
        return f"{base_url}/login"
    
    def open_login_page(self):
        """打开登录页面"""
        logger.info("📖 打开登录页面")
        self.open(self.LOGIN_URL)
    
    def login(self, username, password):
        """执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        """
        logger.info(f"🔐 执行登录操作: username={username}")
        self.input_text(*self.USERNAME_INPUT, username)
        self.input_text(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)
    
    def get_error_message(self):
        """获取错误信息
        
        Returns:
            错误信息文本
        """
        if self.is_element_visible(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return None
    
    def is_login_success(self):
        """检查登录是否成功
        
        Returns:
            True/False
        """
        return self.is_element_visible(*self.SUCCESS_MESSAGE, timeout=5)
    
    def is_error_displayed(self):
        """检查错误信息是否显示
        
        Returns:
            True/False
        """
        return self.is_element_visible(*self.ERROR_MESSAGE, timeout=5)
