from data.category import Category


class Inventory:
    def __init__(self, inv_nr: int = None, category: Category = None, name: str = "", desc: str = ""):
        self.inv_nr = inv_nr
        self.category = category
        self.name = name
        self.desc = desc
