import argparse
import os
import sys

import deepl
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def analyze_args():
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
    max_lines: int | None = args.max_lines

    return {
        "input_file_path": input_file_path,
        "output_file_path": output_file_path,
        "column_name": column_name,
        "max_lines": max_lines,
    }


def ask_overwriting(file_path):
    print(f"{file_path}を上書きしますか？ y/n")
    while 1:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("'y'（yes）または'n'（no）で答えてください。")


def get_alt_file_path(file_path):
    # "./file.csv" -> "./file(1).csv"
    def alt_filename(index):
        root, ext = os.path.splitext(file_path)
        return root + f"({index})" + ext

    index = 1
    while os.path.isfile(alt_filename(index)):
        index += 1
    return alt_filename(index)


def main():
    args = analyze_args()
    input_file_path = args["input_file_path"]
    output_file_path = args["output_file_path"]
    column_name = args["column_name"]
    max_lines = args["max_lines"]

    input_path_or_buf = input_file_path if sys.stdin.isatty() else sys.stdin
    output_path_or_buf = output_file_path if sys.stdout.isatty() else sys.stdout

    try:
        # 欠損している場所はからの文字列として扱う方が後のコードが単純になる
        df = pd.read_csv(input_path_or_buf).fillna("")
    except FileNotFoundError:
        print(f"{input_file_path}というファイルは存在しません。")
        exit(0)
    except Exception as e:
        print(e)
        exit(0)

    # 先頭から`max_lines`件の論文以外を消す
    if max_lines is not None and len(df) > max_lines:
        df = df.drop(df.index[[i for i in range(max_lines, len(df))]])

    translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
    source_text_list = df[column_name].tolist()
    try:
        translated_text_list = translator.translate_text(source_text_list, target_lang="JA")
    except Exception as e:
        print(e)
        exit(0)

    insert_loc = df.columns.get_loc(column_name) + 1
    df.insert(insert_loc, f"{column_name} (和訳)", translated_text_list)

    if sys.stdout.isatty() and os.path.isfile(output_file_path):
        do_overwrite = ask_overwriting(output_file_path)
        if not do_overwrite:
            output_file_path = get_alt_file_path(output_file_path)
    try:
        df.to_csv(output_path_or_buf, index=False)
        if sys.stdout.isatty():
            print(f"{output_file_path}に保存しました。")
    except Exception as e:
        print(e)
        exit(0)


if __name__ == "__main__":
    main()
