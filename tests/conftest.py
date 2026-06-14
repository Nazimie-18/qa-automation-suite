"""测试通用配置 - 全局fixture定义"""
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.logger import setup_logger

logger = setup_logger(__name__)

# 加载环境变量
load_dotenv()

# 设置默认值
os.environ.setdefault("ENVIRONMENT", "dev")
os.environ.setdefault("BROWSER", "chrome")
os.environ.setdefault("HEADLESS", "False")


@pytest.fixture(scope="function")
def driver():
    """Web驱动器fixture - 根据环境变量BROWSER动态选择浏览器

    Chrome: 使用Selenium内置Selenium Manager自动匹配ChromeDriver版本
    Firefox: 使用webdriver-manager自动下载GeckoDriver
    """
    browser_name = os.environ.get("BROWSER", "chrome").lower()
    is_headless = os.environ.get("HEADLESS", "False").lower() == "true"

    logger.info(f"🚀 初始化浏览器: {browser_name} (headless={is_headless})")

    if browser_name == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager
        from selenium.webdriver.firefox.service import Service as FirefoxService

        options = FirefoxOptions()
        if is_headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")

        # Selenium 4.x 内置 Selenium Manager，自动下载匹配的ChromeDriver
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    if not is_headless and browser_name != "firefox":
        driver.maximize_window()

    yield driver

    logger.info("🔒 关闭浏览器")
    driver.quit()
