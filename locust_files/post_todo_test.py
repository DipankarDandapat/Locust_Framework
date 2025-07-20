from locust import HttpUser, task, between
import random

class PostTodoUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://api.freeapi.app"

    @task
    def post_todo(self):
        title = f"Test Todo {random.randint(1, 100000)}"
        description = "Some description about todo which is optional"
        payload = {"description": description, "title": title}
        headers = {"accept": "application/json", "content-type": "application/json"}
        self.client.post("/api/v1/todos", json=payload, headers=headers)