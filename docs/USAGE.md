# QA Automation Suite 使用指南

## 快速开始

```bash
# 1. 安装
pip install -e .                    # 基础安装
pip install -e .[web,api,all]       # 含可选依赖

# 2. 配置
cp .env.example .env               # 复制环境配置
# 编辑 .env 设置 BROWSER, HEADLESS, API_URL 等

# 3. 运行
qa-run                             # 一键运行所有测试
qa-module-selector                 # 交互式选择模块
pytest tests/api -v                # 运行指定目录
```

## 测试模块

| 目录 | 类型 | 前置条件 |
|------|------|----------|
| `tests/functional/` | POM功能测试 | 目标服务器运行中 |
| `tests/web/` | Web自动化 | Chrome/Firefox |
| `tests/api/` | API接口测试 | 无（使用Mock） |
| `tests/app/` | App自动化 | Appium Server |
| `tests/performance/` | 性能测试 | 目标服务器运行中 |

## 配置说明

### 环境变量 (.env)

```ini
BROWSER=chrome          # chrome | firefox
HEADLESS=False          # True = 无头模式
PYTHON_API_URL=...      # API服务地址
APPIUM_HOST=localhost   # Appium服务器地址
```

### 配置文件 (config/config.yaml)

完整的浏览器、API、数据库、报告等配置。优先级：环境变量 > config.yaml > 默认值。

## 报告生成

```bash
# HTML报告（含饼图/统计）
pytest tests/api -v --html=reports/html/report.html --self-contained-html

# JSON报告
pytest tests/api -v --json-report --json-report-file=reports/json/report.json

# Allure报告
pytest tests/api -v --alluredir=reports/allure
allure serve reports/allure
```

## 自定义 Page Object

```python
from selenium.webdriver.common.by import By
from tests.functional.pages.base_page import BasePage

class MyPage(BasePage):
    MY_ELEMENT = (By.ID, "my_element")

    def do_action(self):
        self.click(*self.MY_ELEMENT)
```

## 自定义测试用例

```python
import pytest

@pytest.mark.smoke
class TestMyFeature:
    def test_something(self, driver):
        # 使用全局 driver fixture
        driver.get("https://example.com")
        assert driver.title != ""
```

## CI/CD 集成

```yaml
# GitHub Actions
- name: Run tests
  run: |
    pip install -e .[api]
    pytest tests/api -v
```
