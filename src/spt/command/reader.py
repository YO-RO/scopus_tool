import abc
import os
import sys

import pandas as pd


class IReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def perform_read(self) -> pd.DataFrame:
        raise NotImplementedError()


class StdinCsvReader(IReader):
    def perform_read(self) -> pd.DataFrame:
        df = pd.read_csv(sys.stdin)
        return df


class FileCsvReader(IReader):
    def __init__(self, input_file_path: str) -> None:
        self.input_file_path = input_file_path

    def perform_read(self) -> pd.DataFrame:
        if not os.path.isfile(self.input_file_path):
            sys.stderr.write(f"{self.input_file_path}というファイルは存在しません。")
            exit(1)
        return pd.read_csv(self.input_file_path)
