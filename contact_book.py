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
        if (bool(re.search(pattern, value))) is False:
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

    #  ------------------
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
            # print(self.data[name])
            return self.data[name]
        return None

    def search(self, value: str):
        if len(value) < 3:
            return 'To search by name you need at least 3 letters or 3 numbers to search by phone number'
        search_contact = []
        result = ''
        for name, rec in self.data.items():
            if value.lower() in name.lower():
                result += f'{name}: {str(rec)}\n'
                search_contact.append(result)
            for item in rec.phones:
                if value in item.value:
                    result += f'{name}: {str(rec)}\n'
                    search_contact.append(result)
        if len(result) != 0:
            return result
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
        # while True:
        #     print('Do you want to add the phone number? Please enter the number:\n1.YES\n2.NO')
        #     res_1 = input('Enter your text=>  ').lower()
        #     if res_1 in ('1', 'yes'):
        self.add_phone(record)
            #     print('Do you want to add anothe phone number? Please enter the number:\n1.YES\n2.NO')
            #     res_2 = input('Enter your text=>  ').lower()
            #     if res_2 in ('1', 'yes'):
            #         self.add_phone(record)
            #         break
            # elif res_1 in ('2', 'no'):
            #     break
            # else:
            #     print("Invalid input. Please enter '1' for YES or '2' for NO.")
        # while True:
        #     print('Do you want to add the date of birthday? Please enter the number:\n1.YES\n2.NO')
        #     res_2 = input('Enter your text=>  ').lower()
        #     if res_2 in ('1', 'yes'):
        self.add_birthday(record)
        self.add_email(record)
        self.add_address(record)
            #     break
            # elif res_2 in ('2', 'no'):
            #     break
            # else:
            #     print("Invalid input. Please enter '1' for YES or '2' for NO.")
        self.phone_book.add_record(record)
        return f'You have created a new contact:\n{str(record)}'
    
    # добавление даты рождения
    @input_error
    def add_phone(self, record):
        count_phone = 1
        while True:
            try:
                print(f'Enter your phone number {count_phone} or press ENTER to skip.')
                phone = input('Enter phone=> ')
                if phone:
                    record.add_phone(phone)
                    self.phone_book.add_record(record)
                    print(f'\033[92mYou added a phone number {phone} to the contact:\n{str(record)}\033[0m')
                    count_phone += 1
                else:
                    return
                    # return '\033[92mThe phone number added successfully\033[0m'  # Сообщение о успешном добавлении
            except ValueError as e:
                print(e)

    
  # добавление даты рождения
    @input_error   
    def input_year(self, str_year='2000'):
        while True:
            # year = input("Введите год (по умолчанию 2000): {}".format(str_year))
            year = input('Enter the year (YYYY)=> {}'.format(str_year)) or '{}'.format(str_year)
            # year = input('Enter the year (YYYY)=> ') or str_year
            if year.isdigit() and 1900 <= int(year) <= 2100:
                return year
            else:
                str_year = ''
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
        print(f'Enter your birthday year or press ENTER to skip.')
        str_year = input('Enter address=> ')
        if str_year:
            year = self.input_year(str_year)
            month = self.input_month()
            day = self.input_day()
            birth = f'{year}.{month}.{day}'
            try:
                record.add_birthday(birth)
                self.phone_book.add_record(record)
                # return f'You added the date of birthday {birth} to the contact:\n{str(record)}'
                print(f'\033[92mYou added a phone number {birth} to the contact :\n{str(record)}\033[0m')
            except ValueError as e:
                print(e)
                print('Please enter a valid date in format YYYY.MM.DD')
                return self.add_birthday(record)  # Повторный вызов функции при ошибке ввода
        else:
            return

    @input_error
    def add_email(self, record: Record):
        while True:
            try:
                print(f'Enter your email or press ENTER to skip.')
                email = input('Enter email=> ')
                if email:
                    record.add_email(email)
                    self.phone_book.add_record(record)
                    print(f'\033[92mYou added a phone number {email} to the contact :\n{str(record)}\033[0m')
                    return
                    # return '\033[92mThe email added successfully\033[0m'  # Сообщение о успешном добавлении
                else:
                    return

            except ValueError as e:
                print(e)

    @input_error
    def add_address(self, record: Record):
        print(f'Enter your address or press ENTER to skip.')
        address = input('Enter address=> ')
        if address:
            record.add_address(address)
            self.phone_book.add_record(record)
            print(f'\033[92mYou added a phone number {address} to the contact :\n{str(record)}\033[0m')
            return
            # return '\033[92mThe address added successfully\033[0m'
        else:
            return

    # "меню" для добавления
    @input_error
    def add(self):
        pass
        # print('='*100)
        # print('Please enter the number\nYou can add:\n1.CONTACT\n2.PHONE\n3.BIRTHDAY')
        # res = input('Enter your text=>  ').lower()
        # if res in ('1', 'contact'):
        #     result = self.add_contact()
        # else:
        # name = input('Enter the name of an existing contact=> ')
        # record: Record = self.phone_book.find(name)
            # if res in ('2', 'phone'):
        # result = self.add_phone(record)
        # if res in ('3', 'birthday'):
        #     result = self.add_birthday(record)
        # return result


    @input_error
    def add_phone_menu(self):
        print('=' * 100)
        name = input('Enter the name of an existing contact=> ')
        record: Record = self.phone_book.find(name)
        result = self.add_phone(record)
        return result

    @input_error
    def add_birthday_menu(self):
        print('=' * 100)
        name = input('Enter the name of an existing contact=> ')
        record: Record = self.phone_book.find(name)
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
    def change_email(self):
        # self.add_email(record)
        # return f'You changed the contact:\n{str(record)}'
        while True:
            print('=' * 100)
            name = input('Enter name=> ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                result = self.add_email(record)
                return result
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')

    @input_error
    def change_address(self) :
        # self.add_address(record)
        # return f'You changed the contact:\n{str(record)}'
        while True:
            print('=' * 100)
            name = input('Enter name=> ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                result = self.add_address(record)
                return result
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')

    @input_error
    def change_name(self):
        print('=' * 100)
        name = input('Enter old name=> ')
        record: Record = self.phone_book.find(name)
        new_name = input('Enter new name=> ')
        if new_name:
            old_name = record.name.value
            self.phone_book.data[new_name] = self.phone_book.data.pop(old_name)
            record.name.value = new_name
            return f'Name changed successfully from {old_name} to {new_name}'
        else:
            return 'Name change cancelled'

    @input_error
    def charge_phone_mune(self):
        while True:
            print('=' * 100)
            name = input('Enter name=> ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                result = self.change_phone(record)
                return result
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')

    @input_error
    def charge_birthday_mune(self):
        while True:
            print('=' * 100)
            name = input('Enter name=> ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                result = self.change_birth(record)
                return result
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')
    # delete menu
    # @input_error
    # def change(self):
    #     print('='*100)
    #     print('Please enter the number\nYou can change:\n1.PHONE NUMBER\n2.DATE OF BIRTHDAY')
    #     res = input('Enter your text=>  ').lower()
    #     print('You can change the information in an existing contact')
    #     name = input('Enter name=> ')
    #     record: Record = self.phone_book.find(name)
    #     if res in ('1', 'phone', 'phone number'):
    #         result = self.change_phone(record)
    #         print('Do you want change the date of birthday?Please enter the number:\n1.YES\n2.NO')
    #         res_1 = input('Enter your text=>  ').lower()
    #         if res_1 in ('1', 'yes'):
    #             result = self.change_birth(record)
    #     if res in ('2', 'date', 'birth', 'date of birthday'):
    #         result = self.change_birth(record)
    #         print('Do you want change the phone number?Please enter the number:\n1.YES\n2.NO')
    #         res_1 = input('Enter your text=>  ').lower()
    #         if res_1 in ('1', 'yes'):
    #             result = self.change_phone(record)
    #     return result
    
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

    @input_error
    def delete_email(self, record: Record) :
        record.email = None
        self.phone_book.add_record(record)
        return 'Email removed'

    def delete_address(self, record: Record) :
        record.address = None
        self.phone_book.add_record(record)
        return 'Address removed'

    # удаление контакта
    @input_error       
    def delete_contact(self):
        name = input('Enter name=> ')
        result = self.phone_book.delete(name)
        return result
    
    # "меню" для удаления
    @input_error
    def delete_contact_menu(self):
        result = self.delete_contact()
        return result

    @input_error
    def delete_phone_menu(self):
        # name = input('Enter the name of an existing contact => ')
        # record: Record = self.phone_book.find(name)
        # self.delete_phone(record)
        # return str(record)
        while True:
            print('=' * 100)
            name = input('Enter the name of an existing contact => ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                self.delete_phone(record)
                return str(record)
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')

    @input_error
    def delete_birthday_menu(self):
        # name = input('Enter the name of an existing contact => ')
        # record: Record = self.phone_book.find(name)
        # self.delete_birth(record)
        # self.phone_book.add_record(record)
        # return str(record)
        while True:
            print('=' * 100)
            name = input('Enter the name of an existing contact => ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                self.delete_birth(record)
                self.phone_book.add_record(record)
                return str(record)
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')
    @input_error
    def delete_email_menu(self) :
        # name = input('Enter the name of an existing contact => ')
        # record: Record = self.phone_book.find(name)
        # self.delete_email(record)
        # self.phone_book.add_record(record)
        # return str(record)
        while True:
            print('=' * 100)
            name = input('Enter the name of an existing contact => ')
            record: Record = self.phone_book.find(name)
            if record:
                print(f'{str(record)}')
                self.delete_email(record)
                self.phone_book.add_record(record)
                return str(record)
            else:
                if len(name) == 0:
                    return
                else:
                    print(f'Contact {name} not found')
    @input_error
    def delete_address_menu(self) :
        # name = input('Enter the name of an existing contact => ')
        # record: Record = self.phone_book.find(name)
        # self.delete_address(record)
        # self.phone_book.add_record(record)
        # return str(record)

        while True :
            print('=' * 100)
            name = input('Enter the name of an existing contact => ')
            record: Record = self.phone_book.find(name)
            if record :
                print(f'{str(record)}')
                self.delete_address(record)
                self.phone_book.add_record(record)
                return str(record)
            else :
                if len(name) == 0 :
                    return
                else :
                    print(f'Contact {name} not found')

    # @input_error
    # def delete(self):
    #     print('='*100)
    #     print('Please enter the number\nYou can delete:\n1.CONTACT\n2.INFO IN AN EXISTING CONTACT')
    #     res = input('Enter your text=>  ').lower()
    #     if res in ('1', 'contact'):
    #         result = self.delete_contact()
    #     if res in ('2', 'info', 'info in an existing contact', 'existing contact'):
    #         name = input('Enter the name of an existing contact => ')
    #         record: Record = self.phone_book.find(name)
    #         print('Please enter the number\nYou can delete:\n1.PHONE NUMBER\n2.DATE OF BIRTH')
    #         res_1 = input('Enter your text=>  ').lower()
    #         if res_1 in ('1', 'phone', 'phone number'):
    #             self.delete_phone(record)
    #         if res_1 in ('2', 'birth', 'date', 'date of birth'):
    #             self.delete_birth(record)
    #             self.phone_book.add_record(record)
    #         return str(record)
    #     return result

# поиск по имени и по совпадениям
    @input_error
    def search(self):
        while True:
            print('='*100)
            print('Enter at least 3 letters or numbers to search or press ENTER to exit')

            res_1 = input('Enter your text=>  ').lower()
            if res_1:
                print(self.phone_book.search(res_1))
            else:
                break

            # print('You can search the contact by:\n1.NAME\n2.COINCIDENCE\n3.RETURN TO MAIN MENU')
            # res = input('Enter your text=>  ').lower()
            # if res in ('3', 'main', 'menu'):
            #     return
            # if res in ('1', 'name'):
            #     name = input('Enter name=> ')
            #     contact = self.phone_book.find(name)
            #     if contact is None:
            #         print('\033[91mThe contact does not exist\033[0m')
            #         continue  # Вернуться к началу цикла
            #     print(contact)
            #     return contact
            # if res in ('2'):
            #     res_1 = input('Enter your text=>  ').lower()
            #     print(self.phone_book.search(res_1))
            #     # return self.phone_book.search(res_1)
            # else:
            #     print("The answer doesn't exist. Please enter again")

    # работа через интератор не сделана правильно
    @input_error
    def show_all(self):
        print('='*100)
        print('Enter how many records to display?')
        item_number = input('Enter number=> ')
        if self.phone_book:
            if item_number.isdigit():
                # Введено число
                item_number = int(item_number)
                phones = 'Contacts:\n'
                iteration_count = 0

                for name, record in self.phone_book.data.items():
                    phones += f'{str(record)}\n'
                    iteration_count += 1

                    if iteration_count % item_number == 0:
                        print(phones)
                        phones = 'Contacts:\n'

                if phones != 'Contacts:\n':
                    print(phones)

            elif item_number.isalpha():
                # Введены буквы
                print(f'You entered letters: {item_number}')
            else:
                phones = f'Contacts:\n'
                for name, record in self.phone_book.data.items():
                    phones += f'{str(record)}\n'
                print(phones)
        else:
            print('No contacts')

        # res = input('Enter your text=>  ').lower()
        # if res == '1' or res == 'yes':
        #     if self.phone_book:
        #         phones = f'Contacts:\n'
        #         for name, record in self.phone_book.data.items():
        #             phones += f'{str(record)}\n'
        #         print(phones)
        #
        #         return
        #     else:
        #         return 'No contacts'
        # print('How many contacts to display?')
        # res_1 = input('Enter your text=>  ')
        # if res_1.isdigit():
        # return self.phone_book.iterator(res_1)
        # Выводим по три записи


        # выход из програмы и сохранение файла!
    def exit(self):
        self.phone_book.write_to_file()
        return

# эта часть отвечает за команды телефонной книги, нет адреса и email  


# def main():
#     assistent_bot = AssistantBot()
#     print('Hello!')
#     while True:
#         print('=' * 100)
#         print('How can I help you?\nPlease enter the number:\n1.ADD\n2.CHANGE\n3.DELETE\n4.SEARCH\n5.SHOW ALL\n6.EXIT')
#         command = input('Enter your text=>  ').lower()
#         if command in ('1', 'add'):
#             result = assistent_bot.add()
#         # elif command in ('2', 'change'):
#         #     result = assistent_bot.change()
#         # elif command in ('3', 'delete'):
#         #     result = assistent_bot.delete()
#         elif command in ('4', 'search'):
#             result = assistent_bot.search()
#         elif command in ('5', 'show all', 'show'):
#             result = assistent_bot.show_all()
#         elif command in ('6', 'exit'):
#             assistent_bot.exit()
#             print('Good bye!')
#             break
#         else:
#             result = 'Command not found, try again'
#         print(result)


if __name__ == "__main__":
    pass
    # main()
