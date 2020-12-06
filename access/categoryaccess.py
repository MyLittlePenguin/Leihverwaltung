from access.access import Access
from data.category import Category


class CategoryAccess(Access):
    def __init__(self):
        super().__init__()

    def get_category_list(self):
        result = self.execute("select * from category order by id")
        list = []
        for item in result:
            list.append(Category(item[0], item[1]))
        return list