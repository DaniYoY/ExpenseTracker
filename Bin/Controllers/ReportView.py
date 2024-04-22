from datetime import date
from tkinter import *
from Bin.Models.ExpenseModel import Expense
import matplotlib.pyplot as plt
import numpy as np
from tkcalendar import DateEntry
import pandas as pd

class ReportView(Toplevel):
    def __init__(self, expenses:dict[int,Expense]):
        super().__init__()
        self.title('Reports')
        self.configure(background='#A1CCD1')
        self.start_date_calendar_var = StringVar()
        self.end_date_calendar_var = StringVar()
        self.report_type_var = IntVar()

        self.total_cost = 0
        self.all_expense_categories :list[str] = list()
        self.all_expenses :list[str] = list()
        self.earliest_date : date = date.min
        self.latest_date : date = date.today()
        self.set_expenes_data(expenses)

        self.categories_listbox = Listbox(self, selectmode=MULTIPLE, background='#016A70', fg='white',
                                          listvariable=StringVar(value=self.all_expense_categories))
        self.categories_listbox.grid(row=0, column=0, sticky=NS)

        self.start_date_label = Label(self, text='Enter start date', background='#A1CCD1')
        self.start_date_label.grid(row=1, column=0, sticky=NS)
        self.start_date_button = Button(self, text='DateEntry',background='darkblue', foreground='white', borderwidth=2,
                                        command=lambda :self.select_date(is_start=True))
        self.start_date_button.grid(row=2, column=0,sticky=NS)
        self.start_date_selected_label = Label(self,background='#A1CCD1')
        self.start_date_selected_label.grid(row=3, column=0, sticky=NS)
        self.show_start_date()

        self.end_date_label = Label(self, text='Enter end date',background='#A1CCD1')
        self.end_date_label.grid(row=4, column=0, sticky=NS)
        self.end_date_button = Button(self, text='DateEntry', background='darkblue', foreground='white', borderwidth=2,
                                      command=lambda :self.select_date(is_start=False))
        self.end_date_button.grid(row=5, column=0, sticky=NS)
        self.end_date_selected_label = Label(self, background='#A1CCD1')
        self.end_date_selected_label .grid(row=6, column=0, sticky=NS)
        self.show_end_date()

        self.expense_per_month_radiobutton = Radiobutton(self, text='1. Total expense per month for the period',
                                                         background='#A1CCD1',
                                                         variable=self.report_type_var, value=1,
                                                         command=self.show_report_type)
        self.expense_per_month_radiobutton.grid(row=7, column=0, sticky=NS)
        self.expense_per_category_radiobutton = Radiobutton(self, text='2. Expense per category for the period',
                                                            background='#A1CCD1',
                                                            variable=self.report_type_var, value=2,
                                                            command=self.show_report_type)
        self.expense_per_category_radiobutton.grid(row=8, column=0, sticky=NS)
        self.report_type_sel_label = Label(self,background='#A1CCD1')
        self.report_type_sel_label.grid(row=9, column=0,sticky=NS)
        self.report_generate_button = Button(self, text="Generate Report", bg='#016A70', fg='white',
                                    command=self.generate_report, width=15)
        self.report_generate_button.grid(row=10, column=0,sticky=NS)

        self.exit_button = Button(self, text="Exit Reporting", bg='#016A70', fg='white',
                                         command=lambda : self.destroy(), width=15)
        self.exit_button.grid(row=11, column=0, sticky=NS)
    def set_expenes_data(self, expenses:dict[int,Expense]) -> list:
        cat_list = set()
        for key in expenses:
            cat_list.add(expenses[key].category_id)
            self.total_cost +=expenses[key].amount
            if self.earliest_date == date.min:
                self.earliest_date = expenses[key].date
            self.earliest_date = min(self.earliest_date, expenses[key].date)

        self.all_expenses = list(expenses.values())
        self.all_expense_categories = list(cat_list)

    def show_report_type(self):

        self.report_type_sel_label.configure(text=f'Option {self.report_type_var.get()} is selected')

    def show_start_date(self):
        self.start_date_selected_label.configure(text=f'Start Date: {self.earliest_date.strftime("%d %m %Y")} is selected')

    def show_end_date(self):
        self.end_date_selected_label.configure(text=f'End Date: {self.latest_date.strftime("%d %m %Y")} is selected')

    def select_date(self,*,is_start: bool=True):
        def assign_date(e):
            selected_date = calendar_date_entry.get_date()
            if is_start:
                self.earliest_date = selected_date
                self.show_start_date()
            else:
                self.latest_date = selected_date
                self.show_end_date()

        calendar_window = Toplevel(self)

        Label(calendar_window, text='Choose date').pack(padx=10, pady=10)
        calendar_date_entry = DateEntry(calendar_window, width=12, background='darkblue',                        foreground='white', borderwidth=2,
                        date_pattern='dd/MM/yyyy')
        calendar_date_entry.pack(padx=10, pady=10)
        calendar_date_entry.bind("<<DateEntrySelected>>", assign_date)
        Button(calendar_window, text='OK', background='darkblue',   foreground='white', borderwidth=2,
                                      command=calendar_window.destroy).pack(padx=10, pady=10)

    def generate_report(self):
        reports = {
            1: self.generate_monthly_view,
            2: self.generate_category_view
        }
        chosen_categories = self.all_expense_categories
        selected_categories = self.categories_listbox.curselection()
        if selected_categories:
            chosen_categories.clear()
            for category_index in selected_categories:
                chosen_categories.append(self.categories_listbox.get(category_index))

        filtered_expenses: list[Expense] = list(filter(lambda exp: self.earliest_date <= exp.date <= self.latest_date
                                                       and exp.category_id in chosen_categories,
                                                       self.all_expenses))

        reports[self.report_type_var.get()]( filtered_expenses)

    def generate_category_view(self,  filtered_expenses: list[Expense]):
        category_spend = dict()
        for exp in filtered_expenses:
                if exp.category_id not in category_spend.keys():
                    category_spend[exp.category_id] = 0
                category_spend[exp.category_id] += exp.amount
        category_spend_label_view = [str(f'{x}: {category_spend[x]}') for x in category_spend.keys()]

        colors = plt.get_cmap('BuGn')(np.linspace(0.2, 1, len(filtered_expenses)))

        # plot
        fig, ax = plt.subplots()

        ax.pie(category_spend.values(), labels=category_spend_label_view,colors=colors,
               radius=4, center=(5, 5),
               autopct= lambda pct: str(f'{pct:.2f}'),
               textprops=dict(color='black'),
               wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

        ax.set(xlim=(0, 10), xticks=np.arange(1, 10),
               ylim=(0, 10), yticks=np.arange(1, 10))

        plt.show()

    def generate_monthly_view(self,  filtered_expenses: list[Expense]):
        month_list = pd.period_range(start=self.earliest_date, end=self.latest_date, freq='M')
        month_list = [month.strftime("%m %Y") for month in month_list]
        grouped_expenses = dict().fromkeys(month_list,0)
        print(grouped_expenses.keys())
        for exp in filtered_expenses:
            cust_key = exp.date.strftime("%m %Y")
            grouped_expenses[cust_key] += exp.amount

        plt.bar(grouped_expenses.keys(), grouped_expenses.values(), color='#116D6E')
        plt.xlabel('Month - Year')
        plt.ylabel('Amount')
        plt.show()
