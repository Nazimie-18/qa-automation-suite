"""测试报告生成工具"""
import json
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Template


class ReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, report_dir="reports"):
        """初始化报告生成器
        
        Args:
            report_dir: 报告输出目录
        """
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_html_report(self, test_results, filename=None):
        """生成HTML报告
        
        Args:
            test_results: 测试结果列表
            filename: 报告文件名
        
        Returns:
            报告文件路径
        """
        if filename is None:
            filename = f"report_{self.timestamp}.html"
        
        html_dir = self.report_dir / "html"
        html_dir.mkdir(parents=True, exist_ok=True)
        
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA自动化测试报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        .stat-card .number { font-size: 32px; font-weight: bold; margin-bottom: 10px; }
        .stat-card .label { color: #666; font-size: 14px; }
        .stat-card.passed .number { color: #52c41a; }
        .stat-card.failed .number { color: #f5222d; }
        .stat-card.skipped .number { color: #faad14; }
        .stat-card.total .number { color: #1890ff; }
        .test-list { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .test-item { padding: 15px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; justify-content: space-between; }
        .test-item:last-child { border-bottom: none; }
        .test-name { flex: 1; }
        .test-status { padding: 5px 10px; border-radius: 4px; font-weight: bold; }
        .status-passed { background: #f6ffed; color: #52c41a; }
        .status-failed { background: #fff1f0; color: #f5222d; }
        .status-skipped { background: #fffbe6; color: #faad14; }
        .footer { text-align: center; color: #999; margin-top: 30px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 QA自动化测试报告</h1>
            <p>生成时间: {{ timestamp }}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card total">
                <div class="number">{{ total }}</div>
                <div class="label">总测试数</div>
            </div>
            <div class="stat-card passed">
                <div class="number">{{ passed }}</div>
                <div class="label">通过</div>
            </div>
            <div class="stat-card failed">
                <div class="number">{{ failed }}</div>
                <div class="label">失败</div>
            </div>
            <div class="stat-card skipped">
                <div class="number">{{ skipped }}</div>
                <div class="label">跳过</div>
            </div>
        </div>
        
        <div class="test-list">
            {% for result in results %}
            <div class="test-item">
                <div class="test-name">{{ result.name }}</div>
                <div class="test-status status-{{ result.status }}">{{ result.status.upper() }}</div>
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p>© 2024 QA Automation Suite | 更多信息请访��文档</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        passed = sum(1 for r in test_results if r.get('status') == 'passed')
        failed = sum(1 for r in test_results if r.get('status') == 'failed')
        skipped = sum(1 for r in test_results if r.get('status') == 'skipped')
        total = len(test_results)
        
        html_content = template.render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            results=test_results
        )
        
        report_path = html_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(report_path)
    
    def generate_json_report(self, test_results, filename=None):
        """生成JSON报告
        
        Args:
            test_results: 测试结果列表
            filename: 报告文件名
        
        Returns:
            报告文件路径
        """
        if filename is None:
            filename = f"report_{self.timestamp}.json"
        
        json_dir = self.report_dir / "json"
        json_dir.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'total': len(test_results),
            'passed': sum(1 for r in test_results if r.get('status') == 'passed'),
            'failed': sum(1 for r in test_results if r.get('status') == 'failed'),
            'skipped': sum(1 for r in test_results if r.get('status') == 'skipped'),
            'results': test_results
        }
        
        report_path = json_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return str(report_path)
