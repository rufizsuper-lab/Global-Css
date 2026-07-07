import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"


class Task:
    def __init__(self, title, priority, completed=False, created=None):
        self.title = title
        self.priority = priority
        self.completed = completed
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed,
            "created": self.created,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["priority"],
            data["completed"],
            data["created"],
        )
 
def main():
    manager = TaskManager()
    manager.menu()


if __name__ == "__main__":
    main()