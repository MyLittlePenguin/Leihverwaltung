from access.customeraccess import CustomerAccess
from data.customer import Customer


class CustomerService:
    def __init__(self):
        self.access = CustomerAccess()

    def get_customer(self, id):
        return self.access.get_customer(id)

    def get_customer_list(self):
        return self.access.get_customer_list()

    def insert_customer(self, c: Customer):
        self.access.insert_customer(c)
