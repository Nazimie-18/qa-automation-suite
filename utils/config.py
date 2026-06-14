"""配置加载模块 - 读取config.yaml和.env"""
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 加载.env
load_dotenv(PROJECT_ROOT / ".env")

# 加载config.yaml
_config = {}
_config_path = PROJECT_ROOT / "config" / "config.yaml"
if _config_path.exists():
    with open(_config_path, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f) or {}


def get(key, default=None):
    """获取配置值，优先环境变量，其次config.yaml"""
    env_key = key.upper().replace(".", "_")
    env_val = os.environ.get(env_key)
    if env_val is not None:
        return env_val

    # 从config.yaml中按点号路径查找
    keys = key.split(".")
    val = _config
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k)
            if val is None:
                return default
        else:
            return default
    return val


def get_browser_config(browser=None):
    """获取浏览器配置"""
    if browser is None:
        browser = get("BROWSER", "chrome")
    return get(f"browser.{browser}", {})


def get_api_config(backend="python"):
    """获取API配置"""
    return get(f"api.backends.{backend}", {})


def get_database_config(db_type="mysql"):
    """获取数据库配置"""
    return get(f"database.{db_type}", {})
