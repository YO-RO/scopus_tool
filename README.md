# Scopus-tool

Scopusからエクスポートした論文一覧のCSVファイルを分析して、翻訳の追加などをできるソフトウェア。現時点ではMacでしか動作確認はしていません。

## 実装済みリスト

- [ ] フィルター
- [x] 翻訳
- [ ] キーワード一覧の作成
- [ ] コマンドの連結
- [ ] 英語で出力されたCSVファイルへの対応
- [ ] WindowsとLinuxでの動作

## 使い方

```shell
rye sync
```

### キーワードによるフィルタリング

Scopusで「requirements engineering」とキーワード検索しても、「requirements」と「engineering」を含むだけの論文も引っかかる。この機能ではより厳格なキーワード検索ができる。

```shell
python3 -m scopus_tool.filter -i {input_file_path} {condition}
```

たとえば

```shell
python3 -m scopus_tool.filter -i ./list.csv "requirements engineering AND (nlp OR llm)
```

#### Args, Flags

condition: キーワードは小文字、論理演算子は大文字の"()" "AND" "OR"の3つ、"()" > "AND" > "OR"
-i: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`。
-o: 出力するCSVファイルのパス。

### 翻訳の追加

エクスポートした論文一覧に抄録を含めることができる。この抄録をDeepLのAPIを使って翻訳する。また、指定すれば別の列に変更できる。

---
**API Key**

以下のフォーマットに沿った `.env` ファイルをルートディレクトリに作成する必要がある。もし1Password CLIを使っているなら、以下のアイテムを作成した後に `op inject -i ./.env.template -o ./.env` を実行することで `.env` ファイルを作成できる。

```.env
DEEPL_API_KEY={API_KEY}
```
---


```shell
python3 -m scopus_tool.translate -i {input_file_path}
```

#### Flags

-i, --input-file-path: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`。デフォルトは`$HOME/Downloads/scopus.csv`。
-o, --output-file-path: 出力するCSVファイルのパス。デフォルトは`$HOME/Downloads/scopus_translation.csv`。
-c, --column: 翻訳する列を指定する。指定がなければ抄録の列が翻訳される。
-m, --max-lines: 翻訳する数。上からmax-lines行翻訳する。指定しない場合はすべて翻訳する。

### キーワード一覧の作成

キーワードと指定された回数の一覧を作成できる。

```shell
python3 -m scopus_tool.collect_keywords -i {input_file_path}
```

#### Flags

-i: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`。
-o: 出力するCSVファイルのパス、デフォルトはkeywords.csv。

## コマンドの連結

フィルターを実行した後に翻訳を実行する例

```shell
python3 -m scopus_tool.filter -i ./list.csv -o s "requirements engineering AND (nlp OR llm)" | \
python3 -m scopus_tool.translate -i s
```
