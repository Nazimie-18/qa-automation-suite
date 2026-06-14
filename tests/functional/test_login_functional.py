"""登录功能测试"""
import pytest
from tests.functional.pages.login_page import LoginPage
from utils.common import get_random_email
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.mark.functional
@pytest.mark.web
class TestLoginFunctional:
    """登录功能测试类"""
    
    def test_login_with_valid_credentials(self, driver):
        """测试: 使用有效凭证登录
        
        这个测试验证用户能够使用正确的用户名和密码成功登录
        """
        logger.info("⏳ 开始测试: 使用有效凭证登录")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # 使用有效凭证登录
        login_page.login("admin@example.com", "password123")
        
        # 验证登录成功
        assert login_page.is_login_success(), "登录应该成功"
        logger.info("✅ 测试通过: 成功登录")
    
    def test_login_with_invalid_username(self, driver):
        """测试: 使用无效用户名登录
        
        这个测试验证用户使用无效用户名登录时显示错误信息
        """
        logger.info("⏳ 开始测试: 使用无效用户名登录")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # 使用无效用户名
        login_page.login("invalid@example.com", "password123")
        
        # 验证显示错误信息
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_msg = login_page.get_error_message()
        assert "用户名不存在" in error_msg or "Invalid" in error_msg
        logger.info(f"✅ 测试通过: 显示错误信息 - {error_msg}")
    
    def test_login_with_invalid_password(self, driver):
        """测试: 使用错误密码登录
        
        这个测试验证用户使用错误密码登录时显示错误信息
        """
        logger.info("⏳ 开始测试: 使用错误密码登录")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # 使用错误密码
        login_page.login("admin@example.com", "wrongpassword")
        
        # 验证显示错误信息
        assert login_page.is_error_displayed(), "应该显示错误信息"
        error_msg = login_page.get_error_message()
        assert "密码错误" in error_msg or "Invalid" in error_msg
        logger.info(f"✅ 测试通过: 显示错误信息 - {error_msg}")
    
    @pytest.mark.parametrize("username,password,expected_result", [
        ("admin@example.com", "password123", True),
        ("user@example.com", "user123", True),
        ("invalid@example.com", "password123", False),
        ("admin@example.com", "wrongpass", False),
    ])
    def test_login_with_multiple_credentials(self, driver, username, password, expected_result):
        """测试: 使用多个凭证进行登录
        
        这个测试使用参数化测试验证各种凭证组合
        
        Args:
            username: 用户名
            password: 密码
            expected_result: 预期结果(成功/失败)
        """
        logger.info(f"⏳ 开始测试: 登录 {username}")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(username, password)
        
        if expected_result:
            assert login_page.is_login_success(), f"登录应该成功: {username}"
            logger.info(f"✅ 测试通过: {username} 登录成功")
        else:
            assert login_page.is_error_displayed(), f"登录应该失败: {username}"
            logger.info(f"✅ 测试通过: {username} 登录失败(符合预期)")
    
    def test_login_empty_username(self, driver):
        """测试: 空用户名登录
        
        这个测试验证用户使用空用户名登录时的行为
        """
        logger.info("⏳ 开始测试: 空用户名登录")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # 使用空用户名
        login_page.login("", "password123")
        
        # 验证显示错误信息
        assert login_page.is_error_displayed(), "应该显示错误信息"
        logger.info("✅ 测试通过: 显示错误信息")
    
    def test_login_empty_password(self, driver):
        """测试: 空密码登录
        
        这个测试验证用户使用空密码登录时的行为
        """
        logger.info("⏳ 开始测试: 空密码登录")
        
        login_page = LoginPage(driver)
        login_page.open_login_page()
        
        # 使用空密码
        login_page.login("admin@example.com", "")
        
        # 验证显示错误信息
        assert login_page.is_error_displayed(), "应该显示错误信息"
        logger.info("✅ 测试通过: 显示错误信息")
