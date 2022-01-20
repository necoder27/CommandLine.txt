import glob
import os
from tkinter import Tk, filedialog


def tk_folder_chooser():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    return filedialog.askdirectory()


def tk_file_chooser():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    return filedialog.askopenfilename()


def remove_file():
    file_to_delete = tk_file_chooser()
    os.remove(file_to_delete)


class FileManager:
    not_readable = 'error: file could not be opened'

    def __init__(self):
        self.folder_path = ''
        self.file_name = ''
        self.file_text: list = []
        self.files_in_folder: list = []

    def get_files_from_folder(self):
        return [os.path.normpath(file) for file in glob.glob(f'{self.folder_path}/*.txt')]

    def save_to_files_in_folder(self):
        self.folder_path = tk_folder_chooser()
        if self.folder_path != '':
            self.files_in_folder = self.get_files_from_folder()
            return True
        return False

    def read_text_from_file(self):
        with open(self.file_name, 'r') as newFile:
            try:
                return newFile.readlines()
            except:
                return self.not_readable

    def choose_file(self):
        self.file_name = tk_file_chooser()
        if self.file_name != '':
            self.folder_path = os.path.dirname(self.file_name)

    def save_to_file_text(self):
        text = self.read_text_from_file()
        if self.file_name != '' and text != self.not_readable:
            self.file_text = text
            return self.file_text
        elif text == self.not_readable:
            return text

    def write_to_file(self, text):
        with open(self.file_name, 'w') as newFile:
            newFile.write(text)


if __name__ == '__main__':
    fm = FileManager()
    # fm.choose_file()
    # print(fm.file_name)
    # fm.save_to_file_text()

# return os.listdir()
