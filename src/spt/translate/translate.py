import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv

from ..command import Command, FileCsvReader, FileCsvWriter, IReader, IWriter, StdinCsvReader, StdoutCsvWriter
from ..exceptions import AuthorizationException
from .translator import DeeplTranslator, ITranslator

load_dotenv()


class TranslationCommand(Command):
    def __init__(
        self,
        reader: IReader,
        writer: IWriter,
        translator: ITranslator,
        column_name: str,
        max_lines: int | None,
    ) -> None:
        assert max_lines is None or max_lines >= 1, f"max_linesは1以上を指定する必要がある。指定された値: {max_lines}"

        super().__init__(reader, writer)
        self.translator = translator
        self.column_name = column_name
        self.max_lines = max_lines

    def _process_data_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        df.fillna("")

        # 先頭から`max_lines`件の論文以外を消す
        if self.max_lines is not None and len(df) > self.max_lines:
            df.drop(df.index[[i for i in range(self.max_lines, len(df))]], inplace=True)

        try:
            source_text_list = df[self.column_name].tolist()
            translated_text_list = self.translator.translate_text(source_text_list)
        except KeyError as e:
            e.strerror = f"{self.column_name}という列は存在しません"
            raise

        insert_loc = df.columns.get_loc(self.column_name) + 1
        df.insert(insert_loc, f"{self.column_name} (和訳)", translated_text_list)

        return df


def get_args():
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    default_input_file_path = os.path.join(downloads_dir, "scopus.csv")
    default_output_file_path = os.path.join(downloads_dir, "scopus_translation.csv")
    default_column_name = "抄録"

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file-path", "-i", help="翻訳する列を含む論文一覧のCSVファイルパス。")
    parser.add_argument("--output-file-path", "-o", help="出力するCSVファイルパス。")
    parser.add_argument("--column", "-c", help="翻訳する列。指定がなければ抄録の列を翻訳する。")
    parser.add_argument("--max-lines", "-m", type=int, help="翻訳する論文の最大数")
    args = parser.parse_args()

    input_file_path = default_input_file_path if args.input_file_path is None else args.input_file_path
    output_file_path = default_output_file_path if args.output_file_path is None else args.output_file_path
    column_name = default_column_name if args.column is None else args.column
    max_lines: int | None = args.max_lines if args.max_lines >= 1 else None

    return {
        "input_file_path": input_file_path,
        "output_file_path": output_file_path,
        "column_name": column_name,
        "max_lines": max_lines,
    }


def main():
    args = get_args()
    input_file_path = args["input_file_path"]
    output_file_path = args["output_file_path"]
    column_name = args["column_name"]
    max_lines = args["max_lines"]

    reader = FileCsvReader(input_file_path) if sys.stdin.isatty() else StdinCsvReader()
    writer = FileCsvWriter(output_file_path) if sys.stdout.isatty() else StdoutCsvWriter()
    translator = DeeplTranslator()
    translation_command = TranslationCommand(reader, writer, translator, column_name, max_lines)

    try:
        # ファイルに出力されたら、出力されたファイルのパスが戻り値としてくる。stdoutとかならNone。
        final_output_file_path: str | None = translation_command.execute()
    except FileNotFoundError as e:
        sys.stderr.write(e.strerror)
        exit(1)
    except KeyError as e:
        sys.stderr.write(e.strerror)
        exit(1)
    except ConnectionError as e:
        sys.stderr.write(e.strerror)
        exit(1)
    except AuthorizationException as e:
        sys.stderr.write(e.strerror)
        exit(1)

    if final_output_file_path is not None:
        sys.stdout.write(f"{final_output_file_path}に保存しました。")


if __name__ == "__main__":
    main()
