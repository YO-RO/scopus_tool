import abc
import os
import sys

import pandas as pd


class IWriter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform_write(self, df: pd.DataFrame) -> str | None:
        """DataFrameを書き出すクラスのインターフェース

        Args:
            df (pd.DataFrame): 書き出すDataFrame

        Raises:
            NotImplementedError: 実装されていないときに発生

        Returns:
            str | None: ファイルに保存した場合はファイルパスを、そうでない場合はNoneを返す。保存したファイルパスを伝えるより良い方法を検討
        """
        raise NotImplementedError()


class StdoutCsvWriter(IWriter):
    def perform_write(self, df: pd.DataFrame) -> str | None:
        df.to_csv(sys.stdout, index=False)
        return None


class FileCsvWriter(IWriter):
    def __init__(self, output_file_path: str, overwrite=False) -> None:
        self.output_file_path = output_file_path
        self.overwrite = overwrite

    def perform_write(self, df: pd.DataFrame) -> str | None:
        if not self.overwrite and os.path.isfile(self.output_file_path):
            self.output_file_path = self._get_alt_file_path(self.output_file_path)
        df.to_csv(self.output_file_path, index=False)
        return self.output_file_path

    def _get_alt_file_path(self, file_path: str) -> str:
        # "./file.csv" -> "./file(1).csv"
        def alt_filename(index):
            root, ext = os.path.splitext(file_path)
            return root + f"({index})" + ext

        index = 1
        while os.path.isfile(alt_filename(index)):
            index += 1
        return alt_filename(index)
