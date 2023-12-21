import requests
from googletrans import Translator

"""For correct work translation, pls use this rules:
    pip install googletrans==4.0.0-rc1"""


def get_weather(api_key, city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        print(f"\033[38;2;10;235;190mThe weather in {city}: {temperature}°C, {description}\033[0m")
    else:
        print(f"\033[91mFailed to get weather. Code status: {response.status_code}\033[0m")


def get_joke():
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    joke_data = response.json()
    return joke_data['value']


def translate_to_ukrainian(text):
    translator = Translator()
    translation = translator.translate(text, dest='uk')
    return translation.text


def anecdotes_ua_menu():
    joke = get_joke()
    translated_joke = translate_to_ukrainian(joke)
    print(f'\033[38;2;10;235;190m{translated_joke}\033[0m')


def anecdotes_en_menu():
    joke = get_joke()
    print(f'\033[38;2;10;235;190m{joke}\033[0m')


def weather_menu():
    api_key = '43a8f3599db25559dcfc8b220a2adb8d'
    city = input("Please enter your city in English: ")
    get_weather(api_key, city)

#
# def main():
#     while True:
#         print('=' * 80)
#
#         print('Hello I am a funny personal bot.')
#         print('Pleas choice you happy number:)')
#         print('\n1. anecdote: "Українскою мовою:)')
#         print('2. anecdote: English language')
#         print('3. weather now')
#         print('4. exit')
#
#         command = input("Enter you choice: (1 - 4)==>>:")
#
#         if command == '1':
#             joke = get_joke()
#             translated_joke = translate_to_ukrainian(joke)
#             print(translated_joke)
#         elif command == '2':
#             joke = get_joke()
#             print(joke)
#         elif command == '3':
#             api_key = '43a8f3599db25559dcfc8b220a2adb8d'
#             city = input("Enter you city in english pleas: ")
#             get_weather(api_key, city)
#         elif command == '4':
#             break
#         else:
#             print("Wrong command!. Pleas try again.")


if __name__ == "__main__":
    pass
    # main()