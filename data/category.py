class Category:
    def __init__(self, id: int, name: str):
        self.id, self.name = id, name

    def to_string(self):
        return f"{self.id}: {self.name}"