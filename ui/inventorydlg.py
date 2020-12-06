from datetime import date
from tkinter import END, ANCHOR, Listbox, Y, LEFT, BOTH, X, StringVar, RIGHT, messagebox
from tkinter.ttk import *

from data.inventory import Inventory
from data.inventorycustomer import InventoryCustomer
from ui.dialog import Dialog, DlgNames


class InventoryDlg(Dialog):
    NAME = DlgNames.INVENTORY

    def __init__(self, parent, nav_fn):
        super().__init__(parent, nav_fn)
        self.loadInventoryAction = lambda: []
        self.loadCustomersAction = lambda: []
        self.lendInventoryAction = lambda: 1
        self.returnInventoryAction = lambda: 1

        self.inventory_customer = {}
        self.customers = {}
        self.selected_inventory_customer = None

        menu_bar = Frame(self.frame)
        menu_bar["padding"] = "0 0 0 10"
        menu_bar.pack(fill=X)

        add_inv_btn = Button(menu_bar, text="Neues Inventar", command=lambda: nav_fn(DlgNames.ADD_INV))
        add_inv_btn.pack(side=LEFT)

        change_inv_btn = Button(menu_bar, text="Inventar bearbeiten", command=self.inv_change_click)
        change_inv_btn.pack(side=LEFT)

        add_cust_btn = Button(menu_bar, text="Neuer Kunde", command=lambda: nav_fn(DlgNames.ADD_CUST))
        add_cust_btn.pack(side=LEFT)

        # delete_btn = Button(menu_bar, text="Löschen", command=self.clear_inventory_list)
        # delete_btn.pack(side=LEFT)

        style = Style()
        themes = sorted(style.theme_names())
        self.theme_combo = Combobox(menu_bar)
        self.theme_combo["values"] = themes
        self.theme_combo.state(["readonly"])
        self.theme_combo.bind("<<ComboboxSelected>>", self.select_theme)
        self.theme_combo.set("awdark")
        self.select_theme(None)
        self.theme_combo.pack(side=RIGHT)

        Label(menu_bar, text="Theme: ").pack(side=RIGHT)

        main_area = Frame(self.frame)
        main_area.pack(fill=BOTH)

        item_container = Frame(main_area)
        item_container.pack(side=LEFT, fill=Y)

        sb = Scrollbar(main_area)
        sb.pack(side=LEFT, fill=Y)

        self.inv_list = []
        self.inv_list_var = StringVar(value=self.inv_list)
        self.inv_listbox = Listbox(
            item_container,
            width=30,
            height=1000,
            yscrollcommand=sb.set,
            listvariable=self.inv_list_var
        )
        self.inv_listbox_ignore_event = False
        self.inv_listbox.bind('<<ListboxSelect>>', self.select_inventory)
        self.inv_listbox.pack()

        sb.config(command=self.inv_listbox.yview)

        self.inv_form = self.create_formular(main_area)
        self.inv_form.pack(fill=BOTH)

        self.inv_nr = self.create_field(self.inv_form, "Inv. Nr.", 0, True)
        self.inv_cat = self.create_field(self.inv_form, "Kategorie", 1, True)
        self.inv_name = self.create_field(self.inv_form, "Name", 2, True)
        self.inv_desc = self.create_field(self.inv_form, "Beschreibung", 3, True)

        self.create_label(self.inv_form, "Geliehen an", 4)
        self.customer_box = Combobox(self.inv_form)
        self.customer_box.bind("<<ComboboxSelected>>", self.select_customer)
        self.customer_box.state(["readonly"])
        self.place_field(self.customer_box, 4)

        self.lent_since_var = self.create_field(self.inv_form, "Geliehen seit", 5, True)

        self.lend_inv_btn = Button(self.inv_form, text="Verleihen", command=self.lend)
        self.return_inv_btn = Button(self.inv_form, text="Zurücknehmen", command=self.return_inventory)
        self.place_field(self.lend_inv_btn, 6, 1)
        self.place_field(self.return_inv_btn, 6)

    def inv_change_click(self):
        try:
            inv_cust = self.get_selected_inv_cust()
            self.nav_fn(DlgNames.ADD_INV, {"inventory": inv_cust.inventory})
        except KeyError:
            messagebox.showerror(message="Es wurde kein Inventar ausgewählt")

    def on_leave(self, data=None):
        pass

    def on_arrive(self, data=None):
        self.refresh_current_inventory_customer()

    def clear_inventory_list(self):
        self.selected_inventory_customer = None
        self.inv_list = []
        self.inv_list_var.set(self.inv_list)
        self.inventory_customer = {}
        self.inv_nr.set("")
        self.inv_cat.set("")
        self.inv_name.set("")
        self.inv_desc.set("")
        self.lent_since_var.set("")

    def list_inventory(self, inv_cust: InventoryCustomer):
        key = f"{'' if inv_cust.id is None else '* '}{inv_cust.inventory.inv_nr}"
        self.inv_list.append(f"{key}: {inv_cust.inventory.name} ({inv_cust.inventory.category.name})")
        self.inv_list_var.set(self.inv_list)
        self.inventory_customer[f"{key}"] = inv_cust

    def select_inventory(self, event):
        if not self.inv_listbox_ignore_event:
            selection = self.inv_listbox.get(ANCHOR)
            self.update_form(selection[0:selection.find(":")])
        self.inv_listbox_ignore_event = False

    def update_form(self, selection):
        self.selected_inventory_customer = selection
        selected = self.inventory_customer[self.selected_inventory_customer]
        inv = selected.inventory
        self.inv_nr.set(inv.inv_nr)
        self.inv_cat.set(inv.category.name)
        self.inv_name.set(inv.name)
        self.inv_desc.set(inv.desc)
        cust = selected.customer
        if cust.id is not None:
            self.customer_box.set(f"{cust.id}: {cust.name}, {cust.firstname}")
            self.lent_since_var.set(selected.lent_since)
            self.lend_inv_btn["state"] = "disabled"
            self.return_inv_btn["state"] = "normal"
        else:
            default = self.customer_box["values"][0]
            self.customer_box.set(default)
            self.lent_since_var.set("")
            self.lend_inv_btn["state"] = "normal"
            self.return_inv_btn["state"] = "disabled"
        self.select_customer(None)

    def select_theme(self, event):
        Style().theme_use(self.theme_combo.get())
        self.theme_combo.selection_clear()

    def load_customers(self):
        print("load_customers")
        list = self.loadCustomersAction()
        customers = []
        first = "Auswählen"
        self.customers = {first: None}
        customers.append(first)
        for item in list:
            txt = f"{item.id}: {item.name}, {item.firstname}"
            self.customers[txt] = item
            customers.append(txt)
        self.customer_box["values"] = customers
        self.customer_box.set(first)

    def select_customer(self, event):
        self.customer_box.selection_clear()

        # Leider wird das Listbox-select-event getriggered,
        # wenn die Person ausgewählt wird. das hier ist eine Krücke um die Auswirkungen zu umgehen
        self.inv_listbox_ignore_event = True

    def lend(self):
        default = self.customer_box["values"][0]
        cust_str = self.customer_box.get()
        if cust_str != default:
            since = date.today()
            self.lent_since_var.set(since)
            selected = self.get_selected_inv_cust()
            selected.lent_since = since
            selected.customer = self.customers[cust_str]
            self.set_selected_inv_cust(selected)
            self.lendInventoryAction(selected.inventory, selected.customer)
            oldkey = self.selected_inventory_customer
            self.refresh_current_inventory_customer()
            self.update_form("* " + oldkey)
            self.inv_listbox_ignore_event = False
        else:
            messagebox.showerror(message="Zum verleihen muss ein Kunde ausgewählt sein!")

    def return_inventory(self):
        selected = self.get_selected_inv_cust()
        self.returnInventoryAction(selected)
        oldkey = self.selected_inventory_customer
        self.refresh_current_inventory_customer()

        self.update_form(oldkey[2:])

        self.inv_listbox_ignore_event = False

    def refresh_current_inventory_customer(self):
        self.clear_inventory_list()
        list = self.loadInventoryAction()
        for item in list:
            self.list_inventory(item)

        self.load_customers()

    def get_selected_inv_cust(self):
        key = self.selected_inventory_customer
        selected = self.inventory_customer[key]
        return selected

    def set_selected_inv_cust(self, ic: InventoryCustomer):
        key = self.selected_inventory_customer
        self.inventory_customer[key] = ic
