import os
from kivy import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from Backend.text_file import FileManager, remove_file
from kivy.base import EventLoop

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RootGrid(Widget):
    text_input = ObjectProperty(None)
    commands = ObjectProperty(None)
    cmd_text = StringProperty()
    file_text = StringProperty()
    label_text = ''
    duplicate_file_check = ''
    text_color = ListProperty([0, 1, 0, 1])
    commands_color = ListProperty([1, 1, 1, 1])
    colors_dictionary = {
        'r': [1, 0, 0, 1],
        'g': [0, 1, 0, 1],
        'b': [0, 0, 1, 1],
        'w': [1, 1, 1, 1]
    }
    fm = FileManager()
    add_to_cmd_label_wo_signs = [
        'unrecognized command',
        'similar:\ncfile [file_name].[file_extension]',
        'invalid color',
        'incomplete command',
        fm.not_readable
    ]

    def detect_enter(self):
        text_input_text = self.commands.text
        self.add_to_cmd_label(text_input_text)
        if text_input_text != '':
            self.command(text_input_text)
        self.cmd_text = self.label_text
        self.commands.text = ''

    def add_to_cmd_label(self, text_input_text):
        if text_input_text in self.add_to_cmd_label_wo_signs:
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
            self.command_cfile(com)
        elif com == 'y':
            if self.duplicate_file_check != '':
                self.create_file(self.duplicate_file_check)
                self.duplicate_file_check = ''
        elif com == 'n':
            pass
        elif com == 'rfile':
            self.rfile()
        elif 'textcolor' in com or 'commandscolor' in com:
            self.command_textcolor_commandscolor(com)
        else:
            self.add_to_cmd_label(self.add_to_cmd_label_wo_signs[0])

    def command_cfile(self, com):
        words = com.split()
        if words[0] == 'cfile' and len(words) == 2:
            self.cfile(com)
        else:
            self.add_to_cmd_label(self.add_to_cmd_label_wo_signs[1])

    def command_textcolor_commandscolor(self, com):
        words = com.split()
        if len(words) == 2:
            if words[1] in self.colors_dictionary:
                if words[0] == 'textcolor':
                    self.change_text_color(words[1])
                elif words[0] == 'commandscolor':
                    self.change_commands_color(words[1])
            elif words[1] == '/?':
                self.list_all_colors()
            else:
                self.add_to_cmd_label(self.add_to_cmd_label_wo_signs[2])
        else:
            self.add_to_cmd_label(self.add_to_cmd_label_wo_signs[3])

    def print_commands(self):
        help_comms = 'Commands:\n/? -- help\nopenf -- open file\nsfile -- save file\n' \
                     'cfile [file_name].[file_extension] -- save a newly created file\n' \
                     'rfile -- delete a file' \
                     'textcolor /? -- all choosable colors\n' \
                     'textcolor [sum_color] -- change text color of file text'
        self.add_to_cmd_label(help_comms)

    def openf(self):
        self.fm.choose_file()
        file_text = self.fm.save_to_file_text()
        if file_text == self.fm.not_readable:
            self.add_to_cmd_label(file_text)
        else:
            input_text = ''.join(file_text)
            self.file_text = input_text

    def sfile(self):
        self.fm.write_to_file(self.text_input.text)

    def cfile(self, com):
        if self.fm.save_to_files_in_folder():
            file_name = os.path.normpath(self.fm.folder_path + '/' + com.replace('cfile ', ''))
            self.duplicate_file_check = file_name
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

    def change_text_color(self, color):
        self.text_color = self.colors_dictionary[color]

    def change_commands_color(self, color):
        self.commands_color = self.colors_dictionary[color]

    def list_all_colors(self):
        colors = 'Initials of available colors:\n'
        colors = colors + '\n'.join(self.colors_dictionary)
        if colors not in self.add_to_cmd_label_wo_signs:
            self.add_to_cmd_label_wo_signs.append(colors)
        self.add_to_cmd_label(colors)


class CommandLineTxt(App):
    def build(self):
        self.icon = 'Icon/qtecat.png'
        return RootGrid()


if __name__ == '__main__':
    CommandLineTxt().run()

# EventLoop.window.title = self.fm.folder_path
# todo: adding colors to colors_dictionary
# todo: case insensitive
