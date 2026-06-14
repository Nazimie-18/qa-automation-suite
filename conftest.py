"""全局conftest配置文件"""
import os
import sys
import pytest
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import setup_logger
from utils.screenshot import ScreenshotHelper
from utils.config import get, get_browser_config

# 初始化日志
logger = setup_logger(__name__)


def pytest_configure(config):
    """pytest启动时执行"""
    logger.info("="*80)
    logger.info("QA Automation Suite 测试框架启动")
    logger.info(f"项目路径: {PROJECT_ROOT}")
    logger.info(f"环境: {get('environment', 'dev')}")
    logger.info(f"浏览器: {get('BROWSER', 'chrome')}")
    logger.info("="*80)


def pytest_collection_modifyitems(config, items):
    """修改收集的测试项"""
    for item in items:
        # 自动标记测试
        if "web" in item.nodeid:
            item.add_marker(pytest.mark.web)
        if "app" in item.nodeid:
            item.add_marker(pytest.mark.app)
        if "api" in item.nodeid:
            item.add_marker(pytest.mark.api)
        if "functional" in item.nodeid:
            item.add_marker(pytest.mark.functional)
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行后处理"""
    outcome = yield
    report = outcome.get_result()
    
    # 测试失败时截图
    if report.when == "call" and report.failed:
        logger.error(f"❌ 测试失败: {item.name}")
        # 如果有driver fixture，进行截图
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                try:
                    screenshot_helper = ScreenshotHelper()
                    screenshot_path = screenshot_helper.take_screenshot(
                        driver, 
                        f"failure_{item.name}"
                    )
                    logger.info(f"📷 截图已保存: {screenshot_path}")
                except Exception as e:
                    logger.error(f"截图失败: {e}")


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    """测试套件级别的初始化和清理"""
    logger.info("\n🚀 测试套件开始执行...")
    
    # 创建必要的目录
    os.makedirs("reports/html", exist_ok=True)
    os.makedirs("reports/json", exist_ok=True)
    os.makedirs("reports/allure", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    yield
    
    logger.info("\n✅ 测试套件执行完成")


@pytest.fixture
def test_name(request):
    """获取当前测试名称"""
    return request.node.name


@pytest.fixture
def test_description(request):
    """获取当前测试的描述信息"""
    return request.node.obj.__doc__ if request.node.obj else "No description"
