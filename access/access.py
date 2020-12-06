import os
import sqlite3

from data.category import Category


class Access:
    def __init__(self):
        db_file = "datastore.sqlite"
        db_exists = False

        if os.path.isfile(db_file):
            db_exists = True

        self.db = sqlite3.connect("datastore.sqlite")

        if not db_exists:
            self.create_data_structure()

    def create_data_structure(self):
        queries = [
            """create table if not exists category(
                id integer primary key,
                name text not null
            )""",
            """create table if not exists inventory(
                id integer primary key, 
                fk_category integer not null,
                name text not null, 
                description text,
                foreign key (fk_category) references category(id)
            )""",
            """create table if not exists customers(
                id integer primary key, 
                name text, 
                firstname text
            )""",
            """create table if not exists inventory_customer(
                id integer primary key, 
                fk_inventory integer not null,
                fk_customer integer not null,
                lent_since varchar(10) not null,
                lent_until varchar(10),
                foreign key (fk_inventory) references inventory(id),
                foreign key (fk_customer) references customers(id)
            )""",
            """
            insert into category (name) values ('Buch')
            """,
            """
            insert into category (name) values ('Bluray')
            """,
            """
            insert into category (name) values ('DVD')
            """,
            """
            insert into category (name) values ('Spiel')
            """,
            """
            insert into category (name) values ('Sonstiges')
            """
        ]
        for query in queries:
            self.execute(query, True)

    def execute(self, query: str, commit=False):
        cursor = self.db.cursor()
        cursor.execute(query)
        result = []
        if commit:
            self.db.commit()
        else:
            result = cursor.fetchall()
        cursor.close()
        return result


