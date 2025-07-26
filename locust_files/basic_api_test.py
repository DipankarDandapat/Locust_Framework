from locust import HttpUser, task, between

from utils.assertions import Assertions

class BasicApiUser(HttpUser):
    wait_time = between(1, 2) # Users wait between 1 and 2 seconds between tasks

    @task
    def get_todo(self):
        response = self.client.get("/api/v1/todos",params={"query":"reactjs","complete":"false"},headers={"accept": "application/json"})
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_field(response, "data")  # Assuming the response has a 'data' field

    # @task(3) # This task will be executed 3 times more often than others
    # def create_todo(self):
    #   response =self.client.post("/api/v1/todos/",json={"description": "dipak","title": "reactjs"},headers={"accept": "application/json","content-type": "application/json"})
    #     Assertions.assert_status_code(response, 200)
    #     Assertions.assert_json_field(response, "data")  # Assuming the response has a 'data' field
    #

