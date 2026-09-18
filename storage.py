import json
import os


class StorageManager:

    def __init__(self, base_path="data"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _get_path(self, filename):
        return os.path.join(self.base_path, filename)

    def save(self, filename, data):
        try:
            path = self._get_path(filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Storage Error] Saving file failed: {e}")

    def load(self, filename):
        try:
            path = self._get_path(filename)

            if not os.path.exists(path):
                return []

            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"[Storage Error] Loading file failed: {e}")
            return []

    def append(self, filename, new_data):
        data = self.load(filename)

        if not isinstance(data, list):
            data = []

        data.append(new_data)

        self.save(filename, data)