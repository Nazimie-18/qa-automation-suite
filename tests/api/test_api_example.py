"""API接口测试示例"""
import pytest
import requests
from unittest.mock import patch, Mock
from utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.mark.api
@pytest.mark.python
class TestAPIExample:
    """API测试示例 - 使用mock演示测试模式"""

    @patch("requests.get")
    def test_get_request(self, mock_get):
        """验证GET请求成功响应"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"url": "http://example.com/get"}
        mock_get.return_value = mock_response

        response = requests.get("http://localhost:8000/api/users")
        assert response.status_code == 200
        data = response.json()
        assert "url" in data
        logger.info(f"GET响应状态码: {response.status_code}")

    @patch("requests.post")
    def test_post_request(self, mock_post):
        """验证POST请求"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"json": {"username": "test"}}
        mock_post.return_value = mock_response

        body = {"username": "test", "password": "secret"}
        response = requests.post("http://localhost:8000/api/login", json=body)
        assert response.status_code == 200
        data = response.json()
        assert data["json"]["username"] == "test"
        logger.info(f"POST响应状态码: {response.status_code}")

    @patch("requests.get")
    def test_404_handling(self, mock_get):
        """验证404错误处理"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = requests.get("http://localhost:8000/api/nonexistent")
        assert response.status_code == 404

    @patch("requests.get")
    def test_headers(self, mock_get):
        """验证响应头处理"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"headers": {"Host": "localhost"}}
        mock_get.return_value = mock_response

        response = requests.get("http://localhost:8000/api/headers")
        assert response.status_code == 200
        headers = response.json()["headers"]
        assert "Host" in headers

    @pytest.mark.smoke
    @patch("requests.get")
    def test_api_is_reachable(self, mock_get):
        """冒烟测试 - API可达性"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = requests.get("http://localhost:8000/api/health", timeout=10)
        assert response.status_code == 200
