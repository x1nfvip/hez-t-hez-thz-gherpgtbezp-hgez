from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, username, role, last_generation=None):
        self.id = id
        self.username = username
        self.role = role
        self.last_generation = last_generation
