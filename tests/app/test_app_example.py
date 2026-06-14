"""App自动化测试示例"""
import pytest
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.mark.app
@pytest.mark.android
class TestAppExample:
    """App测试示例（需要Appium服务运行）"""

    def test_app_launch(self, appium_driver):
        """验证应用启动"""
        driver = appium_driver
        activity = driver.current_activity
        logger.info(f"当前Activity: {activity}")
        assert activity is not None, "应用应已启动"

    def test_element_presence(self, appium_driver):
        """验证界面元素存在"""
        driver = appium_driver
        source = driver.page_source
        assert len(source) > 0, "页面源码不应为空"

    @pytest.mark.smoke
    def test_app_basic_health(self, appium_driver):
        """冒烟测试 - 应用基本健康检查"""
        driver = appium_driver
        assert driver.session_id is not None, "应有有效会话"
