import pickle


class Note:
    def __init__(self, content, tags=None):
        if tags is None:
            tags = []
        self.content = content
        self.tags = tags


class NotesManager:
    def __init__(self):
        self.notes = []
        self.file = 'Save_Notes.bin'
        self.read_from_file()

    def add_note(self, content, tags=None):
        if tags is None:
            tags = []
        note = Note(content, tags)
        self.notes.append(note)

    def write_to_file(self):
        with open(self.file, 'wb') as file:
            pickle.dump(self.notes, file)

    def read_from_file(self):
        try:
            with open(self.file, 'rb') as file:
                self.notes = pickle.load(file)
            return self.notes
        except FileNotFoundError:
            pass

    def exit(self):
        self.write_to_file()
        return True

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def display_all_notes(self):
        if not self.notes:
            print('List empty')
        for i, note in enumerate(self.notes, 1):
            print(f"{i}. Content:{note.content}, Tags:{note.tags}")

    def edit_note_content(self, tag, new_content):
        for note in self.notes:
            if tag not in note.tags:
                print("Invalid note index.")
            if tag in note.tags:
                note.content = new_content
                print("Note update successfully.")

    def search_and_sort_notes(self, keyword):
        found_notes = [note for note in self.notes if keyword in note.tags]
        sorted_notes = sorted(found_notes, key=lambda x: x.tags)
        return sorted_notes

    def delete_note_by_index(self, index):
        initial_len = len(self.notes)
        self.notes = [note for note in self.notes if index not in note.tags]
        if len(self.notes) == initial_len:
            print(f"No note found with tag '{index}'.")
        else:
            print(f"Note with tag '{index}' deleted successfully.")

    def note_add_menu(self):
        content = input("Enter your text for the note: ")
        tags = input("Enter tags separated by commas (or press Enter if no tags): ").split(',')
        self.add_note(content, tags)
        self.write_to_file()

    def note_charge_menu(self):
        index = int(input("Enter index of the note to edit: "))
        new_content = input("Enter new text for the note: ")
        self.edit_note_content(index, new_content)
        self.write_to_file()

    def note_delete_menu(self):
        index = int(input("Enter index of the note to delete: "))
        self.delete_note_by_index(index)
        self.write_to_file()

    def note_search_menu(self):
        tag_to_search = input("Enter tag for search and sort: ")
        sorted_notes = self.search_and_sort_notes(tag_to_search)
        if sorted_notes:
            print(f"Found and Sorted Notes with Tag '{tag_to_search}':")
            for note in sorted_notes:
                print(f"Content: {note.content}, Tags: {note.tags}")
        else:
            print('Nothing to sort!')

    def note_show_menu(self):
        self.display_all_notes()

def interact_with_user():
    notes_manager = NotesManager()

    while True:
        print("\n1. Add Note")
        print("2. Show all Note")
        print("3. Search and Sort Notes by Tag")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Choice your option (1 - 6): ")

        if choice == "1":
            content = input("Enter your text for the note: ")
            tags = input("Enter tags separated by commas (or press Enter if no tags): ").split(',')
            notes_manager.add_note(content, tags)
        elif choice == "2":
            notes_manager.display_all_notes()
        elif choice == "3":
            tag_to_search = input("Enter tag for search and sort: ")
            sorted_notes = notes_manager.search_and_sort_notes(tag_to_search)
            if sorted_notes:
                print(f"Found and Sorted Notes with Tag '{tag_to_search}':")
                for note in sorted_notes:
                    print(f"Content: {note.content}, Tags: {note.tags}")
            else:
                print('Nothing to sort!')
        elif choice == "4":
            index = int(input("Enter index of the note to edit: "))
            new_content = input("Enter new text for the note: ")
            notes_manager.edit_note_content(index, new_content)
        elif choice == "5":
            index = int(input("Enter index of the note to delete: "))
            notes_manager.delete_note_by_index(index)
        elif choice == "6":
            if notes_manager.exit():
                print('Notes saved and exiting successfully! Good Luck!')
            else:
                print('exit failed.')
            break
        else:
            print("Wrong choice!!! Try again!.")


if __name__ == "__main__":
    interact_with_user()
