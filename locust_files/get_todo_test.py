from locust import HttpUser, task, between

class GetTodoUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://api.freeapi.app"

    # This is a placeholder. In a real scenario, you would get existing IDs.
    # For this example, we'll use a hardcoded ID from the user's prompt.
    # In an end-to-end test, this ID would come from a previous POST request.
    todo_id = "648e0741aeefd0cfa40adddd"

    @task
    def get_todo(self):
        headers = {"accept": "application/json"}
        self.client.get(f"/api/v1/todos/{self.todo_id}", headers=headers)