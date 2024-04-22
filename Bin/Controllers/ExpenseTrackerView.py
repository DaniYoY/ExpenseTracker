from tkinter import *
from tkinter import ttk
from  tkinter import messagebox
from  tkinter import simpledialog
from tkcalendar import DateEntry
from Bin.Models.ExpenseModel import Expense
from Bin.Models.ExpenseDTOModel import ExpenseDTO
from Bin.Controllers.ReportView import ReportView
from Bin.Controllers.RemoveCategoryView import RemoveCategoryView
from Bin.Controllers.EditCategoryView import EditCategoryView
from Bin.SavingService import SavingService
import datetime

class ExpenseTrackerApp(object):
    def __init__(self, master):
        self.root = master
        self.root.title('My Expense Tracker')

        username = simpledialog.askstring('User name', 'Please enter username')
        self.user = SavingService.load_user_data(username)
        self.root.lift()

        self.selected_row_expense_id = 0

        self.font_config = ('Times new roman', 16)
        self.category_var = StringVar()
        self.amount_var = StringVar()

        # setup 2 frames
        self.table_frame = Frame(self.root, padx=10, pady=10, bg='#2A52BE')
        self.table_frame.pack(expand=True, fill=BOTH)

        self.input_frame = Frame(self.root, padx=10, pady=10, bg='#2A52BE')
        self.input_frame.pack(expand=True, fill=BOTH)

        # config expense_table frame
        self.expense_table = ttk.Treeview(self.table_frame, selectmode='browse',
                                          columns=(1, 2, 3, 4), show='headings', height=8)
        self.expense_table.pack()
        self.expense_table.column(1, anchor=CENTER, stretch=NO, width=50)
        self.expense_table.column(2, anchor=CENTER, stretch=NO, width=90)
        self.expense_table.column(3, anchor=CENTER, stretch=NO, width=150)
        self.expense_table.column(4, anchor=CENTER, stretch=NO, width=200)
        self.expense_table.heading(1, text='ID')
        self.expense_table.heading(2, text='Amount')
        self.expense_table.heading(3, text='Category')
        self.expense_table.heading(4, text='Date')

        self.expense_table.bind('<ButtonRelease-1>', self.select_expense)
        self.table_style = ttk.Style()
        self.table_style.theme_use('default')
        self.table_style.map('Treeview')

        # self.expense_table.update()
        self.table_scrollbar = Scrollbar(self.table_frame, orient=VERTICAL)
        self.table_scrollbar.configure(command=self.expense_table.yview)
        self.table_scrollbar.pack(side=RIGHT, fill=Y)
        self.table_scrollbar.place_configure( relx=0.99, relheight=1)
        self.expense_table.config(yscrollcommand=self.table_scrollbar.set)

        # config input frame
        self.field_type_label = (Label(self.input_frame, text='Field type', font=self.font_config,
                                       bg='#2A52BE', fg='white')
                                 .grid(row=0, column=0,      sticky=W))
        self.field_value_label = (Label(self.input_frame, text='Field value', font=self.font_config,
                                        bg='#2A52BE', fg='white')
                                  .grid(row=0, column=1,      sticky=EW))
        self.categoty_label = (Label(self.input_frame, text='Category:', font=self.font_config,
                                     bg='#2A52BE', fg='white')
                               .grid(row=1, column=0, sticky=W))
        self.amount_label = (Label(self.input_frame, text='Amount:', font=self.font_config,
                                   bg='#2A52BE', fg='white')
                             .grid(row=2, column=0, sticky=W))
        self.date_label = (Label(self.input_frame, text='Date:', font=self.font_config,
                                 bg='#2A52BE', fg='white')
                           .grid(row=3, column=0, sticky=W))
        self.actions_label = (Label(self.input_frame, text='Actions:', font=self.font_config,
                                    bg='#2A52BE', fg='white')
                              .grid(row=0, column=4, sticky=W))
        #entry boxes
        self.expense_category_entry_box = ttk.Combobox(self.input_frame, values=list(self.user.categories),
                                                  textvariable=self.category_var)
        self.expense_category_entry_box.grid(row=1, column=1, sticky=EW, padx=(10, 0))

        self.expense_amount_entry_box = (Entry(self.input_frame, font=self.font_config, fg='black',
                                               textvariable=self.amount_var)
                                    .grid(row=2, column=1, sticky=EW, padx=(10, 0)))
        self.expense_date_entry_box = DateEntry(self.input_frame, width=12, background='darkblue',foreground='white',
                                                borderwidth=2, date_pattern='dd/MM/yyyy')
        self.expense_date_entry_box.grid(row=3, column=1, sticky=EW, padx=(10, 0))

        # buttons
        self.current_date_button = (Button(self.input_frame, text="Set Today", font=self.font_config,
                                          bg='#9D44C0', fg='white',
                                     command=self.get_today, width=10, )
                                    .grid(row=3, column=2, sticky=EW))
        self.add_expense_button = (Button(self.input_frame, text="Add Expense", font=self.font_config,
                                         bg='#9D44C0', fg='white',
                                    command=self.add_expense, width=10, )
                                   .grid(row=1, column=3, sticky=EW))
        self.edit_expense_button = (Button(self.input_frame, text="Edit Expense", font=self.font_config,
                                          bg='#9D44C0', fg='white',
                                     command=self.edit_expense, width=10, )
                                    .grid(row=2, column=3, sticky=EW))
        self.delete_expense_button = (Button(self.input_frame, text="Del Expense", font=self.font_config,
                                            bg='#9D44C0', fg='white',
                                       command=self.delete_expense, width=10, )
                                      .grid(row=3, column=3, sticky=EW))
        self.add_category_button = (Button(self.input_frame, text="Add Category", font=self.font_config,
                                          bg='#9D44C0', fg='white',
                                     command=self.add_category, width=10, )
                                    .grid(row=1, column=4, sticky=EW))
        self.edit_category_button = (Button(self.input_frame, text="Edit Category", font=self.font_config,
                                           bg='#9D44C0', fg='white',
                                      command=self.edit_category, width=10, )
                                     .grid(row=2, column=4, sticky=EW))
        self.delete_category_button = Button(self.input_frame, text="Del Category", font=self.font_config,
                                             bg='#9D44C0', fg='white',
                                        command=self.remove_category, width=10, ).grid(row=3, column=4, sticky=EW)
        self.save_file_button = (Button(self.input_frame, text="Save updates", font=self.font_config, bg='#FFC436',
                                  command=self.save_user, width=10, )
                                 .grid(row=1, column=5, sticky=EW))
        self.report_button = (Button(self.input_frame, text="Report", font=self.font_config, bg='#FFC436',
                               command=self.get_report, width=10, )
                              .grid(row=2, column=5, sticky=EW))
        self.exit_button = (Button(self.input_frame, text="Exit", font=self.font_config, bg='#7A9D54',
                             command=lambda: self.root.destroy(), width=10, )
                            .grid(row=3, column=5, sticky=EW))

    def get_today(self):
        self.expense_date_entry_box.set_date(datetime.date.today())

    def update_expense_category_entry_box(self):
        self.expense_category_entry_box.configure(values=list(self.user.categories))

    def add_expense(self):
        try:
            current_category = self.category_var.get()
            if not current_category:
                raise  ValueError('Select category! if none are to be selected, add them')
            self.user.add_expense(ExpenseDTO( category_id=current_category,
                                 amount=self.__check_amount_positive_number(),
                                              current_date=self.expense_date_entry_box.get_date()))
        except ValueError as ex:
            messagebox.showerror('Incorrect Data input', ex)

    def select_expense(self,event):
        selected = self.expense_table.focus()
        val = self.expense_table.item(selected, 'values')
        print(val)

        try:
            cur_date = datetime.datetime.strptime(val[3], '%d/%b/%y').date()
            self.selected_row_expense_id = val[0]
            self.amount_var.set(val[1])
            self.category_var.set(val[2])
            self.expense_date_entry_box.set_date(cur_date)
        except Exception as ex:
            messagebox.showerror('Error', ex)

    def edit_expense(self):

        selected = self.expense_table.focus()

        try:
            self.user.edit_expense(Expense(id=int(self.selected_row_expense_id),category_id=self.category_var.get(),
                                      amount=self.__check_amount_positive_number(), current_date=self.expense_date_entry_box.get_date()))
            self.expense_table.item( selected, values=(self.selected_row_expense_id, self.amount_var.get(),
                                                 self.category_var.get(), self.expense_date_entry_box.get_date()))
        except ValueError as ex:
            messagebox.showerror('Incorrect Data input', ex)
        except Exception as ex:
            messagebox.showerror('Error', ex)

        self.expense_table.after(500, self.refreshData())

    def delete_expense(self):
        self.user.delete_expense(int(self.selected_row_expense_id))
        self.refreshData()

    def add_category(self):
        try:
            self.user.add_category(simpledialog
                          .askstring("New category", "Please enter category name")
                          .capitalize())
        except ValueError as ex:
            messagebox.showerror("Invalid data", ex)
        finally:
            self.update_expense_category_entry_box()

    def edit_category(self):
        edit_category_view = EditCategoryView(self.user, self.update_expense_category_entry_box)

    def remove_category(self):
        remove_cat_window = RemoveCategoryView(self.user, self.update_expense_category_entry_box)

    def get_report(self):
        report = ReportView(self.user.expenses.copy())

    def load_expenses(self):
        all_expenses = self.user.expenses
        for counter in all_expenses:
            curr_exp = all_expenses[counter]
            self.expense_table.insert(parent='', index='end', iid=counter,
                                 values=(curr_exp.id, curr_exp.amount, curr_exp.category_id,
                                         curr_exp.date.strftime('%d/%b/%y')))

        self.expense_table.after(500, self.refreshData)

    def refreshData(self):
        for it in self.expense_table.get_children():
            self.expense_table.delete(it)
        self.load_expenses()
    def __check_amount_positive_number(self) -> float:
        amt = float(self.amount_var.get())
        if amt <= 0:
            raise ValueError('Amounts are entered as positive numbers')
        return amt

    def save_user(self):
        try:
            SavingService.save_user_data(self.user)
            messagebox.showinfo('Data saved', f'File for {self.user.name} was saved successfully')
        except Exception as ex:
            messagebox.showerror("Saving error", ex)