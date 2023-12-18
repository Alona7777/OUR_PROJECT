from collections import UserDict
import cmd
from datetime import date, datetime, timedelta
import pickle
import os
import re


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass

class Address(Field):
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value: str):
        self.__value = value

    def __str__(self):
        return str(self.__value) 
    
class Email(Field):
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value: str):
        pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, value) is None:
            raise ValueError('Invalid email')
        self.__value = value
    def __str__(self):
        return str(self.__value)   

class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except ValueError:
            raise ValueError('No such date exists')
        
    def __str__(self):
        return self.__value.strftime('%Y.%m.%d')


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('The phone number should be digits only and have 10 symbols')
        self.__value = value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, value: str):
        phone = Phone(value)
        self.phones.append(phone)
    
    def add_email(self, value: str):
        self.email = Email(value)
    
    def add_address(self, value: str):
        self.address = Address(value)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return f'The phone number: {phone} has been deleted'   
        return f'The phone number {phone} not found'

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f'Phones: {"; ".join(p.value for p in self.phones)}'
        raise ValueError(f'Phone: {old_phone} not found!')

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def days_to_birthday(self):
        if self.birthday is None:
            return None
        date_today = date.today()
        birthday_date = self.birthday.value.replace(year=date_today.year)
        if date_today == birthday_date:
            return 'Birthday today'
        if birthday_date <= date_today - timedelta(days=1):
            birthday_date = birthday_date.replace(year=date_today.year + 1)
        day_to_birthday = (birthday_date - date_today).days
        return day_to_birthday

    def __str__(self):
        # return f"|| Name: {self.name.value}  || Phones: {'; '.join(p.value for p in self.phones)}; " \
        #        f"|| Day to birthday: {self.days_to_birthday()}||"
         return f"|| Name: {self.name.value}  || Phones: {'; '.join(p.value for p in self.phones)}; "\
               f"|| Birthday: {self.birthday}  || Email: {self.email}  || Adress: {self.address}"\
               f"|| Days to birthday: {self.days_to_birthday()}||"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file = 'Phone_Book.bin'

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        return None
        
    def search(self, value: str):                    
        if len(value) < 3:
            return 'To search by name you need at least 3 letters or 3 numbers to search by phone number'
        search_contact = []
        for name, rec in self.data.items():
            if value in name:
                search_contact.append(name)
            for item in rec.phones:
                if value in item.value:
                    search_contact.append(name)    
        if len(search_contact) != 0:
            return search_contact
        else:
            return 'No matches found'

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)
            return f'The contact {name} has been deleted'
        else:
            return f'The contact {name} not found'
        
    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        yield result
     
    def write_to_file(self):
        with open(self.file, 'wb') as file:
            pickle.dump(self.data, file)
    
    def read_from_file(self):
        with open(self.file, 'rb') as file:
            self.data = pickle.load(file)
        return self.data
        

class Controller(cmd.Cmd):
    def exit(self):
        self.book.dump()
        return True 

    # декоратор по исправлению ошибок. НАПИСАН КОРЯВО, нужно редактировать!!!


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return 'No user with this name'
        except ValueError:
            return 'The phone number should be digits only and have 10 symbols'
        except IndexError:
            return 'Enter user name'
    return inner      


'''эта часть кода отвечает за выполнение команд'''


