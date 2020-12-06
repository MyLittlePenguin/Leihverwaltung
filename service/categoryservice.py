from access.categoryaccess import CategoryAccess


class CategoryService:
    def __init__(self):
        self.access = CategoryAccess()

    def get_category_list(self):
        return self.access.get_category_list()