import abc
import os
import sys

import pandas as pd


class IWriter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform_write(self, df: pd.DataFrame) -> None:
        raise NotImplementedError()


class StdoutCsvWriter(IWriter):
    def perform_write(self, df: pd.DataFrame) -> None:
        df.to_csv(sys.stdout, index=False)


class FileCsvWriter(IWriter):
    def __init__(self, output_file_path: str, overwrite=False) -> None:
        self.output_file_path = output_file_path
        self.overwrite = overwrite

    def perform_write(self, df: pd.DataFrame) -> None:
        if not self.overwrite and os.path.isfile(self.output_file_path):
            self.output_file_path = self._get_alt_file_path(self.output_file_path)
        df.to_csv(self.output_file_path, index=False)
        print(f"{self.output_file_path}に保存しました。")

    def _get_alt_file_path(self, file_path: str) -> str:
        # "./file.csv" -> "./file(1).csv"
        def alt_filename(index):
            root, ext = os.path.splitext(file_path)
            return root + f"({index})" + ext

        index = 1
        while os.path.isfile(alt_filename(index)):
            index += 1
        return alt_filename(index)
