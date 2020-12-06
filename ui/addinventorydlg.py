import re
from sqlite3 import IntegrityError
from tkinter import BOTH, LEFT, X, StringVar, E, W, S, messagebox

from data.inventory import Inventory
from ui.dialog import Dialog, DlgNames
from tkinter.ttk import *


class AddInventoryDlg(Dialog):
    NAME = DlgNames.ADD_INV

    def __init__(self, parent, nav_fn):
        super().__init__(parent, nav_fn)
        self.inventory = None

        self.save_action = lambda d: print(d)
        self.selected_category = None
        self.categories = {}

        menu_bar = Frame(self.frame)
        menu_bar.pack(fill=X)
        b = Button(menu_bar, text="<", command=lambda: nav_fn(DlgNames.INVENTORY))
        b.pack(side=LEFT)

        self.container = self.create_formular(self.frame)
        self.container.pack(fill=BOTH)

        # self.invNr = self.createField("Inv. Nr.", 0)
        self.create_label(self.container, "Kategorie", 0)
        self.cat_box = Combobox(self.container)
        self.cat_box.state(["readonly"])
        self.place_field(self.cat_box, 0)
        self.cat_box.bind("<<ComboboxSelected>>", self.select_category)

        self.name = self.create_field(self.container, "Name", 1)
        self.desc = self.create_field(self.container, "Beschreibung", 2)

        b = Button(self.container, text="Speichern", command=self.on_save)
        b.grid(row=3, column=2, sticky=(W, E), padx=5, pady=5)

    def on_arrive(self, data):
        if data is not None:
            self.set_inventory(data["inventory"])

    def on_leave(self, data):
        print(f"{AddInventoryDlg.NAME} verlassen")

    def on_save(self):
        try:
            if self.inventory is None:
                self.inventory = Inventory()
            self.inventory.category = self.selected_category
            self.inventory.name = self.name.get()
            self.inventory.desc = self.desc.get()
            self.save_action(self.inventory)
            self.reset_category()
            self.nav_fn(DlgNames.INVENTORY)
        except IntegrityError:
            messagebox.showerror(message="Die Inv. Nr. ist bereits vergeben!")

    def set_categories(self, categories):
        cat_list = []
        for cat in categories:
            txt = cat.to_string()
            self.categories[txt] = cat
            cat_list.append(txt)
        self.cat_box["values"] = cat_list
        if len(categories) > 0:
            first = cat_list[0]
            self.cat_box.set(first)
            self.selected_category = self.categories[first].id

    def select_category(self, event):
        selection = self.cat_box.get()
        print(self.categories[selection].name)
        self.selected_category = self.categories[selection].id
        self.cat_box.selection_clear()

    def reset_category(self):
        self.inventory = None
        self.name.set("")
        self.desc.set("")
        first = self.cat_box["values"][0]
        self.cat_box.set(first)
        self.selected_category = self.categories[first]

    def set_inventory(self, inv: Inventory):
        self.inventory = inv
        self.name.set(inv.name)
        self.desc.set(inv.desc)
        cat_str = inv.category.to_string()
        self.cat_box.set(cat_str)
        self.selected_category = self.categories[cat_str]
