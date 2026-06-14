"""App自动化测试配置 - Appium驱动"""
import pytest
from utils.logger import setup_logger
from utils.config import get

logger = setup_logger(__name__)


@pytest.fixture(scope="function")
def appium_driver():
    """Appium驱动器fixture（示例，需要Appium服务器运行）"""
    appium_host = get("APPIUM_HOST", "localhost")
    appium_port = get("APPIUM_PORT", "4723")

    logger.info(f"📱 初始化Appium驱动: {appium_host}:{appium_port}")

    try:
        from appium import webdriver

        desired_caps = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": "emulator-5554",
            "appPackage": "com.example.app",
            "appActivity": ".MainActivity",
            "autoGrantPermissions": True,
        }
        driver = webdriver.Remote(
            f"http://{appium_host}:{appium_port}/wd/hub", desired_caps
        )
        driver.implicitly_wait(10)
        yield driver
        logger.info("🔒 关闭Appium会话")
        driver.quit()
    except Exception as e:
        pytest.skip(f"Appium服务不可用: {e}")
