import questionary
from termcolor import colored
import time
from contact_book import AssistantBot
from Note import NotesManager
from weather import anecdotes_ua_menu, anecdotes_en_menu, weather_menu
from file_sorter import sorteds_menu


def start_menu():
    assistent_bot = AssistantBot()
    notes_manager = NotesManager()

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
        'SEARCH': [assistent_bot.search, 1, 1],
        'SHOW ALL': [assistent_bot.show_all, 1, 1],
        'NOTE': [function_stub, 5, 1],
        'GOODIES': [function_stub, 6, 1],
        'EXIT': [f_exit, 2, 1],
    }

    commands_add = {
        'CONTACT': [assistent_bot.add_contact, 1, 1],
        'PHONE': [assistent_bot.add_phone_menu, 1, 1],
        'BIRTHDAY': [assistent_bot.add_birthday_menu, 1, 1],
        'EMAIL': [assistent_bot.add_email, 1, 1],
        'ADDRESS': [assistent_bot.add_address, 1, 1],
        'NOTE': [notes_manager.note_add_menu, 5, 1],
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
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 0, 0],
    }

    commands_note = {
        'ADD NOTE': [notes_manager.note_add_menu, 5, 1],
        'CHARGE NOTE': [notes_manager.note_charge_menu, 5, 1],
        'DELETE NOTE': [notes_manager.note_delete_menu, 5, 1],
        'SEARCH NOTE': [notes_manager.note_search_menu, 5, 1],
        'SHOW ALL NOTE': [notes_manager.note_show_menu, 5, 1],
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 2, 1],
    }

    commands_goodies = {
        'FILE SORTING': [sorteds_menu, 6, 1],
        'WEATHER': [weather_menu, 6, 1],
        'ANECDOTES': [function_stub, 7, 1],
        'RETURN TO MAIN MENU': [function_stub, 1, 0],
        'EXIT': [f_exit, 2, 1],
    }

    commands_anecdotes = {
        'Українскою мовою': [anecdotes_ua_menu, 6, 1],
        'English language': [anecdotes_en_menu, 6, 1],
        'EXIT': [f_exit, 2, 1],
    }
    # Функция для получения ввода пользователя
    def get_user_input(commands_menu):
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
            print(colored('We will add more? Please choose: |CONTACT|PHONE|BIRTHDAY|EMAIL|NOTE|', text_colors))
        elif current_menu_number == 3:
            commands_menu = commands_change
            print(colored('What do you want to change? Please choose: |PHONE|BIRTHDAY|EMAIL|NOTE|', text_colors))
        elif current_menu_number == 4:
            commands_menu = commands_del
            print(colored("What do you want to delete? Please choose: |CONTACT|PHONE|BIRTHDAY|EMAIL|NOTE|",
                          text_colors))
        elif current_menu_number == 5:
            commands_menu = commands_note
            print(colored('How can I help you? Please choose: |ADD NOTE|CHARGE NOTE|DELETE NOTE|SEARCH NOTE|'
                          'SHOW ALL NOTE|', text_colors))
        elif current_menu_number == 6:
            commands_menu = commands_goodies
            print(colored('How can I help you? Please choose: |FILE SORTING|WEATHER|ANECDOTES|', text_colors))
        elif current_menu_number == 7:
            commands_menu = commands_anecdotes
            print(colored('Choose language. Please choose: |Українскою мовою|English language|', text_colors))

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
