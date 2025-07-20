

from locust import HttpUser, task, between

class BasicApiUser(HttpUser):
    wait_time = between(1, 2) # Users wait between 1 and 2 seconds between tasks

    @task
    def get_todo(self):
        self.client.get("/api/v1/todos",params={"query":"reactjs","complete":"false"},headers={"accept": "application/json"})

    # @task(3) # This task will be executed 3 times more often than others
    # def create_todo(self):
    #     self.client.post("/api/v1/todos/",json={"description": "dipak","title": "reactjs"},headers={"accept": "application/json","content-type": "application/json"})
    #

