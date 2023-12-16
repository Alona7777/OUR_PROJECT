from pathlib import Path
import shutil
import sys
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
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    # Проходимо по всіх знайдених списках для відео
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI_VIDEO')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4_VIDEO')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV_VIDEO')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV_VIDEO')

    # Проходимо за всіма знайденими списками для audio
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3_AUDIO')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG_AUDIO')
    for file in WAV_AUDIO :
        handle_media(file, folder / 'audio' / 'WAV_AUDIO')
    for file in AMR_AUDIO :
        handle_media(file, folder / 'audio' / 'AMR_AUDIO')

    # Проходимо по всіх знайдених списках для documents
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC_DOCUMENTS')
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX_DOCUMENTS')
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT_DOCUMENTS')
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF_DOCUMENTS')
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX_DOCUMENTS')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX_DOCUMENTS')

    # Проходимо за всіма знайденими списками для MY_OTHER
    for file in MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')

    # Проходимо по всіх знайдених списках для ARCHIVES
    for file in ARCHIVES:
        handle_archive(file, folder / 'ARCHIVES')

    for folder in FOLDERS[::-1]:
        # Видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())
