from collections import UserDict, defaultdict
from datetime import date, datetime, timedelta
from contact_book import AssistantBot, AddressBook, Record, Name, Phone, Birthday
from rich.console import Console
from rich.table import Table


console = Console()

# список имен у кого день рождения на указанною дату
def birthdays_for_date(day):
    date = datetime.strptime(day, '%Y.%m.%d').date()
    assistent_bot = AssistantBot()
    date_today = date.today()             
    contact_birth = []
    for n, rec in assistent_bot.phone_book.data.items():
        name = n
        birth = rec.birthday.value.replace(year=date_today.year)
        if birth == date:
            contact_birth.append(name)
        
    if len(contact_birth) == 0:
        print(f'\033[38;2;10;235;190mNo Birthday this day.\033[0m')
        return None
    return contact_birth

# Displaying birthdays for the current date
def birthdays_for_date_menu():
    assistent_bot = AssistantBot()
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width = 100)
    table.add_column("Name", style="red", justify="center")
    today_data = datetime.today().date()
    today_data_str = today_data.strftime('%Y.%m.%d')
    if not assistent_bot.phone_book:
        print(f'\033[91mNo contacts.\033[0m')
        return
    else:
        birth = birthdays_for_date(today_data_str)
        if birth:
            s = ''
            for el in birth:
                s += '| ' + el + ' |'
            table.add_row(s)
            console.print(table)

# список имен у кого дни рождения на неделю от сегоднешней даты
# {'Monday': ['Masha'], 'Tuesday': ['Pavel'], 'Wednesday': ['Stiv']}
def get_birthdays_per_week():
    assistent_bot = AssistantBot()
    date_today = date.today()          
    birthday_per_week = []
    for n, rec in assistent_bot.phone_book.data.items():
        name = n
        birth = rec.birthday.value.replace(year=date_today.year)
        if birth < date_today - timedelta(days=1):
            birth = birth.replace(year=date_today.year+1)
        day_week = birth.isoweekday()
        end_date = date_today + timedelta(days=7)
        if date_today <= birth <= end_date:
            birthday_per_week.append([name, birth, day_week])
    if len(birthday_per_week) == 0:
        print(f'\033[38;2;10;235;190mNo Birthday this week.\033[0m')
        return None
    users = defaultdict(list)
    for item in birthday_per_week:
        if item[2] == 1 or item[2] == 6 or item[2] == 7:
            users['Monday'].append(item[0])
        if item[2] == 2:
            users['Tuesday'].append(item[0])   
        if item[2] == 3:
            users['Wednesday'].append(item[0])
        if item[2] == 4:
            users['Thursday'].append(item[0])
        if item[2] == 5:
            users['Friday'].append(item[0])
        if item[2] == 6:
            users['Satturday'].append(item[0])
        if item[2] == 7:
            users['Sunday'].append(item[0])
    return {key: value for key, value in users.items() if value} 

# List of birthdays this week
def get_birthdays_per_week_menu():
    assistent_bot = AssistantBot()
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width = 100)
    table.add_column("Day of the week", style="red", justify="center")
    table.add_column("Names", style="bold blue", justify="center")
    if not assistent_bot.phone_book:
        print(f'\033[91mNo contacts.\033[0m')
        return
    birthdays = get_birthdays_per_week()
    if birthdays:
        for k, v in birthdays.items():
            v_1 = ', '.join(p for p in v)
            table.add_row(k, v_1)
        console.print(table)


# виводити список контактів, у яких день народження через задану кількість днів від поточної дати
def birthday_in_given_days(value):
    assistent_bot = AssistantBot()
    date_today = date.today()
    date_value = date_today + timedelta(days=value)         
    contact_birth = []
    for n, rec in assistent_bot.phone_book.data.items():
        name = n
        birth = rec.birthday.value.replace(year=date_today.year)
        if date_today <=  birth <= date_value:
            contact_birth.append(f'{name}: {rec.birthday.value}')

    if len(contact_birth) == 0:
        print(f'\033[38;2;10;235;190mNo Birthday during this period.\033[0m')
        return None
    
    return contact_birth

# Displaying birthdays for a number of days
def birthday_in_given_days_menu():
    assistent_bot = AssistantBot()
    table = Table(title="Birthdays information", style="cyan", title_style="bold magenta", width = 100)
    table.add_column("Name", style="red", justify="center")
    table.add_column("Date of birth", style="bold blue", justify="center")
    if not assistent_bot.phone_book:
        print(f'\033[91mNo contacts.\033[0m')
        return
    while True:
        print(f'\033[38;2;10;235;190mEnter the required number of days or press ENTER to skip.')
        item_number = input('Enter the number=> \033[0m')
        if item_number:
            if item_number.isdigit() :
                # Введено число
                item_number = int(item_number)
                days_birth = birthday_in_given_days(item_number)
                if days_birth:
                    for elem in days_birth:
                        item = elem.split(':')
                        table.add_row(item[0], item[1])
                    console.print(table)
                    return
            elif item_number.isalpha():
                # Введены буквы
                print(f'\033[91mYou entered letters: {item_number}\033[0m')
            else:
                # Введены буквы
                print(f'\033[91mYou entered lettersYou entered letters.: {item_number}\033[0m')

        return


if __name__ == "__main__":
    pass


   
