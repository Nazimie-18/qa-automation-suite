"""Web自动化测试示例"""
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logger import setup_logger

logger = setup_logger(__name__)

# 本地测试页面路径
TEST_PAGE = os.path.join(os.path.dirname(__file__), "test_page.html")
TEST_URL = f"file:///{TEST_PAGE.replace(os.sep, '/').lstrip('/')}"


@pytest.mark.web
class TestWebExample:
    """Web自动化示例测试"""

    def test_page_loads(self, driver):
        """验证页面能正常加载"""
        driver.get(TEST_URL)
        assert driver.title == "QA Test Demo Page"
        logger.info(f"页面标题: {driver.title}")

    def test_form_input(self, driver):
        """验证表单元素可交互"""
        driver.get(TEST_URL)
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("testuser")
        assert username_input.get_attribute("value") == "testuser"

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("mypassword")
        assert password_input.get_attribute("value") == "mypassword"

    def test_button_present(self, driver):
        """验证按钮存在且可点击"""
        driver.get(TEST_URL)
        login_btn = driver.find_element(By.ID, "login_btn")
        assert login_btn.is_enabled()
        assert login_btn.text == "登录"

    @pytest.mark.smoke
    def test_page_structure(self, driver):
        """冒烟测试 - 验证页面基本结构"""
        driver.get(TEST_URL)
        assert driver.find_element(By.TAG_NAME, "h1").text != ""
        assert driver.find_element(By.ID, "username").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()
        assert driver.find_element(By.ID, "login_btn").is_displayed()
