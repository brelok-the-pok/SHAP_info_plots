from typing import Optional
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QWidget


class QtHelper:
    def __init__(self):
        self.__cur_dir = str(Path.cwd())

    def get_path_to_file(self, parent: QWidget) -> Optional[str]:
        file_name = QFileDialog.getOpenFileName(parent, "Открыть файл", self.__cur_dir)

        return file_name[0] or None
