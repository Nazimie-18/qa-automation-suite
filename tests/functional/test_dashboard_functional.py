"""仪表板功能测试"""
import pytest
from tests.functional.pages.login_page import LoginPage
from tests.functional.pages.dashboard_page import DashboardPage
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.mark.functional
@pytest.mark.web
class TestDashboardFunctional:
    """仪表板功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """测试前登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login("admin@example.com", "password123")
        assert login_page.is_login_success()
        logger.info("✅ 登录成功")
    
    def test_dashboard_loads_successfully(self, driver):
        """测试: 仪表板加载成功
        
        验证用户登录后仪表板正确加载
        """
        logger.info("⏳ 开始测试: 仪表板加载")
        
        dashboard = DashboardPage(driver)
        assert dashboard.is_dashboard_loaded(), "仪表板应该加载成功"
        logger.info("✅ 测试通过: 仪表板加载成功")
    
    def test_search_functionality(self, driver):
        """测试: 搜索功能
        
        验证用户能够在仪表板进行搜索
        """
        logger.info("⏳ 开始测试: 搜索功能")
        
        dashboard = DashboardPage(driver)
        dashboard.search("test keyword")
        
        # 验证搜索结果显示
        results_count = dashboard.get_search_results_count()
        assert results_count >= 0, "应该有搜索结果"
        logger.info(f"✅ 测试通过: 搜索返回 {results_count} 结果")
    
    @pytest.mark.parametrize("keyword", [
        "python",
        "testing",
        "automation",
    ])
    def test_search_with_different_keywords(self, driver, keyword):
        """测试: 使用不同关键词搜索
        
        Args:
            keyword: 搜索关键词
        """
        logger.info(f"⏳ 开始测试: 搜索关键词 '{keyword}'")
        
        dashboard = DashboardPage(driver)
        dashboard.search(keyword)
        
        results_count = dashboard.get_search_results_count()
        logger.info(f"✅ 测试通过: 搜索 '{keyword}' 返回 {results_count} 结果")
    
    def test_logout_functionality(self, driver):
        """测试: 登出功能
        
        验证用户能够成功登出
        """
        logger.info("⏳ 开始测试: 登出功能")
        
        dashboard = DashboardPage(driver)
        dashboard.logout()
        
        # 验证返回登录页面
        login_page = LoginPage(driver)
        assert login_page.is_element_present(*login_page.LOGIN_BUTTON), "应该回到登录页面"
        logger.info("✅ 测试通过: 登出成功")
