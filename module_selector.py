#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QA自动化测试框架 - 测试模块选择器
根据测试类型选择对应的测试模块并执行
"""

import os
import sys
import subprocess
from pathlib import Path
from enum import Enum

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import setup_logger

logger = setup_logger(__name__)


class TestModule(Enum):
    """测试模块枚举"""
    WEB_UI = "web_ui"
    API = "api"
    APP = "app"
    PERFORMANCE = "performance"
    ALL = "all"


class ModuleSelector:
    """测试模块选择器"""

    MODULE_CONFIG = {
        TestModule.WEB_UI: {
            "name": "Web & UI 功能测试",
            "test_dirs": ["tests/web", "tests/functional"],
            "marker": "web or functional",
            "description": """
🌐 Web & UI 功能测试模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

测试能力:
  ✅ Selenium Web自动化测试 (Chrome/Firefox)
  ✅ Page Object Model 页面对象模式
  ✅ 功能测试 (登录、仪表板、搜索、登出)
  ✅ 参数化数据驱动测试
  ✅ 失败自动截图
  ✅ 响应式设计测试

适用场景:
  • Vue/React 前端应用
  • 用户登录/注册流程
  • 表单提交和验证
  • 页面导航和交互
            """,
        },
        TestModule.API: {
            "name": "API 接口测试",
            "test_dirs": ["tests/api"],
            "marker": "api",
            "description": """
🔌 API 接口测试模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

测试能力:
  ✅ RESTful API 测试 (GET/POST/PUT/DELETE)
  ✅ 请求/响应验证
  ✅ 状态码和响应头验证
  ✅ Mock 数据测试
  ✅ 错误处理测试
  ✅ 冒烟测试

支持后端:
  • Python (Django/Flask/FastAPI)
  • Node.js (Express/NestJS)
  • Java (Spring Boot)
  • Go (Gin/Gorm)
            """,
        },
        TestModule.APP: {
            "name": "App 自动化测试",
            "test_dirs": ["tests/app"],
            "marker": "app",
            "description": """
📱 App 自动化测试模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

测试能力:
  ✅ Appium 移动端自动化测试
  ✅ Android 应用测试 (UiAutomator2)
  ✅ iOS 应用测试 (XCUITest)
  ✅ Native/Hybrid 应用测试

前置条件:
  • Appium Server 运行中
  • 模拟器/真机已连接
  • .env 中配置 APPIUM_HOST/PORT
            """,
        },
        TestModule.PERFORMANCE: {
            "name": "性能测试",
            "test_dirs": ["tests/performance"],
            "marker": "performance",
            "description": """
⚡ 性能测试模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

测试能力:
  ✅ Locust 负载测试
  ✅ 并发用户模拟
  ✅ 响应时间分析
  ✅ 压力测试

运行方式:
   locust -f tests/performance/locustfile.py --host=http://localhost:8000
            """,
        },
        TestModule.ALL: {
            "name": "全部测试",
            "test_dirs": ["tests/web", "tests/functional", "tests/api", "tests/app", "tests/performance"],
            "marker": "",
            "description": """
🚀 全部测试模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

