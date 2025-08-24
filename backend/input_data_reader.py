import json
import os

from config import JSON_FILE_PATH


class InputDataReader:
    def __init__(self):
        self.tasks_data = self._get_tasks()

    @staticmethod
    def _get_tasks() -> list[dict]:
        if not os.path.exists(JSON_FILE_PATH):
            raise FileNotFoundError(f"JSON file '{JSON_FILE_PATH}' not found!")

        with open(JSON_FILE_PATH, "r") as file:
            tasks_data = json.load(file)

        return tasks_data

    def get_tasks_data(self) -> list[dict]:
        return self.tasks_data
