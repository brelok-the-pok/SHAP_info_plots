import os
import shutil


class CreatedPlotsSaver:
    @staticmethod
    def save_plots(from_path: str, to_path: str) -> None:
        files = os.listdir(from_path)
        for file in files:
            if ".png" in file:
                shutil.copy2(f"{from_path}\\{file}", f"{to_path}\\{file}")
