from typing import List, Dict

class Memory:
    def __init__(self):
        self._history: List[Dict] = []

    def add(self, role: str, content: str) -> None:
        self._history.append({"role": role, "content": content})

    def add_raw(self, message: Dict) -> None:
        self._history.append(message)

    def get(self) -> List[Dict]:
        return list(self._history)

    def clear(self) -> None:
        self._history = []
