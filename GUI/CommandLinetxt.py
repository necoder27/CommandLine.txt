import os
from kivy import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from Backend.text_file import FileManager, remove_file

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class Grid(Widget):
    text_input = ObjectProperty(None)
    commands = ObjectProperty(None)
    cmd_text = StringProperty()
    file_text = StringProperty()
    label_text = ''
    string_for_anything = ''
    fm = FileManager()

    def detect_enter(self):
        text_input_text = self.commands.text
        self.add_to_cmd_label(text_input_text)
        if text_input_text != '':
            self.command(text_input_text)
        self.cmd_text = self.label_text
        self.commands.text = ''

    def add_to_cmd_label(self, text_input_text):
        if text_input_text == 'unrecognized command':
            self.label_text = self.label_text + '\n' + text_input_text
        elif self.label_text != '':
            self.label_text = self.label_text + '\n>>> ' + text_input_text
        else:
            self.label_text = '>>> ' + text_input_text

    def command(self, com):
        com = com.strip()
        if com == '/?':
            self.print_commands()
        elif com == 'openf':
            self.openf()
        elif com == 'sfile':
            self.sfile()
        elif 'cfile' in com:
            words = com.split()
            if words[0] == 'cfile' and len(words) == 2:
                self.cfile(com)
            else:
                self.add_to_cmd_label('unrecognized command')
        elif com == 'y':
            if self.string_for_anything != '':
                self.create_file(self.string_for_anything)
                self.string_for_anything = ''
        elif com == 'n':
            pass
        elif com == 'rfile':
            self.rfile()
        else:
            self.add_to_cmd_label('unrecognized command')

    def print_commands(self):
        help_comms = 'Commands:\n/? -- help\nopenf -- open file\nsfile -- save file\n' \
                     'cfile [sum_file_name] -- save a newly created file\n' \
                     'rfile -- delete a file'
        self.add_to_cmd_label(help_comms)

    def openf(self):
        self.fm.choose_file()
        file_text = self.fm.save_to_file_text()
        input_text = ''.join(file_text)
        self.file_text = input_text

    def sfile(self):
        self.fm.write_to_file(self.text_input.text)

    def cfile(self, com):
        if self.fm.save_to_files_in_folder():
            file_name = os.path.normpath(self.fm.folder_path + '/' + com.replace('cfile ', '') + '.txt')
            self.string_for_anything = file_name
            if file_name not in self.fm.files_in_folder:
                self.create_file(file_name)
            else:
                self.label_text = self.label_text + '\nfile already exists. do you want to replace it? [y/n]'
        else:
            self.label_text = self.label_text + '\nerror: no folder chosen'

    def create_file(self, file_name):
        self.fm.file_name = file_name
        self.fm.write_to_file(self.text_input.text)
        self.fm.save_to_file_text()

    @staticmethod
    def rfile():
        remove_file()


class CommandLineTxt(App):
    def build(self):
        self.icon = 'Icon/qtecat.png'
        return Grid()


if __name__ == '__main__':
    CommandLineTxt().run()
