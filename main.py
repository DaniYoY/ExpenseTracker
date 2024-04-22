from tkinter import *
from Bin.Controllers.ExpenseTrackerView import ExpenseTrackerApp


def main():
    root = Tk()
    app = ExpenseTrackerApp(root)
    app.load_expenses()
    app.root.mainloop()


if __name__ == '__main__':
    main()
