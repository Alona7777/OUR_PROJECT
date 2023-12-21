from collections import UserDict, defaultdict
import cmd
from datetime import date, datetime, timedelta
import pickle
import os
import re
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table


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
        if (bool(re.search(pattern, value))) is False:
            raise ValueError('\033[91mInvalid email format.\033[0m')
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
            raise ValueError('\033[91mInvalid date format. Correct format: YYYY.MM.DD\033[0m')

    def __str__(self):
        return self.__value.strftime('%Y.%m.%d')
    


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('\033[91mThe phone number should be digits only and have 10 symbols.\033[0m')
        self.__value = value

    def __str__(self):
        return(str(self.__value))


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
                return f'The phone number: {phone} has been deleted.'
        return f'The phone number {phone} not found.'

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f'Phones: {"; ".join(p.value for p in self.phones)}'
        # raise ValueError(f'Phone: {old_phone} not found!')
        return None

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    #  показывает сколько дней до дня рождения
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
        
        return f'{self.name.value}, {"; ".join(p.value for p in self.phones)}, {self.birthday}, {self.email}, {self.address}, {self.days_to_birthday()}'

        # return f"|| Name: {self.name.value}  || Phones: {'; '.join(p.value for p in self.phones)}; " \
        #        f"|| Birthday: {self.birthday}  || Email: {self.email}  || Address: {self.address}" \
        #        f"|| Days to birthday: {self.days_to_birthday()}||"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file = 'Phone_Book.bin'

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            # print(self.data[name])
            return self.data[name]
        return None

    def search(self, value: str):
        if len(value) < 3:
            return '\033[91mYou need at least 3 letters to search by name or 3 didgit to search by phone number.\033[0m'
        result = ''
        for name, rec in self.data.items():
            if value.lower() in name.lower():
                result += f'{str(rec)}\n'
            for item in rec.phones:
                if value in item.value:
                    result += f'{str(rec)}'
        if len(result) != 0:
            return result
        else:
            return None

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)
            return f'The contact {name} has been deleted.'
        else:
            return f'The contact {name} not found.'

    def iterator(self, item_number):
        counter = 0
        result = f'Contacts:\n'
        print(result)
        print(self.data)
        for item, record in self.data.items():
            result += f'{item}: {str(record)}\n'
            counter += 1
            print(counter)
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        print(result)
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
            return 'Incorrect information entered'
        except IndexError:
            return 'Enter user name'
    return inner


'''эта часть кода отвечает за выполнение команд'''


