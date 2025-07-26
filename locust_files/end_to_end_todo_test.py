
from locust import HttpUser, task, between
from utils.data_generator import DataGenerator
from utils.assertions import Assertions

class EndToEndTodoUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://api.freeapi.app"
    todo_id = None

    def on_start(self):
        self.data_gen = DataGenerator()

    @task(1)
    def create_todo(self):
        todo_data = self.data_gen.generate_todo_data()
        headers = {"accept": "application/json", "content-type": "application/json"}
        response = self.client.post("/api/v1/todos", json=todo_data, headers=headers, name="Create Todo")
        Assertions.assert_status_code(response, 201)
        Assertions.assert_json_field(response, "_id")
        if "_id" in response.json():
            self.todo_id = response.json()["_id"]
            print(f"Created Todo with ID: {self.todo_id}")
        else:
            print(f"Failed to create Todo: {response.status_code} - {response.text}")

    @task(2)
    def get_todo(self):
        if self.todo_id:
            headers = {"accept": "application/json"}
            response = self.client.get(f"/api/v1/todos/{self.todo_id}", headers=headers, name="Get Todo by ID")
            Assertions.assert_status_code(response, 200)
            Assertions.assert_json_field(response, "_id", self.todo_id)
            Assertions.assert_response_time_less_than(response, 1000)
        else:
            print("No Todo ID available to get.")

    @task(3)
    def delete_todo(self):
        if self.todo_id:
            headers = {"accept": "application/json"}
            response = self.client.delete(f"/api/v1/todos/{self.todo_id}", headers=headers, name="Delete Todo by ID")
            Assertions.assert_status_code(response, 200)
            Assertions.assert_response_time_less_than(response, 1000)
            self.todo_id = None # Reset todo_id after deletion
        else:
            print("No Todo ID available to delete.")


