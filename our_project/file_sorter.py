from pathlib import Path
import shutil
from tqdm import tqdm
import time
import re

# normalize
# Створюємо змінну з українською абеткою
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
# Створюємо змінну (список) для транслейту
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "i", "ji", "g")
# Створюємо порожній словник для транслейту
CONVERTS = dict()

# Заповнюємо словник
for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    CONVERTS[ord(cyrillic)] = latin
    CONVERTS[ord(cyrillic.upper())] = latin.upper()


# Створюємо функцію для чищення від усіх зайвих символів і перетворюємо та заміняємо на транслейт
def normalize(name: str) -> str:
    translate_name = re.sub(r'\W', '_', name.translate(CONVERTS))
    return translate_name

# file_parser
# Створюємо порожні списки для зображень


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

# Створюємо порожні списки для відео
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

# Створюємо порожні списки для музики
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

# Створюємо порожні списки для документів
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []

# Створюємо порожній список для архівів
ARCHIVES = []

# Створюємо порожній список для решти
MY_OTHER = []

# Створюємо словник з розширеннями та відповідними ним списками
REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAW': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

# Створюємо порожній список для шляху до папок
FOLDERS = []
# Створюємо порожню множину для розширень
EXTENSIONS = set()
# Створюємо порожню множину для невідомих
UNKNOWN = set()


# Відокремлюємо суфікс і перетворюємо на великі літери
def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()


# Проходимося по папці із сортувальними файлами
def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:  # перевіряємо з розширень
                register_extension = REGISTER_EXTENSION[extension]
                register_extension.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)


# Проводимо очищення і створюємо директорію, а не директорію з розширенням для папок і файлів.
def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    name_normalize = normalize(file_name.stem) + file_name.suffix
    file_name.replace(target_folder / name_normalize)


# Проводимо очищення та створюємо директорію, розпаковуємо архів для архівів.
def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


# Основний модуль логіки
def main(folder: Path):
    scan(folder)
    # Проходимо по всіх знайдених списках для images
    # count_star  =0
    # count_stop = len(JPEG_IMAGES)
    # items = list(range(count_stop))
    # for file in JPEG_IMAGES:
    #     handle_media(file, folder / 'images' / 'JPEG')

    count_star = 0
    for file in tqdm(JPEG_IMAGES, desc = '\033[38;2;10;235;190mОбробка изображений JPEG',
                     unit = " файл\033[0m", ncols = 100):
        handle_media(file, folder / 'images' / 'JPEG')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(JPG_IMAGES, desc = '\033[38;2;10;235;190mОбробка зображення JPG',
                     unit = " файл\033[0m", ncols = 100):
    # for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(PNG_IMAGES, desc = '\033[38;2;10;235;190mОбробка зображення PNG',
                     unit = " файл\033[0m", ncols = 100):
    # for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(SVG_IMAGES, desc = '\033[38;2;10;235;190mОбробка зображення SVG',
                     unit = " файл\033[0m", ncols = 100):
    # for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
        count_star += 1
        time.sleep(0.05)

    # Проходимо по всіх знайдених списках для відео
    count_star = 0
    for file in tqdm(AVI_VIDEO, desc = '\033[38;2;10;235;190mОбробка відео AVI',
                     unit = " файл\033[0m", ncols = 100):
    # for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI_VIDEO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(MP4_VIDEO, desc = '\033[38;2;10;235;190mОбробка відео MP4',
                     unit = " файл\033[0m", ncols = 100):
    # for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4_VIDEO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(MOV_VIDEO, desc = '\033[38;2;10;235;190mОбробка відео MOV',
                     unit = " файл\033[0m", ncols = 100):
    # for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV_VIDEO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(MKV_VIDEO, desc = '\033[38;2;10;235;190mОбробка відео MKV',
                     unit = " файл\033[0m", ncols = 100):
    # for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV_VIDEO')
        count_star += 1
        time.sleep(0.05)

    # Проходимо за всіма знайденими списками для audio
    count_star = 0
    for file in tqdm(MP3_AUDIO, desc = '\033[38;2;10;235;190mОбробка аудіо MP3',
                     unit = " файл\033[0m", ncols = 100):
    # for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3_AUDIO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(OGG_AUDIO, desc = '\033[38;2;10;235;190mОбробка аудіо OGG',
                     unit = " файл\033[0m", ncols = 100):
    # for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG_AUDIO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(WAV_AUDIO, desc = '\033[38;2;10;235;190mОбробка аудіо WAV',
                     unit = " файл\033[0m", ncols = 100):
    # for file in WAV_AUDIO :
        handle_media(file, folder / 'audio' / 'WAV_AUDIO')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(AMR_AUDIO, desc = '\033[38;2;10;235;190mОбробка аудіо AMR',
                     unit = " файл\033[0m", ncols = 100):
    # for file in AMR_AUDIO :
        handle_media(file, folder / 'audio' / 'AMR_AUDIO')
        count_star += 1
        time.sleep(0.05)

    # Проходимо по всіх знайдених списках для documents
    count_star = 0
    for file in tqdm(DOC_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів DOC',
                     unit = " файл\033[0m", ncols = 100):
    # for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(DOCX_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів DOCX',
                     unit = " файл\033[0m", ncols = 100):
    # for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(TXT_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів TXT',
                     unit = " файл\033[0m", ncols = 100):
    # for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(PDF_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів PDF',
                     unit = " файл\033[0m", ncols = 100):
    # for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(XLSX_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів XLSX',
                     unit = " файл\033[0m", ncols = 100):
    # for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for file in tqdm(PPTX_DOCUMENTS, desc = '\033[38;2;10;235;190mОбробка документів PPTX',
                     unit = " файл\033[0m", ncols = 100):
    # for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX_DOCUMENTS')
        count_star += 1
        time.sleep(0.05)


    # Проходимо за всіма знайденими списками для MY_OTHER
    count_star = 0
    for file in tqdm(MY_OTHER, desc = '\033[38;2;10;235;190mОбробка інших файлів',
                     unit = " файл\033[0m", ncols = 100):
    # for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')
        count_star += 1
        time.sleep(0.05)

    # Проходимо по всіх знайдених списках для ARCHIVES
    count_star = 0
    for file in tqdm(ARCHIVES, desc = '\033[38;2;10;235;190mОбробка архівів',
                     unit = " файл\033[0m", ncols = 100):
    # for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')
        count_star += 1
        time.sleep(0.05)

    count_star = 0
    for folder in tqdm(FOLDERS[::-1], desc = '\033[38;2;10;235;190mВидалення пустих папок',
                     unit = " файл\033[0m", ncols = 100):
        count_star += 1
        time.sleep(0.05)
    # for folder in FOLDERS[::-1]:


        # Видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


def sorteds_menu():
    print(f'\033[38;2;10;235;190mCopy the files to be sorted into a folder in this project and press Enter to sort '
          f'them.\033[0m')
    user_input = input('\033[38;2;10;235;190mPress Enter to sort them.\033[0m')

    folder_process = Path('trash_folder')
    main(folder_process.resolve())

if __name__ == "__main__":
    # items = list(range(100))
    # for item in tqdm(items, desc='\033[38;2;10;235;190mПрогресс', unit='элемент\033[0m', ncols=100):
    #     # Симулируем задержку для наглядности
    #     time.sleep(0.05)
    # folder_process = Path(sys.argv[1])
    folder_process = Path('trash_folder')
    main(folder_process.resolve())