class AssistantBot:
    def __init__(self):
        self.console = Console()
        self.phone_book = AddressBook()
        if os.path.isfile(self.phone_book.file):  # запуск файла с сохранеными контактами!!!
            self.phone_book.read_from_file()

    # вывод в таблицу rich       
    def table_print(self, record: Record):
        table = Table(title="Contact Information", style="cyan", title_style="bold magenta")
        table.add_column("Name", style="red", justify="center")
        table.add_column("Phones", style="bold blue", justify="center")
        table.add_column("Birthday", style="bold green", justify="center")
        table.add_column("Email", style="bold blue", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Days to birthday", style="yellow", justify="center")
        phone_str = "\n".join(
            "; ".join(p.value for p in record.phones[i:i + 2]) for i in range(0, len(record.phones), 2))
        # {'; '.join(p.value for p in self.phones)}
        table.add_row(
            str(record.name.value),
            str(phone_str),
            str(record.birthday),
            str(record.email),
            str(record.address),
            str(record.days_to_birthday())
        )
        return table

    # отдельная функция по поиску рекорд, чтобы избежать ошибку с несущестующим контактом 
    @input_error
    def find_record(self):
        print('=' * 100)
        completer = WordCompleter(list(self.phone_book.keys()), ignore_case=True)
        name = prompt('Enter the name of an existing contact=> ', completer=completer)
        record: Record = self.phone_book.find(name)
        if record:
            return record

    # добавление нового контакта
    @input_error
    def add_contact(self):
        name = input('Enter name=> ')
        record = Record(name)
        self.add_phone(record)
        self.add_birthday(record)
        self.add_email(record)
        self.add_address(record)
        self.phone_book.add_record(record)
        contact = self.table_print(record)
        print(f'\033[92mYou have created a new contact:\033[0m')
        self.console.print(contact)
        return

    # добавление номера телефона
    @input_error
    def add_phone(self, record):
        count_phone = 1
        while True:
            try:
                print(
                    f'\033[38;2;10;235;190mPlease enter the Phone Number {count_phone}, or press ENTER to skip.\033[0m')
                phone = input('Enter phone=> ')
                if phone:
                    record.add_phone(phone)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe phone number {phone} has been added.\033[0m')
                    count_phone += 1
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_phone_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            self.add_phone(record)
            self.console.print(self.table_print(record))
            return

    # добавление даты дня рождения
    def add_birthday(self, record: Record):
        while True:
            try:
                print(f'\033[38;2;10;235;190mEnter the date of birth or press ENTER to skip.\033[0m')
                birth = input('Enter date of birth. Correct format: YYYY.MM.DD=> ')
                if birth:
                    record.add_birthday(birth)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe date of birth {birth} has been added.\033[0m')
                    return
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            elif record.birthday == None:
                self.add_birthday(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has date of birth.\033[0m')
                return

    # добаваление email  
    @input_error
    def add_email(self, record: Record):
        while True:
            try:
                print(f'\033[38;2;10;235;190mEnter the email or press ENTER to skip.\033[0m')
                email = input('Enter email=> ')
                if email:
                    record.add_email(email)
                    self.phone_book.add_record(record)
                    print(f'\033[38;2;10;235;190mThe email {email} has been added.\033[0m')
                    return
                else:
                    return
            except ValueError as e:
                print(e)

    @input_error
    def add_email_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            elif record.email == None:
                self.add_email(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has email.\033[0m')
                return

    # добавление адреса   
    @input_error
    def add_address(self, record: Record):
        print(f'\033[38;2;10;235;190mEnter your address or press ENTER to skip.\033[0m')
        address = input('Enter address=> ')
        if address:
            record.add_address(address)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe address {address} has been added.\033[0m')
            return
        else:
            return

    @input_error
    def add_address_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found\033[0m')
                return
            elif record.address == None:
                self.add_address(record)
                self.console.print(self.table_print(record))
                return
            else:
                print('\033[91mThis contact has address.\033[0m')
                return

    # изменение телефона
    @input_error
    def edit_phone(self, record: Record):
        old_phone = input('Enter the phone number you want to change=> ')
        new_phone = input('Enter the new phone number=> ')
        result = record.edit_phone(old_phone, new_phone)
        if result is None:
            print(f'\033[91mPhone: {old_phone} not found!\033[0m')
            return
        self.phone_book.add_record(record)
        print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
        self.console.print(self.table_print(record))
        return

    @input_error
    def edit_phone_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            self.edit_phone(record)
            return

    # изменение email      
    @input_error
    def edit_email(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            self.add_email(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    @input_error
    def edit_address(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            self.add_address(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    # изменение имени
    @input_error
    def edit_name(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            new_name = input('Enter new name=> ')
            if new_name:
                old_name = record.name.value
                self.phone_book.data[new_name] = self.phone_book.data.pop(old_name)
                record.name.value = new_name
                self.phone_book.add_record(record)
                print(f'\033[38;2;10;235;190mName changed successfully from {old_name} to {new_name}.\n\033[0m')
                self.console.print(self.table_print(record))
                return
            else:
                return

    # изменение даты рождения
    @input_error
    def edit_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            self.add_birthday(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление номера
    @input_error
    def delete_phone(self, record: Record):
        phone = input('Enter phone=> ')
        result = record.remove_phone(phone)
        print(f'\033[38;2;10;235;190mThe phone number {phone} was removed.\033[0m')
        return result

    @input_error
    def delete_phone_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            self.delete_phone(record)
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mYou changed the contact:\n.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление даты рождения
    @input_error
    def delete_birthday_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            record.birthday = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe date of birth was removed.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление email
    @input_error
    def delete_email_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            record.email = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe email was removed.\033[0m')
            self.console.print(self.table_print(record))
            return

    # удаление адреса
    @input_error
    def delete_address_menu(self):
        while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            record.address = None
            self.phone_book.add_record(record)
            print(f'\033[38;2;10;235;190mThe address was removed.\033[0m')
            self.console.print(self.table_print(record))
            return
        
    # удаление контакта
    @input_error
    def delete_contact_menu(self):
         while True:
            record = self.find_record()
            if not record:
                print('\033[91mThe contact was not found.\033[0m')
                return
            print(f'\033[92m{str(record)}\033[0m')
            print('\033[91mDo you really want to delete this contact? Please enter the number: 1.YES or press ENTER to skip.\033[0m')
            res = input('Enter your text=>  ').lower()
            if res in ('1', 'yes'):
                self.phone_book.delete(record.name.value)
                print(f'\033[38;2;10;235;190mThe contact {record.name.value} was removed.\033[0m')
                return 
            else:
                return

    # поиск по имени и по совпадениям
    @input_error
    def search(self):
        table = Table(title="Search results", style="cyan", title_style="bold magenta")
        table.add_column("Name", style="red", justify="center")
        table.add_column("Phones", style="bold blue", justify="center")
        table.add_column("Birthday", style="bold green", justify="center")
        table.add_column("Email", style="bold blue", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Days to birthday", style="yellow", justify="center")
        while True:
            print('=' * 100)
            print(f'\033[38;2;10;235;190mEnter at least 3 letters or numbers to search or press ENTER to exit.\033[0m')
            res = input('Enter your text=>  ').lower()
            if res:
                result = self.phone_book.search(res).split('\n')
                if result:
                    for item in result:
                        record = item.split(',')
                        table.add_row(record[0], record[1], record[2], record[3], record[4], record[5])
                        self.console.print(table)
                print(f'\033[38;2;10;235;190mNo matches found.\033[0m')        
            else:
                break
            

    # работа через интератор
    @input_error
    def show_all(self):
        table = Table(title="Contact Information", style="cyan", title_style="bold magenta")
        table.add_column("Name", style="red", justify="center")
        table.add_column("Phones", style="bold blue", justify="center")
        table.add_column("Birthday", style="bold green", justify="center")
        table.add_column("Email", style="bold blue", justify="center")
        table.add_column("Address", style="yellow", justify="center")
        table.add_column("Days to birthday", style="yellow", justify="center")
        print('=' * 100)
        print(f'\033[38;2;10;235;190mEnter how many records to display or press ENTER to skip.\033[0m')
        item_number = input('Enter number=> ')
        if not self.phone_book:
            print('No contacts')
        if item_number:
            try:
                item_number = int(item_number)
            except ValueError:
                print(f'\033[91mYou entered letters: {item_number}. Please enter only numbers.\033[0m')
            iteration_count = 0
            for name, record in self.phone_book.data.items():
                phone_str = "\n".join("; ".join(p.value for p in record.phones[i:i + 2]) for i in range(0, len(record.phones), 2))
                table.add_row(str(record.name.value), 
                            str(phone_str), 
                            str(record.birthday), 
                            str(record.email), 
                            str(record.address), 
                            str(record.days_to_birthday())
                            )
                iteration_count += 1
                if iteration_count == item_number:
                    self.console.print(table)
        else:
            for name, record in self.phone_book.data.items():
                phone_str = "\n".join("; ".join(p.value for p in record.phones[i:i + 2]) for i in range(0, len(record.phones), 2))
                table.add_row(str(record.name.value), 
                                str(phone_str), 
                                str(record.birthday), 
                                str(record.email), 
                                str(record.address), 
                                str(record.days_to_birthday())
                                )
            self.console.print(table)

    # выход из програмы и сохранение файла!
    def exit(self):
        self.phone_book.write_to_file()
        return


if __name__ == "__main__":
    pass
