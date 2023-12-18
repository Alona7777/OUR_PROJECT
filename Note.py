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
            print(f"{i}. Content: {note.content}. Tags:{note.tags}")

    def edit_note_content(self, index, new_content):
        if 1 <= index <= len(self.notes):
            self.notes[index - 1].content = new_content
        else:
            print("Invalid note index.")

    def search_and_sort_notes(self, keyword):
        found_notes = [note for note in self.notes if keyword in note.tags]
        sorted_notes = sorted(found_notes, key=lambda x: x.tags)
        return sorted_notes

    def delete_note_by_index(self, index):
        if 1 <= index <= len(self.notes):
            del self.notes[index - 1]
        else:
            print("Invalid note index.")


def interact_with_user():
    notes_manager = NotesManager()

    while True:
        print("\n1. Add Note")
        print("2. Show all Note")
        print("3. Search and Sort Notes by Tag")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Exit")

        choice = input("Choose your option: ")

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
            break
        else:
            print("Wrong choice!!! Try again!.")


if __name__ == "__main__":
    interact_with_user()
