from access.access import Access
from data.category import Category
from data.customer import Customer
from data.inventory import Inventory
from data.inventorycustomer import InventoryCustomer


class InventoryAccess(Access):
    def __init__(self):
        super().__init__()

    def insert_inventory(self, inv: Inventory):
        self.execute(
            f"""
            insert into inventory(fk_category, name, description) 
            values ({inv.category}, '{inv.name}', '{inv.desc}')
            """,
            True
        )

    def update_inventory(self, inv: Inventory):
        self.execute(
            f"""
            update inventory
            set fk_category = {inv.category.id}, 
                name = '{inv.name}', 
                description = '{inv.desc}'
            where id = {inv.inv_nr}
            """,
            True
        )

    def get_inventory_customer_list(self):
        list = []
        result = self.execute("""
            select 
                inv.id,
                cat.id,
                cat.name,
                inv.name,
                inv.description,
                ic.id, 
                cust.id,
                cust.name,
                cust.firstname,
                ic.lent_since,
                ic.lent_until
            from inventory inv 
            join category cat
                on inv.fk_category = cat.id
            left join inventory_customer ic
                on inv.id = ic.fk_inventory
                and ic.lent_until is null
            left join customers cust
                on cust.id = ic.fk_customer
        """)
        for item in result:
            inv_id = item[0]
            cat_id, cat_name = item[1], item[2]
            inv_name, inv_desc = item[3], item[4]
            ic_id, ic_since, ic_until = item[5], item[9], item[10]
            cust_id, cust_name, cust_fname = item[6], item[7], item[8]
            cust = Customer(cust_id, cust_name, cust_fname)
            cat = Category(cat_id, cat_name)
            inv = Inventory(inv_id, cat, inv_name, inv_desc)
            ic = InventoryCustomer(ic_id, inv, cust, ic_since, ic_until)
            list.append(ic)
        return list

    def insert_inventory_customer(self, ic: InventoryCustomer):
        self.execute(f"""
            insert into inventory_customer(fk_inventory, fk_customer, lent_since, lent_until)
            values ({ic.inventory.inv_nr}, {ic.customer.id}, '{ic.lent_since}', null)
        """, True)

    def update_inventory_customer(self, ic: InventoryCustomer):
        self.execute(f"""
            update inventory_customer
            set fk_inventory = {ic.inventory.inv_nr},
                fk_customer = {ic.customer.id},
                lent_since = '{ic.lent_since}',
                lent_until = '{ic.lent_until}'
            where id = {ic.id}
        """, True)