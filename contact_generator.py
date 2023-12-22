import random
import faker
import re
from contact_book import AssistantBot, Record, AddressBook
import faker
from faker import Faker

fake = Faker()

def generate_name():
    return normalize(fake.name())

fake = faker.Faker('uk_UA')

assistant_bot = AssistantBot()
AddressBook_bot = AddressBook()

# Создаем переменную с украинским алфавитом
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
# Создаем переменную (список) для транслейта
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "i", "ji", "g")
# Создаем пустой словарь для транслейта
CONVERTS = dict()

# Заполняем словарь
for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    CONVERTS[ord(cyrillic)] = latin
    CONVERTS[ord(cyrillic.upper())] = latin.upper()


# Создаем функцию для чистки от всех лишних символов и преобразовываем и заменя на транслейт
def normalize(name: str) -> str:
    translate_name = re.sub(r'\W', '_', name.translate(CONVERTS))
    return translate_name


def generate_phone_number():
    return f"0{random.randint(50, 99)}{random.randint(100, 999)}{random.randint(1000, 9999)}"


def generate_birthdate():
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}.{month:02d}.{day:02d}"


def generate_email(name):
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com"])
    return fake.email()


def generate_address():
    cities = ["Kyiv", "Lviv", "Odesa", "Kharkiv", "Dnipro"]
    streets = ["Main St", "First St", "Second St", "Third St", "Park Ave"]
    return f"{random.choice(streets)}, {random.randint(1, 100)}, {random.choice(cities)}"


def generate_contract_book(num_entries, phone_book):
    for _ in range(num_entries):
        name = generate_name()
        phones = generate_phone_number()
        birthday = generate_birthdate()
        email = generate_email(name)
        address = generate_address()

        record = Record(name)
        record.add_phone(phones)
        record.add_birthday(birthday)
        record.add_email(email)
        record.add_address(address)
        phone_book[name] = record  # Add the record directly to the phone_book


def contact_generator_menu():
    num_entries = 30
    assistant_bot = AssistantBot()
    generate_contract_book(num_entries, assistant_bot.phone_book)

    for name, record in assistant_bot.phone_book.items():
        print(f"Name: {name}")
        print(f"Phones: {record.phones}")
        print(f"Birthday: {record.birthday}")
        print(f"Email: {record.email}")
        print(f"Address: {record.address}")
        print()

    AddressBook_bot.write_to_file()
    AddressBook_bot.read_from_file()
    return


if __name__ == "__main__":
    num_entries = 20
    assistant_bot = AssistantBot()
    generate_contract_book(num_entries, assistant_bot.phone_book)

    for name, record in assistant_bot.phone_book.items():
        print(f"Name: {name}")
        print(f"Phones: {record.phones}")
        print(f"Birthday: {record.birthday}")
        print(f"Email: {record.email}")
        print(f"Address: {record.address}")
        print()

    assistant_bot.exit()
