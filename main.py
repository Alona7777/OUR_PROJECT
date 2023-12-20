from collections import UserDict
import cmd
from datetime import date, datetime, timedelta
import pickle
import os
import questionary
from termcolor import colored
import time
from contact_book import AssistantBot, Record, Name, Phone, Birthday


def start_menu():
    assistent_bot = AssistantBot()

    current_menu_number = 1
    # old_menu_number = 0
    text_colors = 'cyan'
    print(colored('Hello!', text_colors))

    # Function definitions
    def f_exit():
        assistent_bot.exit()
        print(colored('Good bye!', text_colors))
        # time.sleep(1)
        exit()

    # Заменить на реальные функции
    def f_add():
        print(f'Вы ввели: add')

    # Функция заглушка
    def function_stub():
        pass

    commands_start = {
        'ADD': [function_stub, 2, 1],
        'CHARGE': [function_stub, 3, 1],
        'DELETE': [function_stub, 4, 1],
        'SEARCH': [assistent_bot.search, 5, 1],
        'SHOW ALL': [assistent_bot.show_all, 1, 1],
        'EXIT': [f_exit, 2, 1],
    }

    commands_add = {
        'CONTACT': [assistent_bot.add_contact, 1, 1],
        'PHONE': [assistent_bot.add_phone_menu, 1, 1],
        'BIRTHDAY': [assistent_bot.add_birthday_menu, 1, 1],
        'EMAIL': [function_stub, 1, 1],
        'NOTE': [function_stub, 7, 1],
        'BACK': [function_stub, 1, 0],
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 0, 0],
    }

    commands_change = {
        'NAME': [assistent_bot.edit_name, 1, 1],
        'PHONE': [assistent_bot.edit_phone_menu, 1, 1],
        'BIRTHDAY': [assistent_bot.edit_birthday_menu, 1, 1],
        'EMAIL': [assistent_bot.edit_email, 1, 1],
        'ADDRESS': [assistent_bot.edit_address, 1, 1],
        'NOTE': [function_stub, 7, 1],
        'BACK': [function_stub, 1, 0],
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 0, 0],
    }

    commands_del = {
        'CONTACT': [assistent_bot.delete_contact_menu, 1, 1],
        'PHONE': [assistent_bot.delete_phone_menu, 1, 1],
        'BIRTHDAY': [assistent_bot.delete_birthday_menu, 1, 1],
        'EMAIL': [assistent_bot.delete_email_menu, 1, 1],
        'ADDRESS': [assistent_bot.delete_address_menu, 1, 1],
        'NOTE': [function_stub, 7, 1],
        'BACK': [function_stub, 1, 0],
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 0, 0],
    }

    # Функция для получения ввода пользователя
    def get_user_input(commands_menu) :
        print(colored('=' * 100, text_colors))
        result = questionary.select('Select a team:', choices = commands_menu.keys()).ask()
        return result

    # Основной цикл ввода
    while True :
        commands_menu = commands_start
        print(colored('=' * 100, text_colors))
        if current_menu_number == 1:
            commands_menu = commands_start
            print(colored('How can I help you? Please choose: |ADD|CHANGE|DELETE|SEARCH|SHOW ALL|', text_colors))
        elif current_menu_number == 2:
            commands_menu = commands_add
            print(colored('How can I help you? Please choose: |CONTACT|PHONE|BIRTHDAY|EMAIL|NOTE|', text_colors))
        elif current_menu_number == 3:
            commands_menu = commands_change
            print(colored('What do you want to change? Please choose: |PHONE|BIRTHDAY|EMAIL|NOTE|', text_colors))
        elif current_menu_number == 4:
            commands_menu = commands_del
            print(colored('What do you want to delete? Please choose: |CONTACT|PHONE|BIRTHDAY|EMAIL|NOTE|', text_colors))
        user_input = get_user_input(commands_menu)

        current_menu_number = commands_menu[user_input][1]
        # old_menu_number = commands_menu[user_input][2]

        # Обработка введенной команды
        if user_input in commands_menu:
            # Вызов функции, соответствующей выбранной команде
            commands_menu[user_input][0]()
        else:
            print('Please select a team.')


if __name__ == "__main__":
    start_menu()
