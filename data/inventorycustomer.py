from data.customer import Customer
from data.inventory import Inventory


class InventoryCustomer:
    def __init__(self, id: int, inv: Inventory, cust: Customer, lent_since, lent_until):
        self.id = id
        self.inventory = inv
        self.customer = cust
        self.lent_since = lent_since
        self.lent_until = lent_until
