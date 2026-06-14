"""性能测试Locustfile - 负载测试和压力测试"""
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    """模拟网站用户行为"""
    wait_time = between(1, 3)

    @task(3)
    def get_homepage(self):
        """访问首页（权重3）"""
        self.client.get("/get")

    @task(2)
    def post_data(self):
        """提交数据（权重2）"""
        self.client.post("/post", json={"key": "value"})

    @task(1)
    def get_delay(self):
        """模拟慢响应（权重1）"""
        self.client.get("/delay/1")

    @task(1)
    def get_status(self):
        """状态检查"""
        self.client.get("/status/200")


class APILoadTest(HttpUser):
    """API负载测试"""
    wait_time = between(0.5, 2)

    @task
    def api_call(self):
        self.client.get("/get")
