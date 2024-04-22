from tkinter import *
from Bin.Models.UserModel import User


class RemoveCategoryView(Toplevel):
    def __init__(self, user: User, update_func):
        super().__init__()
        self.title('Remove category')
        self.configure(bg='#7A9D54')
        self.update_main_window = update_func
        self.category_list = Listbox(self, selectmode=MULTIPLE,
                                listvariable=StringVar(value=list(user.categories)))
        self.category_list.pack()

        self.remove_button = Button(self, text='Remove selected',
                                    command=lambda :self.delete_selected(user))
        self.remove_button.pack()
        self.exit_button = Button(self, text='Back', command=self.destroy)
        self.exit_button.pack()

    def delete_selected(self, user):
        selected = self.category_list.curselection()
        for cat in reversed(selected):
            user.delete_category(self.category_list.get(cat))
            self.category_list.delete(cat)
            self.update_main_window()




