import json
import os
from typing import Optional

class DataProvider:
    def __init__(self, json_path: str = 'test_data.json') -> None:
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data: dict = json.load(f)

    def get(self, prop: str) -> Optional[str]:
        return self.data.get(prop)

    def getint(self, prop: str) -> Optional[int]:
        val = self.get(prop)
        return int(val) if val is not None else None

    def get_token(self) -> Optional[str]:
        return self.get("token")
