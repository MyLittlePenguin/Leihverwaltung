from access.access import Access
from data.customer import Customer


class CustomerAccess(Access):
    def __init__(self):
        super().__init__()

    def get_customer(self, id: int):
        result = self.execute(f"""
            select id, name, firstname
            from customers
            where id = {id}
        """)
        out = None
        if len(result):
            row = result[0]
            out = Customer(id=row[0], name=row[1], firstname=row[2])

        return out

    def get_customer_list(self):
        result = self.execute("select id, name, firstname from customers")
        list = []
        for row in result:
            list.append(Customer(id=row[0], name=row[1], firstname=row[2]))
        return list

    def insert_customer(self, c: Customer):
        self.execute(f"""
            insert into customers(name, firstname)
            values ('{c.name}', '{c.firstname}')
        """, True)
