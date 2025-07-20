from locust import HttpUser, task, between
import random

class EndToEndTodoUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://api.freeapi.app"
    todo_id = None

    @task(1)
    def create_todo(self):
        title = f"EndToEnd Test Todo {random.randint(1, 100000)}"
        description = "Some description about todo which is optional"
        payload = {"description": description, "title": title}
        headers = {"accept": "application/json", "content-type": "application/json"}
        response = self.client.post("/api/v1/todos", json=payload, headers=headers, name="Create Todo")
        if response.status_code == 201 and "_id" in response.json():
            self.todo_id = response.json()["_id"]
            print(f"Created Todo with ID: {self.todo_id}")
        else:
            print(f"Failed to create Todo: {response.status_code} - {response.text}")

    @task(2)
    def get_todo(self):
        if self.todo_id:
            headers = {"accept": "application/json"}
            self.client.get(f"/api/v1/todos/{self.todo_id}", headers=headers, name="Get Todo by ID")
        else:
            print("No Todo ID available to get.")

    @task(3)
    def delete_todo(self):
        if self.todo_id:
            headers = {"accept": "application/json"}
            self.client.delete(f"/api/v1/todos/{self.todo_id}", headers=headers, name="Delete Todo by ID")
            self.todo_id = None # Reset todo_id after deletion
        else:
            print("No Todo ID available to delete.")