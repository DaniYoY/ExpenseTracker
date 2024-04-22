from datetime import date


class Expense:

    def __init__(self,id: int, category_id: str, amount: float, current_date: date = date.today()):
        self.__id = id
        self.__category_id : str = category_id
        self.__amount: float = amount
        self.__date: date = current_date

    @property
    def category_id(self) -> str:
        return self.__category_id

    @category_id.setter
    def category_id(self, val: str):
        self.__category_id = val

    @property
    def id(self) -> int:
        return self.__id

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, val: float):
        self.__amount = val

    @property
    def date(self) -> date:
        return self.__date

    @date.setter
    def date(self, val: date):
        self.__date = val

    def __eq__(self, other):
        if isinstance(other, Expense):
            return (self.id, self.amount, self.category_id, self.date
            == other.id, other.amount, other.category_id, other.date)

    def __hash__(self):
        return hash(self.date, self.id,self.category_id, self.amount)

    def __str__(self):
        return f'# {self.id} - {self.amount} for {self.category_id} on {self.date}'

    def __repr__(self):
        return f'# {self.id} - {self.amount} for {self.category_id} on {self.date}'
