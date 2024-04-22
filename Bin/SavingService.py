from Bin.Models.UserModel import User
import pickle
import os
import sys


class SavingService:

    @staticmethod
    def load_user_data( username: str) -> User:
        user =User(username)
        if os.path.exists(f'{username}.pickle'):
            with open(f'{os.getcwd()}/Data/{username}.pickle', 'rb') as filehandler_expenses:
                user = pickle.load(filehandler_expenses)
        else:
            print(f'file {username} not found')
        return user

    @staticmethod
    def save_user_data(user: User):
        with open(f'{os.getcwd()}/Data/{user.name}.pickle', 'wb') as filehandler_expenses:
            user = pickle.dump(user,filehandler_expenses)
