from Bin.Models.ExpenseModel import Expense
from Bin.Models.ExpenseDTOModel import ExpenseDTO
# from random import randint
from numpy import random

class User:

    def __init__(self, name, expenses:dict[int,Expense]=dict(), categories:set[str]=set(), latest_id:int =0):
        self.__name = name
        self.__expenses : dict[int, Expense] = expenses
        self.__categories: set[str] = categories
        self.__latest_id = latest_id

    def add_expense(self, dto: ExpenseDTO):
        new_expense =    Expense(self.__generate_id(), dto.category_id, dto.amount, dto.date)
        self.expenses[new_expense.id] = new_expense

    def edit_expense(self, expense: Expense):
        self.expenses[expense.id] = expense

    def delete_expense(self, id):
        self.expenses.pop(id)

    def add_category(self, category_name: str):
        ''''adds new category to the user, if it exists raises exception'''
        if category_name in self.categories:
            raise  ValueError(f"{category_name} already exists!")
        self.__categories.add(category_name)

    def edit_category(self, new_name: str, old_name: str):
        ''''edits the category and updates all expenses'''
        self.add_category(new_name)
        for key in self.expenses:
            if self.expenses[key].category_id == old_name:
                self.expenses[key].category_id = new_name
        self.categories.remove(old_name)

    def delete_category(self, old_name: str):
        '''remove the category for future uses, current uses are set to N/A category '''
        self.edit_category('N/A',old_name)

    @property
    def expenses(self):
        return self.__expenses

    @property
    def categories(self):
        return self.__categories

    @property
    def name(self):
        return self.__name

    def __generate_id(self) -> int:
        new_id= self.__latest_id +1
        self.__latest_id = new_id
        return new_id



