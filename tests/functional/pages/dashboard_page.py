"""仪表板页面对象"""
from selenium.webdriver.common.by import By
from tests.functional.pages.base_page import BasePage
from utils.logger import setup_logger
from utils.config import get_api_config

logger = setup_logger(__name__)


class DashboardPage(BasePage):
    """仪表板页面"""

    # 定位器
    USER_PROFILE = (By.CLASS_NAME, "user-profile")
    LOGOUT_BUTTON = (By.ID, "logout_btn")
    SEARCH_BOX = (By.ID, "search_input")
    SEARCH_BUTTON = (By.ID, "search_btn")
    RESULTS_LIST = (By.CLASS_NAME, "results-list")

    @property
    def DASHBOARD_URL(self):
        api_config = get_api_config("python")
        base_url = api_config.get("base_url", "http://localhost:8000")
        return f"{base_url}/dashboard"
    
    def open_dashboard(self):
        """打开仪表板"""
        logger.info("📖 打开仪表板")
        self.open(self.DASHBOARD_URL)
    
    def is_dashboard_loaded(self):
        """检查仪表板是否加载
        
        Returns:
            True/False
        """
        return self.is_element_visible(*self.USER_PROFILE, timeout=10)
    
    def search(self, keyword):
        """执行搜索
        
        Args:
            keyword: 搜索关键词
        """
        logger.info(f"🔍 搜索: {keyword}")
        self.input_text(*self.SEARCH_BOX, keyword)
        self.click(*self.SEARCH_BUTTON)
    
    def get_search_results_count(self):
        """获取搜索结果数量
        
        Returns:
            结果数量
        """
        results = self.find_elements(*self.RESULTS_LIST)
        return len(results)
    
    def logout(self):
        """执行登出"""
        logger.info("🚪 执行登出")
        self.click(*self.LOGOUT_BUTTON)