class AssistantBot:
    def __init__(self):
        self.phone_book = AddressBook()
        if os.path.isfile(self.phone_book.file):      # запуск файла с сохранеными контактами!!!
            self.phone_book.read_from_file()
    
    # добавление нового контакта
    @input_error
    def add_contact(self):
        name = input('Enter name=> ')
        record = Record(name)
        while True:
            print('Do you want to add the phone number? Please enter the number:\n1.YES\n2.NO')
            res_1 = input('Enter your text=>  ').lower()
            if res_1 in ('1', 'yes'):
                self.add_phone(record)
                print('Do you want to add anothe phone number? Please enter the number:\n1.YES\n2.NO')
                res_2 = input('Enter your text=>  ').lower()
                if res_2 in ('1', 'yes'):
                    self.add_phone(record)
            elif res_1 in ('2', 'no'):
                break
            else:
                print("Invalid input. Please enter '1' for YES or '2' for NO.")
        while True:
            print('Do you want to add the date of birthday? Please enter the number:\n1.YES\n2.NO')
            res_2 = input('Enter your text=>  ').lower()
            if res_2 in ('1', 'yes'):
                self.add_birthday(record)
                break
            elif res_2 in ('2', 'no'):
                break
            else:
                print("Invalid input. Please enter '1' for YES or '2' for NO.")
        self.phone_book.add_record(record)
        return f'You have created a new contact:\n{str(record)}'
    
    # добавление даты рождения
    @input_error
    def add_phone(self, record):
        while True:
            try:
                phone = input('Enter phone=> ')
                record.add_phone(phone)
                self.phone_book.add_record(record)
                return '\033[92mThe phone number added successfully\033[0m'  # Сообщение о успешном добавлении
            except ValueError as e:
                print(e)
    
  # добавление даты рождения
    @input_error   
    def input_year(self):
        while True:
            year = input('Enter the year (YYYY)=> ')
            if year.isdigit() and 1900 <= int(year) <= 2100:
                return year
            else:
                print("Invalid year. Please enter a valid year in format YYYY.")
    def input_month(self):
        while True:
            month = input('Enter the month (MM)=> ')
            if month.isdigit() and 1 <= int(month) <= 12:
                return month.zfill(2)  # Добавляем ведущий ноль, если нужно
            else:
                print("Invalid month. Please enter a valid month (1-12).")
    def input_day(self):
        while True:
            day = input('Enter the day (DD)=> ')
            if day.isdigit() and 1 <= int(day) <= 31:  # Простая проверка, не учитывающая количество дней в месяце
                return day.zfill(2)  # Добавляем ведущий ноль, если нужно
            else:
                print("Invalid day. Please enter a valid day (1-31).")
    def add_birthday(self, record):
        if not record:
            print('\033[91mThe contact does not exist\033[0m')
            return
        year = self.input_year()
        month = self.input_month()
        day = self.input_day()
        birth = f'{year}.{month}.{day}'
        try:
            record.add_birthday(birth)
            self.phone_book.add_record(record)
            return f'You added the date of birthday {birth} to the contact:\n{str(record)}'
        except ValueError as e:
            print(e)
            print('Please enter a valid date in format YYYY.MM.DD')
            return self.add_birthday(record)  # Повторный вызов функции при ошибке ввода
     
    # "меню" для добавления  
    @input_error
    def add(self):
        print('='*100)
        print('Please enter the number\nYou can add:\n1.CONTACT\n2.PHONE\n3.BIRTHDAY')
        res = input('Enter your text=>  ').lower()
        if res in ('1', 'contact'):
            result = self.add_contact()
        else:
            name = input('Enter the name of an existing contact=> ')
            record: Record = self.phone_book.find(name)
            if res in ('2', 'phone'):
                result = self.add_phone(record)
            if res in ('3', 'birthday'):
                result = self.add_birthday(record)
        return result
    
    # изменение телефона
    @input_error
    def change_phone(self, record: Record):
        old_phone = input('Enter the phone number you want to change=> ')
        new_phone = input('Enter the new phone number=> ')
        record.edit_phone(old_phone, new_phone)
        self.phone_book.add_record(record)
        return f'You changed the contact:\n{str(record)}'
    
    # изменение даты рождения
    @input_error    
    def change_birth(self, record):
        self.add_birthday(record)
        return f'You changed the contact:\n{str(record)}' 
    
    # "меню" для изменения 
    @input_error
    def change(self):
        print('='*100)
        print('Please enter the number\nYou can change:\n1.PHONE NUMBER\n2.DATE OF BIRTHDAY')
        res = input('Enter your text=>  ').lower()
        print('You can change the information in an existing contact')
        name = input('Enter name=> ')
        record: Record = self.phone_book.find(name)
        if res in ('1', 'phone', 'phone number'):
            result = self.change_phone(record)
            print('Do you want change the date of birthday?Please enter the number:\n1.YES\n2.NO')
            res_1 = input('Enter your text=>  ').lower()
            if res_1 in ('1', 'yes'):
                result = self.change_birth(record)        
        if res in ('2', 'date', 'birth', 'date of birthday'):
            result = self.change_birth(record)
            print('Do you want change the phone number?Please enter the number:\n1.YES\n2.NO')
            res_1 = input('Enter your text=>  ').lower()
            if res_1 in ('1', 'yes'):
                result = self.change_phone(record)
        return result
    
        # удаление номера
    @input_error
    def delete_phone(self, record: Record):
        phone = input('Enter phone=> ')
        result = record.remove_phone(phone)
        return result
    
    # удаление даты рождения
    @input_error   
    def delete_birth(self, record):
        record.birthday = None
        return 'Date of birth removed'
    
    # удаление контакта
    @input_error       
    def delete_contact(self):
        name = input('Enter name=> ')
        result = self.phone_book.delete(name)
        return result
    
    # "меню" для удаления       
    @input_error
    def delete(self):
        print('='*100)
        print('Please enter the number\nYou can delete:\n1.CONTACT\n2.INFO IN AN EXISTING CONTACT')
        res = input('Enter your text=>  ').lower()
        if res in ('1', 'contact'):
            result = self.delete_contact()
        if res in ('2', 'info', 'info in an existing contact', 'existing contact'):
            name = input('Enter the name of an existing contact => ')
            record: Record = self.phone_book.find(name)
            print('Please enter the number\nYou can delete:\n1.PHONE NUMBER\n2.DATE OF BIRTH')
            res_1 = input('Enter your text=>  ').lower()
            if res_1 in ('1', 'phone', 'phone number'):
                self.delete_phone(record)
            if res_1 in ('2', 'birth', 'date', 'date of birth'):
                self.delete_birth(record)
                self.phone_book.add_record(record)
            return str(record)
        return result

