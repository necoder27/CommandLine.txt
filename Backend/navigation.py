import os
from pathlib import Path


class Navigation:
    path = os.environ['USERPROFILE']

    def cd_command(self, dir_name):
        dir_path = f'{self.path}\\{dir_name}'
        if Path(dir_path).is_dir():
            self.path = dir_path
            return dir_path
        else:
            return 'error: directory does not exist'

    def open(self, file_name):
        if file_name not in self.path:
            file_path = f'{self.path}\\{file_name}'
            if os.path.exists(file_path):
                self.path = file_path
                return file_path
            else:
                return 'error: file does not exist'

    def dir_command(self):
        return os.listdir(self.path)

    def folders_command(self):
        return next(os.walk(self.path))[1]

    def files_command(self):
        return next(os.walk(self.path))[2]
