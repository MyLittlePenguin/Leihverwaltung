from tkinter import StringVar, E, W, S, DISABLED
from tkinter.ttk import Frame, Entry, Label


class Dialog:
    def __init__(self, parent, nav_fn):
        self.frame = Frame(parent)
        self.frame["padding"] = "10"
        self.nav_fn = nav_fn

    def on_arrive(self, data):
        pass

    def on_leave(self, data):
        pass

    def create_field(self, container, txt, i, readonly=False):
        self.create_label(container, txt, i)
        var = StringVar()
        entry = None
        if readonly:
            entry = Entry(container, textvariable=var, state=DISABLED)
        else:
            entry = Entry(container, textvariable=var)
        self.place_field(entry, i)
        return var

    def place_field(self, field, row, col=2):
        field.grid(row=row, column=col, sticky=(E, W, S), padx=5, pady=5)

    def create_label(self, container, txt, i):
        Label(container, text=txt).grid(row=i, column=1, sticky=(E, S), padx=5, pady=5)

    def create_formular(self, container):
        form = Frame(container)
        form.rowconfigure(0, weight=1)
        form["padding"] = "0 50 0 0"
        form.columnconfigure(0, weight=1)
        form.columnconfigure(3, weight=1)
        return form


class DlgNames:
    INVENTORY = "leihen"
    ADD_INV = "inventarisierung"
    ADD_CUST = "neukunde"
