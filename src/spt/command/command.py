import abc

import pandas as pd

from .reader import IReader
from .writer import IWriter


class Command(metaclass=abc.ABCMeta):
    """全てのコマンドを抽象化したクラス。全てのコマンドはCSVの読み込み→加工→書き込みを実行する。読み込みと書き込みは同じ処理をする。"""

    def __init__(self, reader: IReader, writer: IWriter) -> None:
        self._reader: IReader = reader
        self._writer: IWriter = writer

    def _read(self) -> pd.DataFrame:
        return self._reader.perform_read()

    def _write(self, df: pd.DataFrame) -> None:
        self._writer.perform_write(df)

    @abc.abstractmethod
    def _process_data_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """個々のコマンドで行われるDataFrameの加工はここに書く"""
        raise NotImplementedError()

    def execute(self) -> None:
        """コマンドを実行するためのメソッド"""
        df = self._read()
        df = self._process_data_frame(df)
        self._write(df)
