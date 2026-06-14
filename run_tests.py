#!/usr/bin/env python
"""测试运行脚本 - 一键运行所有测试和生成报告"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from utils.logger import setup_logger
from utils.report import ReportGenerator

logger = setup_logger(__name__)


def run_pytest(test_path, markers=None, report_type="html"):
    """运行pytest
    
    Args:
        test_path: 测试路径
        markers: pytest标记
        report_type: 报告类型
    """
    logger.info(f"\n{'='*80}")
    logger.info(f"🚀 开始执行测试: {test_path}")
    logger.info(f"{'='*80}\n")
    
    cmd = ["pytest", test_path, "-v", "--tb=short"]
    
    if markers:
        cmd.extend(["-m", markers])
    
    if report_type == "html":
        report_file = f"reports/html/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        cmd.extend(["--html=" + report_file, "--self-contained-html"])
    elif report_type == "json":
        report_file = f"reports/json/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        cmd.extend(["--json-report", f"--json-report-file={report_file}"])
    
    try:
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"❌ 测试执行失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    logger.info("\n" + "#"*80)
    logger.info("# QA自动化测试框架 - 一键测试")
    logger.info("#"*80 + "\n")
    
    # 创建报告目录
    Path("reports/html").mkdir(parents=True, exist_ok=True)
    Path("reports/json").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    
    # 运行功能测试
    logger.info("\n📋 执行功能测试...")
    functional_pass = run_pytest("tests/functional", markers="functional", report_type="html")
    
    # 运行Web测试
    logger.info("\n🌐 执行Web测试...")
    web_pass = run_pytest("tests/web", markers="web", report_type="html")
    
    # 运行API测试
    logger.info("\n🔌 执行API测试...")
    api_pass = run_pytest("tests/api", markers="api", report_type="html")
    
    # 生成最终报告
    logger.info("\n" + "="*80)
    logger.info("📊 生成测试报告")
    logger.info("="*80)
    
    results = {
        "功能测试": "✅ 通过" if functional_pass else "❌ 失败",
        "Web测试": "✅ 通过" if web_pass else "❌ 失败",
        "API测试": "✅ 通过" if api_pass else "❌ 失败",
    }
    
    logger.info("\n📈 测试汇总:")
    for test_type, result in results.items():
        logger.info(f"  {test_type}: {result}")
    
    logger.info(f"\n📂 报告位置: {os.path.abspath('reports')}")
    logger.info("\n✅ 所有测试执行完成!\n")


def main():
    """CLI入口点"""
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        run_pytest(test_path)
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
