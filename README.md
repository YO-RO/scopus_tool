# Scopus-tool

Scopusからエクスポートした論文一覧のCSVファイルを分析して、翻訳の追加や正規表現を使ったキーワード検索などをできるソフトウェア。

## 実装済みリスト

- [ ] フィルター
- [ ] 翻訳
- [ ] キーワード一覧の作成

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
-i: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`

### 翻訳の追加

エクスポートした論文一覧に要約を含めることができる。この要約をDeepLのAPIを使って和訳する。

---
**API Key**

以下のフォーマットに沿った `.env` ファイルをルートディレクトリに作成する必要がある。もし1Password CLIを使っているなら、以下のアイテムを作成した後に `op inject -i ./.env.template -o ./.env` を実行することで `.env` ファイルを作成できる。

```.env
DEEPL_API_URL={URL}
DEEPL_API_KEY={API_KEY}
```
---


```shell
python3 -m scopus_tool.translate -i {input_file_path}
```

#### Flags

-i: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`

### キーワード一覧の作成

キーワードと指定された回数の一覧を作成できる。

```shell
python3 -m scopus_tool.collect_keywords -i {input_file_path}
```

#### Flags

-i: 論文一覧のCSVファイルパス、たとえば `-i ./list.csv`
-o: 出力するCSVファイルのパス、デフォルトはkeywords.csv
