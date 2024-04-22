from tkinter import *
from tkinter import messagebox
from Bin.Models.UserModel import User

class EditCategoryView(Toplevel):
    def __init__(self, user: User, update_func):
        super().__init__()
        self.title('Edit category')
        self.configure(bg='#7A9D54')
        self.update_main_window = update_func
        self.new_category_name_var = StringVar()
        self.edit_entry_box = (Entry(self, fg='black', textvariable=self.new_category_name_var)
                          .grid(row=0, column=0, sticky=EW))

        self.category_list = Listbox(self, selectmode=SINGLE,
                                listvariable=StringVar(value=list(user.categories)))
        self.category_list.grid(row=1, column=0, sticky=EW)

        self.remove_button = Button(self, text='Edit', command=lambda :self.edit_selected(user))
        self.remove_button.grid(row=2, column=0, sticky=EW)

        self.exit_button = (Button(self, text='Back', command=self.destroy)
                       .grid(row=3, column=0, sticky=EW))

    def edit_selected(self, user: User):
        try:
            old_category_name = self.category_list.get(self.category_list.curselection())
            new_category_name = self.new_category_name_var.get()
            if new_category_name and old_category_name:
                user.edit_category(new_category_name.capitalize(), old_category_name)
                self.category_list.configure(listvariable=StringVar(value=list(user.categories)))
                self.update_main_window()
            else:
                raise ValueError("Please add new category name and select categoty to be edited")
        except ValueError as ex:
            messagebox.showerror('Missing data Error', ex)
        except TclError:
            messagebox.showerror('Missing data Error', 'Select category for editting')


