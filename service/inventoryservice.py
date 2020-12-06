from datetime import date

from access.inventoryaccess import InventoryAccess
from data.inventory import Inventory
from data.inventorycustomer import InventoryCustomer


class InventoryService:
    def __init__(self):
        self.access = InventoryAccess()

    def save_inventory(self, inv: Inventory):
        if inv.inv_nr is None:
            self.access.insert_inventory(inv)
        else:
            self.access.update_inventory(inv)

    def get_inventory_list(self):
        return self.access.get_inventory_customer_list()

    def lend_inventory(self, inv, customer):
        lent_since = date.today()
        ic = InventoryCustomer(None, inv, customer, lent_since, None)
        self.access.insert_inventory_customer(ic)

    def return_inventory(self, inv_cust: InventoryCustomer):
        self.access.update_inventory_customer(inv_cust)

