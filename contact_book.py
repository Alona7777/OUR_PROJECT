from collections import UserDict
import cmd
from datetime import date, datetime, timedelta
import pickle
import os


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


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except ValueError:
            raise ValueError('The birsday date must be in format: 2022.01.01')


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('The phone number should be digits only and have 10 symbols')
        self.__value = value


class Note:
    def __init__(self, content, tags=None):
        if tags is None:
            tags = []
        self.content = content
        self.tags = tags


class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, content, tags=None):
        if tags is None:
            tags = []
        note = Note(content, tags)
        self.notes.append(note)

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def display_all_notes(self):
        if not self.notes:
            print('List empty')
        for i, note in enumerate(self.notes, 1):
            print(f"{i}. Content:{note.content}, Tags:{note.tags}")

    def edit_note_content(self, index, new_content):
        if 1 <= index <= len(self.notes):
            self.notes[index - 1].content = new_content
        else:
            print("Invalid note index.")

    def delete_note_by_index(self, index):
        if 1 <= index <= len(self.notes):
            del self.notes[index - 1]
        else:
            print("Invalid note index.")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value: str):
        phone = Phone(value)
        self.phones.append(phone)

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
        return f"|| Name: {self.name.value}  || Phones: {'; '.join(p.value for p in self.phones)}; " \
               f"|| Day to birthday: {self.days_to_birthday()}||"
        # return '||Name: {:^10}||Phones: {:<20}||Day to Birthday: {:^7}'.format(self.name.value, '; '.join(p.value for p in self.phones), self.days_to_birthday())


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
        print('Do you want to add the phone number? Please enter the number:\n1.YES\n2.NO')
        res_1 = input('Enter your text=>  ').lower()
        if res_1 == '1' or res_1 == 'yes':
            self.add_phone(record)
        print('Do you want to add the date of birthday? Please enter the number:\n1.YES\n2.NO')
        res_2 = input('Enter your text=>  ').lower()
        if res_2 == '1' or res_2 == 'yes':
            self.add_birthday(record)
        self.phone_book.add_record(record)
        return f'You have created a new contact:\n{str(record)}'
    
    # добавление даты рождения
    @input_error
    def add_phone(self, record):
        phone = input('Enter phone=> ')
        record.add_phone(phone)
        self.phone_book.add_record(record)
        return f'You added a phone number {phone} to the contact:\n{str(record)}'
    
    # добавление даты рождения
    @input_error   
    def add_birthday(self, record):
        year = input('Enter the year=> ')
        month = input('Enter the month=> ')
        day = input('Enter the day=> ')
        birth = f'{year}.{month}.{day}'
        record.add_birthday(birth)
        self.phone_book.add_record(record)
        return f'You added the date of birthday {birth} to the contact:\n{str(record)} '
     
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
        if command in ('2', 'change'):
            result = assistent_bot.change()
        if command in ('3', 'delete'):
            result = assistent_bot.delete()
        if command in ('4', 'search'):
            result = assistent_bot.search() 
        if command in ('5', 'show all', 'show'):
            result = assistent_bot.show_all()
        if command in ('6', 'exit'):
            assistent_bot.exit()
            print('Good bye!')
            break
        print(result)


if __name__ == "__main__":
    main()
