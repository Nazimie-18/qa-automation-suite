# QA Automation Suite 🚀

完整的自动化测试框架，支持Web、App、API、功能测试、性能测试及一键报告生成

## 📋 框架概述

这是一个企业级自动化测试框架，包含以下功能：

### ✨ 核心功能
- ✅ **Web自动化测试** - Selenium + Playwright (支持Vue、React前端)
- ✅ **App自动化测试** - Appium (iOS、Android、跨平台)
- ✅ **API接口测试** - pytest + requests (支持Python、Node.js、Java后端)
- ✅ **功能测试** - 完整的功能测试框架和Page Object Model
- ✅ **性能测试** - Locust (负载测试、压力测试)
- ✅ **测试用例管理** - 参数化、数据驱动、BDD支持
- ✅ **一键报告生成** - HTML、JSON、Allure美化报告
- ✅ **CI/CD集成** - GitHub Actions、Jenkins支持
- ✅ **日志与截图** - 自动截图、详细日志记录

## 📁 项目结构

```
qa-automation-suite/
├── tests/                          # 测试用例目录
│   ├── functional/                 # 功能测试
│   │   ├── conftest.py            # 功能测试配置
│   │   ├── pages/                 # Page Object Model
│   │   │   ├── base_page.py
│   │   │   ├── login_page.py
│   │   │   └── dashboard_page.py
│   │   ├── test_login_functional.py
│   │   └── test_dashboard_functional.py
│   ├── web/                        # Web自动化测试
│   ├── app/                        # App自动化测试
│   ├── api/                        # API接口测试
│   └── performance/                # 性能测试
├── config/                         # 配置文件
│   └── config.yaml                # 主配置文件
├── utils/                          # 工具类
│   ├── logger.py                  # 日志工具
│   ├── screenshot.py              # 截图工具
│   ├── common.py                  # 通用工具
│   ├── report.py                  # 报告生成
│   └── data_handler.py            # 数据处理
├── reports/                        # 报告输出
│   ├── html/                      # HTML报告
│   ├── json/                      # JSON报告
│   └── allure/                    # Allure报告
├── logs/                           # 日志输出
├── screenshots/                    # 截图输出
├── requirements.txt               # 依赖包
├── pytest.ini                     # pytest配置
├── conftest.py                    # 全局配置
├── run_tests.py                   # 一键运行脚本
└── README.md                      # 项目说明
```

## 🛠️ 安装与环境配置

### 前置条件
- Python 3.8+
- pip

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/Nazimie-18/qa-automation-suite.git
cd qa-automation-suite

# 2. 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 复制环境配置
cp .env.example .env

# 5. 编辑.env文件配置具体参数
vim .env  # 或使用你喜欢的编辑器
```

## 📝 测试用例编写

### 功能测试示例

```python
import pytest
from tests.functional.pages.login_page import LoginPage