# поиск по имени и по совпадениям
    @input_error
    def search(self):
        print('='*100)
        print('Do you know the contact name? Please enter the number:\n1.YES\n2.NO')
        res = input('Enter your text=>  ').lower()
        if res == '1' or res == 'yes':
            name = input('Enter name=> ')
            return self.phone_book.find(name)
        print('If you don\'t know the contact\'s name, enter at least three digits of phone number or at least three letters of the name')
        res_1 = input('Enter your text=>  ').lower()
        return self.phone_book.search(res_1)

    # работа через интератор не сделана правильно
    @input_error
    def show_all(self):
        print('='*100)
        print('Do you want to display all contacts? Please enter the number:\n1.YES\n2.NO')
        res = input('Enter your text=>  ').lower()
        if res == '1' or res == 'yes':
            if self.phone_book:
                phones = f'Contacts:\n'
                for name, record in self.phone_book.data.items():
                    phones += f'{str(record)}\n'
                return phones
            else:
                return 'No contacts'
        print('How many contacts to display?')
        res_1 = input('Enter your text=>  ')
        if res_1.isdigit():
            return self.phone_book.iterator(res_1)
        
        # выход из програмы и сохранение файла!
    def exit(self):
        self.phone_book.write_to_file()
        return 

# эта часть отвечает за команды телефонной книги, нет адреса и email  


def main():
    assistent_bot = AssistantBot()
    print('Hello!')
    while True:
        print('=' * 100)
        print('How can I help you?\nPlease enter the number:\n1.ADD\n2.CHANGE\n3.DELETE\n4.SEARCH\n5.SHOW ALL\n6.EXIT')
        command = input('Enter your text=>  ').lower()
        if command in ('1', 'add'):
            result = assistent_bot.add()
        elif command in ('2', 'change'):
            result = assistent_bot.change()
        elif command in ('3', 'delete'):
            result = assistent_bot.delete()
        elif command in ('4', 'search'):
            result = assistent_bot.search() 
        elif command in ('5', 'show all', 'show'):
            result = assistent_bot.show_all()   
        elif command in ('6', 'exit'):
            assistent_bot.exit()
            print('Good bye!')
            break
        else:
            result = 'Command not found, try again'
        print(result)


if __name__ == "__main__":
    main()
