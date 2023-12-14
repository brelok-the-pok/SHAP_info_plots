from typing import Optional
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QWidget


class QtHelper:
    def __init__(self):
        self.__cur_dir = str(Path.cwd())

    def get_path_to_open_file(
        self, parent: QWidget, descriptor_name="Открыть файл"
    ) -> Optional[str]:
        file_name = QFileDialog.getOpenFileName(parent, descriptor_name, self.__cur_dir)

        return file_name[0] or None

    def get_path_to_save_file(
        self, parent: QWidget, descriptor_name="Сохранить файл"
    ) -> Optional[str]:
        file_name = QFileDialog.getSaveFileName(parent, descriptor_name, self.__cur_dir)

        return file_name[0] or None

    def get_existing_dir_path(
        self, parent: QWidget, descriptor_name="Выбрать дитекторию"
    ) -> Optional[str]:
        return QFileDialog.getExistingDirectory(parent, descriptor_name, self.__cur_dir)