@pytest.mark.functional
@pytest.mark.web
class TestLoginFunctional:
    def test_login_with_valid_credentials(self, driver):
        """测试使用有效凭证登录"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login("admin@example.com", "password123")
        assert login_page.is_login_success()
    
    @pytest.mark.parametrize("username,password", [
        ("user1@test.com", "pwd123"),
        ("user2@test.com", "pwd456"),
    ])
    def test_login_multiple(self, driver, username, password):
        """参数化登录测试"""
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(username, password)
        assert login_page.is_login_success()
```

### Web测试示例

```python
# 在 tests/web/ 目录下创建相似的测试
import pytest
from selenium import webdriver

@pytest.mark.web
@pytest.mark.vue
class TestVueApp:
    def test_vue_feature(self, driver):
        """Vue应用功能测试"""
        # 您的测试代码
        pass
```

### API测试示例

```python
# 在 tests/api/ 目录下创建相似的测试
import pytest
import requests

@pytest.mark.api
@pytest.mark.python
class TestPythonAPI:
    def test_get_users(self):
        """获取用户列表"""
        response = requests.get("http://localhost:8000/api/users")
        assert response.status_code == 200
```

## 🚀 运行测试

### 一键运行所有测试
```bash
python run_tests.py
```

### 运行特定类型的测试

```bash
# 功能测试
pytest tests/functional -v

# Web测试
pytest tests/web -v -m web

# App测试
pytest tests/app -v -m app

# API测试
pytest tests/api -v -m api

# 特定测试文件
pytest tests/functional/test_login_functional.py -v

# 特定测试类
pytest tests/functional/test_login_functional.py::TestLoginFunctional -v

# 特定测试方法
pytest tests/functional/test_login_functional.py::TestLoginFunctional::test_login_with_valid_credentials -v
```

### 生成测试报告

```bash
# HTML报告
pytest --html=reports/html/report.html --self-contained-html

# JSON报告
pytest --json-report --json-report-file=reports/json/report.json

# Allure报告
pytest --alluredir=reports/allure
allure serve reports/allure
```

## 📊 报告生成

测试完成后，报告会自动生成在以下位置：

- **HTML报告**: `reports/html/report_*.html`
- **JSON报告**: `reports/json/report_*.json`
- **Allure报告**: `reports/allure/`
- **日志文件**: `logs/automation_*.log`
- **截图文件**: `screenshots/`

## 🔧 配置文件说明

### config.yaml 主配置

```yaml
# 浏览器配置
browser:
  chrome:
    headless: false
    window-size: 1920x1080

# Appium配置
appium:
  host: localhost
  port: 4723
  
# API配置
api:
  timeout: 30
  retry: 3
  
# 截图配置
screenshot:
  enabled: true
  on_failure: true
  on_success: false
  
# 日志配置
logging:
  level: DEBUG
  format: detailed
```

## 🎯 功能测试框架特点

### Page Object Model (POM)
- ✅ 基础页面类 (BasePage)
- ✅ 登录页面类 (LoginPage)
- ✅ 仪表板页面类 (DashboardPage)
- ✅ 灵活的定位器管理
- ✅ 元素查找和交互的通用方法

### 测试用例
- ✅ 7个完整的功能测试用例
- ✅ 参数化测试支持
- ✅ 测试前后的setup/teardown
- ✅ 详细的日志记录
- ✅ 失败自动截图

### 最佳实践
- ✅ 对象化测试
- ✅ 数据驱动测试
- ✅ 清晰的测试文档
- ✅ 完善的错误处理
- ✅ 模块化设计

## 📱 支持的测试类型

### 1. 功能测试
- 用户登录/注册
- 表单提交和验证
- 页面导航
- 搜索和过滤
- 业务流程验证

### 2. Web自动化测试
- Vue应用测试
- React应用测试
- 兼容性测试
- 响应式设计测试

### 3. App自动化测试
- iOS应用测试
- Android应用测试
- 跨平台测试
- Native/Hybrid应用

### 4. API接口测试
- RESTful API测试
- 请求/响应验证
- 数据库操作验证
- 错误处理测试

### 5. 性能测试
- 负载测试
- 压力测试
- 并发测试
- 响应时间分析

## 📞 常见问题

### Q1: 如何修改浏览器窗口大小？
A: 修改 `config/config.yaml` 中的 `window-size` 参数

### Q2: 如何设置隐式/显式等待时间？
A: 在 `config/config.yaml` 中修改 `implicit-wait` 和 `explicit-wait`

### Q3: 如何添加自定义的Page Object？
A: 在 `tests/functional/pages/` 目录下创建新的页面类继承 `BasePage`

### Q4: 如何运行特定标记的测试？
A: 使用 `pytest -m <marker_name>` 命令

### Q5: 截图文件保存在哪里？
A: 所有截图保存在 `screenshots/` 目录

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📞 技术支持

- 📖 [详细文档](docs/)
- 🐛 [提交Issue](../../issues)
- 💬 [讨论区](../../discussions)

---

**Happy Testing! 🎉**

### 快速开始命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
python run_tests.py

# 运行功能测试
pytest tests/functional -v

# 生成报告
pytest --html=reports/html/report.html --self-contained-html
```
