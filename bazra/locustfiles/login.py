from locust import HttpUser, task


class LoggingInUser(HttpUser):
    @task
    def login(self):
        self.client.get("/auth")
