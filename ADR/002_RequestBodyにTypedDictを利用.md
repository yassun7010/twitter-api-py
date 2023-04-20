# 決定#002: RequestBodyにTypedDictを利用

## ステータス

| 区分 | 日付 | 詳細             |
| ---- | ---- | ---------------- |
| 提案 | --   | 過去の決定のメモ |

## 経緯

リクエストパラメータを表す型に TypedDict を用いる。

### 導入経緯

ここで、設計時に最も重要視したのは、入力に必要な Json データをコピーし張り付けるだけで、 Python スクリプトからも呼べるようにするためである。

TypedDict ならば、それが可能だ。

```python
TwitterApiClient.from_app_oauth_env()
    .get_tweets({
        "ids": ["12345"],
        "media.fields": ["public_metrics"]
    })
```

Json をそっくり持ってくるだけで、簡単に API を呼び出すことができる。  
また、 Twitter API V2 のリクエストボディには "media.fields" のような、フィールド引数に使えないキーワードが存在する。  
TypedDict を使えば、どのように Python へ移植するかを考えずに使用できる。

## 代替案

### 複数のキーワード引数
この選択は当初採用された方式で合った。

```python
async def get_tweets(
    self,
    *,
    ids: list[str],
    expansions: Optional[list[Expansion]] = None,
    media_fields: Optional[list[MediaField]] = None,
) -> GetV2TweetsResponseBody:
    ...
```

この場合、抽象クラスと具象クラスに対して、複数の引数を繰り返し定義する必要がある。  
引数の数は一つにし、型でまとめた方が API の変更に対して強くなる。

また、 "media.fields" のような引数があった場合は、 "media_fields" 等に変換するコストが発生する。


### BaseModel や dataclass

レスポンス型には BaseModel を採用している。 #001 を参照。
リクエスト型に BaseModel を用いる場合、 API の呼び出しのために、毎回リクエストボディの型を import し、利用する必要がある。
そのため、使い勝手が落ちてしまう。

```python
TwitterApiClient.from_app_oauth_env()
    .get_tweets(
        GetV2TweetsRequestBody.parse_obj({
            "ids": ["12345"],
            "media.fields": ["public_metrics"]
        })
    )
```

## 対応工数

作りながら考えた。 0h

## 作成者

安谷尚人
