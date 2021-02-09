# This is a sample Python script.

from tkinter import Tk, BOTH, mainloop, PhotoImage
from tkinter.ttk import Style

from access.access import Access
from service.categoryservice import CategoryService
from service.customerservice import CustomerService
from service.inventoryservice import InventoryService
from ui.addcustomerdlg import AddCustomerDlg
from ui.addinventorydlg import AddInventoryDlg
from ui.inventorydlg import InventoryDlg


class Main:
    """
    Diese Klasse baut das Hauptfenster auf und kümmert sich um die navigation
    """

    def __init__(self):
        self.root = Tk()
        self.root.tk.call("lappend", "auto_path", "./themes/awthemes-9.5.1.1")
        self.root.tk.call("package", "require", "awdark")
        self.root.tk.call("package", "require", "awlight")

        self.inventory_service = InventoryService()
        self.category_service = CategoryService()
        self.customer_service = CustomerService()

        self.root.title("Das Leihhaus")
        self.root.iconphoto(False, PhotoImage(file="pic/logo.png"))
        self.root.geometry("1024x728")

        self.access = Access()

        self.akt_fenster = None
        self.fenster = {}
        self.init_managment_window()
        self.init_inv_window()
        self.init_cust_window()

        self.open(InventoryDlg.NAME)

    def open(self, fensterName, data=None):
        print(f"open: {fensterName}")
        if self.akt_fenster is not None:
            self.akt_fenster.on_leave(data)
            self.akt_fenster.frame.pack_forget()

        fenster = self.fenster[fensterName]
        fenster.on_arrive(data)

        self.akt_fenster = fenster
        self.akt_fenster.frame.pack(fill=BOTH, expand=1)

    def init_managment_window(self):
        fenster = InventoryDlg(self.root, self.open)
        fenster.loadInventoryAction = self.inventory_service.get_inventory_list
        fenster.lendInventoryAction = self.inventory_service.lend_inventory
        fenster.returnInventoryAction = self.inventory_service.return_inventory
        fenster.loadCustomersAction = self.customer_service.get_customer_list
        self.fenster[InventoryDlg.NAME] = fenster

    def init_inv_window(self):
        fenster = AddInventoryDlg(self.root, self.open)
        fenster.save_action = self.inventory_service.save_inventory
        fenster.set_categories(self.category_service.get_category_list())
        self.fenster[AddInventoryDlg.NAME] = fenster

    def init_cust_window(self):
        fenster = AddCustomerDlg(self.root, self.open)
        fenster.save_action = self.customer_service.insert_customer
        self.fenster[AddCustomerDlg.NAME] = fenster


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = Main()
    mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