运行所有可用测试，生成完整测试报告
            """,
        },
    }

    def __init__(self):
        self.selected_module = None

    def print_header(self):
        """打印欢迎信息"""
        print("\n" + "=" * 80)
        print("🚀 QA自动化测试框架 - 模块选择器")
        print("=" * 80)
        print()
        print("选择要运行的测试模块:")
        print()

    def print_modules(self):
        """打印可用模块"""
        print("  1️⃣  Web & UI 功能测试")
        print("       Selenium + Page Object Model")
        print("       包含: 功能测试、Web自动化、截图")
        print()
        print("  2️⃣  API 接口测试")
        print("       requests + pytest")
        print("       包含: RESTful API、Mock测试、错误处理")
        print()
        print("  3️⃣  App 自动化测试")
        print("       Appium (需要Appium Server)")
        print("       包含: Android/iOS、跨平台测试")
        print()
        print("  4️⃣  性能测试")
        print("       Locust 负载测试")
        print("       包含: 并发模拟、压力测试")
        print()
        print("  5️⃣  全部测试")
        print("       运行所有模块")
        print()
        print("  0️⃣  退出")
        print()

    def select_module(self):
        """选择测试模块"""
        self.print_header()
        self.print_modules()

        while True:
            choice = input("请输入选择 (0-5): ").strip()

            mapping = {
                "1": TestModule.WEB_UI,
                "2": TestModule.API,
                "3": TestModule.APP,
                "4": TestModule.PERFORMANCE,
                "5": TestModule.ALL,
            }

            if choice == "0":
                logger.info("👋 退出测试框架")
                return False
            elif choice in mapping:
                self.selected_module = mapping[choice]
                logger.info(f"✅ 已选择: {self.MODULE_CONFIG[mapping[choice]]['name']}")
                return True
            else:
                print("❌ 无效的选择，请重新输入\n")

    def show_module_details(self):
        """显示模块详细信息"""
        config = self.MODULE_CONFIG[self.selected_module]
        print(config["description"])
        print()

    def show_available_tests(self):
        """显示可用的测试文件"""
        config = self.MODULE_CONFIG[self.selected_module]
        print("=" * 80)
        print("发现的测试文件:")
        print("=" * 80)

        found_any = False
        for test_dir in config["test_dirs"]:
            test_path = PROJECT_ROOT / test_dir
            if test_path.exists():
                test_files = list(test_path.glob("test_*.py"))
                if test_files:
                    found_any = True
                    print(f"\n📂 {test_dir}/")
                    for tf in test_files:
                        print(f"   📄 {tf.name}")

        if not found_any:
            print("   ⚠️  未发现测试文件（目录存在但无测试脚本）")
        print()

    def run_module_tests(self):
        """运行选中模块的测试"""
        config = self.MODULE_CONFIG[self.selected_module]
        test_dirs = config["test_dirs"]
        marker = config["marker"]

        print("\n" + "=" * 80)
        print(f"🚀 运行: {config['name']}")
        print("=" * 80)

        # 只运行存在且有测试文件的目录
        existing_dirs = []
        for test_dir in test_dirs:
            test_path = PROJECT_ROOT / test_dir
            if test_path.exists() and list(test_path.glob("test_*.py")):
                existing_dirs.append(test_dir)

        if not existing_dirs:
            print("\n⚠️  没有找到可运行的测试文件")
            print("请先编写测试用例到对应目录\n")
            return

        report_dir = PROJECT_ROOT / "reports" / "html"
        report_dir.mkdir(parents=True, exist_ok=True)
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")

        for test_dir in existing_dirs:
            print(f"\n📂 {test_dir}/")
            cmd = [
                sys.executable, "-m", "pytest", test_dir, "-v", "--tb=short",
                f"--html={report_dir}/report_{timestamp}.html",
                "--self-contained-html",
            ]
            if marker:
                cmd.extend(["-m", marker])

            try:
                result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
                if result.returncode == 0:
                    logger.info(f"✅ {test_dir} 测试通过")
                else:
                    logger.warning(f"⚠️ {test_dir} 测试有失败项")
            except Exception as e:
                logger.error(f"❌ {test_dir} 执行失败: {e}")

        print("\n" + "=" * 80)
        print(f"✅ {config['name']} 测试完成")
        print(f"📂 报告位置: {report_dir}")
        print("=" * 80 + "\n")

    def print_quick_commands(self):
        """打印快速手动运行命令"""
        config = self.MODULE_CONFIG[self.selected_module]
        print("📝 手动运行命令:")
        print("=" * 80)

        test_dir = " ".join(config["test_dirs"])
        marker_flag = f' -m "{config["marker"]}"' if config["marker"] else ""

        print(f"""
  # 运行测试
  pytest {test_dir} -v{marker_flag}

  # 生成HTML报告
  pytest {test_dir} -v{marker_flag} --html=reports/html/report.html --self-contained-html

  # 生成JSON报告
  pytest {test_dir} -v{marker_flag} --json-report --json-report-file=reports/json/report.json

  # 并行运行
  pytest {test_dir} -v -n auto{marker_flag}
        """)
        print("=" * 80)


def main():
    """CLI入口点"""
    selector = ModuleSelector()

    if not selector.select_module():
        return

    selector.show_module_details()
    selector.show_available_tests()
    selector.print_quick_commands()

    run = input("\n是否立即运行测试? (Y/n): ").strip().lower()
    if run in ("", "y", "yes"):
        selector.run_module_tests()

    print("\n✨ 模块选择完成！\n")


if __name__ == "__main__":
    main()
