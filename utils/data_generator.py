
from faker import Faker
import random

class DataGenerator:
    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)

    def generate_user_data(self):
        """Generates realistic-looking user data."""
        return {
            "username": self.fake.user_name(),
            "email": self.fake.email(),
            "password": self.fake.password(length=12),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name()
        }

    def generate_product_data(self):
        """Generates realistic-looking product data."""
        return {
            "name": self.fake.word().capitalize() + " " + self.fake.word(),
            "description": self.fake.paragraph(nb_sentences=3),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "category": self.fake.word()
        }

    def generate_todo_data(self):
        """Generates realistic-looking todo data."""
        return {
            "title": self.fake.sentence(nb_words=4),
            "description": self.fake.paragraph(nb_sentences=2),
            "completed": self.fake.boolean()
        }

    # Add more data generation methods as needed


