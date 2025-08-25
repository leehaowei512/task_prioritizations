import json
import os
from pathlib import Path

from database.config import JSON_FILE_PATH


class InputDataReader:
    def __init__(self):
        script_dir = Path(__file__).parent.parent.parent
        self.json_path = os.path.join(script_dir, JSON_FILE_PATH)
        print(f"PATH: {self.json_path}")
        self.tasks_data = self._get_tasks()

    def _get_tasks(self) -> list[dict]:
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"JSON file '{self.json_path}' not found!")

        with open(self.json_path, "r") as file:
            tasks_data = json.load(file)

        return tasks_data

    def get_tasks_data(self) -> list[dict]:
        return self.tasks_data
