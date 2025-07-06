
from locust import HttpUser, task, between, SequentialTaskSet

class UserBehavior(SequentialTaskSet):
    def on_start(self):
        self.client.get("/")

    @task(1)
    def view_homepage(self):
        self.client.get("/", name="Homepage")

    @task(2)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")

    @task(1)
    def view_about_page(self):
        self.client.get("/about", name="About Page")

    @task(1)
    def view_contact_page(self):
        self.client.get("/contact", name="Contact Page")

class WebsiteUser(HttpUser):
    wait_time = between(5, 9)
    tasks = [UserBehavior]


