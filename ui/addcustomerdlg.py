from tkinter import X, LEFT, BOTH, messagebox
from tkinter.ttk import Frame, Button

from data.customer import Customer
from ui.dialog import Dialog, DlgNames


class AddCustomerDlg(Dialog):
    NAME = DlgNames.ADD_CUST

    def __init__(self, parent, nav_fn):
        super().__init__(parent, nav_fn)

        self.save_action = lambda d: print(d)

        menu_bar = Frame(self.frame)
        menu_bar.pack(fill=X)
        b = Button(menu_bar, text="<", command=lambda: nav_fn(DlgNames.INVENTORY))
        b.pack(side=LEFT)

        self.container = self.create_formular(self.frame)
        self.container.pack(fill=BOTH)

        self.firstname_var = self.create_field(self.container, "Vorname", 0)
        self.name_var = self.create_field(self.container, "Name", 1)

        self.place_field(Button(self.container, text="Speichern", command=self.on_save), 2)

    def on_save(self):
        name, firstname = self.name_var.get(), self.firstname_var.get()
        if len(name) > 0 and len(firstname) > 0:
            c = Customer(name=self.name_var.get(), firstname=self.firstname_var.get())
            self.save_action(c)
            self.name_var.set("")
            self.firstname_var.set("")
            self.nav_fn(DlgNames.INVENTORY)
        else:
            messagebox.showerror(message="Name oder Vorname ist nicht ausgefüllt!")
