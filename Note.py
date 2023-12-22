import pickle
from rich.console import Console
from rich.table import Table


class Note:
    def __init__(self, content, tags=None):
        if tags is None:
            tags = []
        self.content = content
        self.tags = tags


class NotesManager:
    def __init__(self):
        self.console = Console()
        self.notes = []
        self.file = 'Save_Notes.bin'
        self.read_from_file()
        
    def table_print_note(self):
        table = Table(title="Note Information", style="cyan", title_style="bold magenta", width = 100)
        table.add_column("Content", style="bold green", justify="center")
        table.add_column("Tags", style="bold blue", justify="center")
    
        table.add_row(
            str(self.notes.content),
            str(self.note.tags),
          )
        return table

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
        table = Table(title="Note Information", style="cyan", title_style="bold magenta", width = 100)
        table.add_column("Content", style="bold blue", justify="center")
        table.add_column("Tags", style="bold blue", justify="center")
        if not self.notes:
            print('\033[91mList empty.\033[0m')
        else:
            for i, note in enumerate(self.notes, 1):
                table.add_row(str(note.content), str(note.tags))
            self.console.print(table)

    def edit_note_content(self, tag, new_content):
        for note in self.notes:
            if tag not in note.tags:
                print('\033[91mInvalid note index.\033[0m')
            if tag in note.tags:
                note.content = new_content
                print(f'\033[92mNote update successfully.\033[0m')

    def search_and_sort_notes(self, keyword):
        found_notes = [note for note in self.notes if keyword in note.tags]
        sorted_notes = sorted(found_notes, key=lambda x: x.tags)
        return sorted_notes

    def delete_note_by_index(self, index):
        initial_len = len(self.notes)
        self.notes = [note for note in self.notes if index not in note.tags]
        if len(self.notes) == initial_len:
            print(f'\033[91mNo note found with tag "{index}".\033[0m')
        else:
            print(f'\033[92mNote with tag "{index}" deleted successfully.\033[0m')

    def note_add_menu(self):
        content = input('Enter your text for the note: ')
        tags = input('Enter tags separated by commas (or press Enter if no tags): ').split(',')
        self.add_note(content, tags)
        self.write_to_file()

    def note_charge_menu(self):
        index = int(input('Enter index of the note to edit: '))
        new_content = input('Enter new text for the note: ')
        self.edit_note_content(index, new_content)
        self.write_to_file()

    def note_delete_menu(self):
        index = int(input('Enter index of the note to delete: '))
        self.delete_note_by_index(index)
        self.write_to_file()

    def note_search_menu(self):
        table = Table(title="Note Information", style="cyan", title_style="bold magenta", width = 100)
        table.add_column("Content", style="bold blue", justify="center")
        table.add_column("Tags", style="bold blue", justify="center")
        tag_to_search = input('Enter tag for search and sort: ')
        sorted_notes = self.search_and_sort_notes(tag_to_search)
        if sorted_notes:
            print(f'\033[92mFound and Sorted Notes with Tag "{tag_to_search}":\033[0m')
            for note in sorted_notes:
                table.add_row(str(note.content), str(note.tags))
            self.console.print(table)
        else:
            print('\033[91mNothing to sort!\033[0m')

    def note_show_menu(self):
        self.display_all_notes()



if __name__ == "__main__":
    pass
