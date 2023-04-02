# ✨✨ Twitter API Client by Typed Python ✨✨

# Why do we needs new twitter Api client?

今までの API クライアントに対し、常に不満を持っていました。

- 簡単にモックする手段を提供していない
- カプセル化によって、どの API を利用しているのかわからない
- ほとんどの API が型情報について不十分です。
- Twitter API の変更は突然やってくる。Twitter API の挙動がおかしくなったとき、すぐに我々の問題か Twitter API 側の問題かを切り分ける必要があります

私は、 Twitter API を利用したキャンペーンを実施する企業に勤めていましたが、
チームへの配属当初から、 Twitter API を自前のクライアントライブラリを作成し扱うべきと主張しました。

しかし、私は具体的な手段を示さなかったため、ここにその手段を書き留めておこうと思います。

私は会社を去ることになりましたが、 Twitter API を使ってビジネスや開発をしたい人は、
是非このライブラリを発展させてください。


# Design Concept
## Twitter API の何を使っているのか、ソースコード上で容易にエビデンスを得られること

私の会社では 2 つの実装が行われていました。

1 つは直接 HttpClient で API を呼び出すことです。

```ruby
HttpClient.get("https://api.twitter.com/2/users/2244994945")
```

この開発方法は決して快適ではありません。
ドキュメントを読み、自分の入力が合っているか画面とにらめっこし、
上手く動かなければ時間をかけてデバックする必要があるでしょう。

ヘッダの情報は大丈夫？
本当にドキュメントが正しい？
クエリパラメータで大丈夫？ 実はリクエストボディに書くべきではないのか？
動いた実績のあるコードを他のメンバーが持っているのではないだろうか？

小さな問題が山積みです。我々はもっと簡単に動かしたいのです。

もう一つは有名な Gem を使うことです。

```ruby
api.tweets
```

この方法は記述量が少なくなるかもしれませんが、致命的な問題を抱えていると思います。

Twitter API の仕様変更の連絡が Twitter 社から来ると、
プロジェクトで用いている Twitter API の一覧をマネージャーから求められますが、
全てのコードを追うのは辛い。

この点では、HttpCliet を使ってる方がずっとましでした。
具体的に、私は下記のようなコードが twitter API を内部的に実行ことに気づきませんでした。

```ruby
its.each do |it|
  it.followers(params)
end
```

まったく、こんなコードを書いたのは誰だ？

このライブラリは、このような問題を解決します。実際には、次のような書き方を促します。

```python
from twitter_api import TwitterApiClient
twitter_client = TwitterApiRealClient.from_app_auth_v2_env()

response = (
    twitter_client.request("https://api.twitter.com/2/tweets").get(
        {"ids": "1460323737035677698", "expansions": ["attachments.media_keys"]}
    )
)
```

このようなコードであれば、 Twitter API を使っていることは一目でわかります。
そして、このコードは型補完の助けを借りながら使うことができます。本当に快適です。

## クライアントライブライを用いた自動テスト

多くの API のクライアントアプリが、 Mock 用のツールを同時に用意してくれると、大変うれしいです。

私の好みを反映して、本ライブラリも自動テスト用の Mock 機能を用意しています。

```python
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient

twitter_client = TwitterApiMockClient.from_app_auth_v2_env()

response = (
    twitter_client.chain()
    .inject_get_response_body("https://api.twitter.com/2/tweets", response)
    .request("https://api.twitter.com/2/tweets").get(
        {"ids": "1460323737035677698", "expansions": ["attachments.media_keys"]}
    )
)
```

少し書き方が変わりました。 `TwitterApiClient` を使う箇所で、 `TwitterApiMockClient` を使う必要があります。
`TwitterApiMockClient` は `inject_*response_body` というメソッドを使うことができ、
これによって、簡単に戻りのデータ・例外を注入できます。

実際には、 `TwitterApiClient` を使う関数をプロジェクトで作成し、テスト時には関数を利用する前に、データ注入をすることになるでしょう。

```python

def some_logic(twitter_client: TwitterApiClient):
    ...

def test_some_logic():
    twitter_client = (
        TwitterApiMockClient.from_app_auth_v2_env()
        .inject_post_response_body("https://api.twitter.com/2/tweets", post_response)
        .inject_get_response_body("https://api.twitter.com/2/tweets", get_response)
        .inject_delete_response_body("https://api.twitter.com/2/tweets", delete_response)
    )

    assert some_logic(twitter_client) is True
```

## 外形監視用の自動テスト

本ツールには Twitter API を実際にたたいて応答を確認する自動テストが用意されています。

Twitter API の挙動がおかしくなったかは、簡単に確認することができます。
Twitter API が時たま起こす奇妙な挙動のテストケースを教えていただけると、大変助かります。
