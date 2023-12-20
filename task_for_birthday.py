
from collections import UserDict, defaultdict
from datetime import date, datetime, timedelta
from contact_book import AssistantBot, AddressBook, Record, Name, Phone, Birthday


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
        return 'No Birthday this day'
    
    return contact_birth

# список имен у кого дни рождения на неделю от сегоднешней даты
# {'Monday': ['Masha'], 'Tuesday': ['Pavel'], 'Wednesday': ['Stiv']}
def get_birthdays_per_week():
    assistent_bot = AssistantBot()
    date_today = date.today()          
    day_week_today = date_today.isoweekday() 

    dec_31 = datetime(2024, 12, 31).date().replace(year=date_today.year)
    dec_30 = datetime(2024, 12, 30).date().replace(year=date_today.year)  

    birthday_per_week = []
    for n, rec in assistent_bot.phone_book.data.items():
        name = n
        birth = rec.birthday.value.replace(year=date_today.year)
        if date_today == datetime(2024, 1, 1).date().replace(year=date_today.year) and day_week_today == 1:
            if birth == dec_30 or birth == dec_31:
                birth = birth.replace(year=date_today.year-1)

        if birth < date_today - timedelta(days=3):
            birth = birth.replace(year=date_today.year+1)
        day_week = birth.isoweekday()
        
        if day_week_today == 1:
            start_date = date_today - timedelta(days=2)
            end_date = date_today + timedelta(days=4)
            if start_date <= birth <= end_date:
                birthday_per_week.append([name, birth, day_week])

        else:
            end_date = date_today + timedelta(days=6)
            if date_today <= birth <= end_date:
                birthday_per_week.append([name, birth, day_week])
    if len(birthday_per_week) == 0:
        return 'No Birthday this week'

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
    return {key: value for key, value in users.items() if value} 


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
            contact_birth.append(name)
    if len(contact_birth) == 0:
        return 'No Birthday during this period'
    
    return contact_birth
    


if __name__ == "__main__":

    birth = birthdays_for_date('2023.12.19')
    print(birth)

    birthdays = get_birthdays_per_week()
    print(birthdays)
    
    b = birthday_in_given_days(1)
    print(b)
