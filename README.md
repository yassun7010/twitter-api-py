# ✨✨ Twitter API Client by Typed Python ✨✨

# Why do we needs new Twitter API Client?

今までの API クライアントに対し、常に不満を持っていました。

- 簡単にモックする手段を提供していない
- カプセル化によって、どの API を利用しているのかわからない
- ほとんどの API が型情報について不十分です。
- Twitter API の変更は突然やってくる。Twitter API の挙動がおかしくなったとき、すぐに我々の問題か Twitter API 側の問題かを切り分ける必要があります。

このライブラリは、Twitter の公式ドキュメントを重視しながらも、  
実際に API を叩くことができるのかを定期的に検査することを主眼に作られています。

# Design Concept
## Twitter API の何を使っているのか、ソースコード上で容易にエビデンスを得られること

私の知るプロジェクトでは 2 つの実装が行われていました。

1 つは直接 HttpClient で API を呼び出すことです。

```ruby
HttpClient.new.get("https://api.twitter.com/2/users/2244994945")
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
api.users(params)
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

このライブラリは、このような問題を解決します。実際には、次のような書き方を促します。

```python
from twitter_api import TwitterApiClient
twitter_client = TwitterApiRealClient.from_oauth2_app_env()

response = (
    twitter_client.request("https://api.twitter.com/2/tweets").get(
        {"ids": "1460323737035677698", "expansions": ["attachments.media_keys"]}
    )
)
```

このようなコードであれば、 Twitter API を使っていることは一目でわかります。
そして、このコードは型補完の助けを借りながら記述することができます。本当に快適です。

## クライアントライブライを用いた自動テスト

多くの API のクライアントアプリが、 Mock 用のツールを同時に用意してくれると大変うれしいです。

私の好みを反映して、本ライブラリも自動テスト用の Mock 機能を用意しています。

```python
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient

twitter_client = TwitterApiMockClient.from_oauth2_app_env()

response = (
    twitter_client.chain()
    .inject_get_response_body("https://api.twitter.com/2/tweets", expected_response)
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
        TwitterApiMockClient.from_oauth2_app_env()
        .inject_post_response_body("https://api.twitter.com/2/tweets", post_response)
        .inject_get_response_body("https://api.twitter.com/2/tweets/:id", get_response)
        .inject_delete_response_body("https://api.twitter.com/2/tweets", delete_response)
    )

    assert some_logic(twitter_client) is True
```

## 開発者向け

### 初回構築

```sh
# .env を読み取るプラグインを入れておく。
poetry self add poetry-dotenv-plugin

# 必要な物をインストール
poetry install
```

### サンプルの実行

```sh
poetry run python example/${EXAMPLE_FILE}.py
```

### 自動テストの実行

```sh
# 静的解析の実行
poetry run task lint

# 自動テストの実行
poetry run task test
```

### 外形監視用の自動テスト

本ツールには Twitter API を実際にたたいて応答を確認する自動テストが用意されています。

Twitter API の挙動がおかしくなったかは、簡単に確認することができます。
Twitter API が時たま起こす奇妙な挙動のテストケースを教えていただけると、大変助かります。

#### 外形監視用の自動テスト用の環境変数の設定

1. `.env.local` をコピーし、 `.env` を作成する。
2. [Twitter 開発者のページ](https://developer.twitter.com/en/portal/projects-and-apps) へ移動し、下記を取得する。
    - API_KEY
    - API_SECRET
    - ACCESS_TOKEN
    - ACCESS_SECRET
    - BEARER_TOEKN
    - CLIENT_ID
    - CLIENT_SECRET
    - CALLBACK_URL 
3. `OAUTH2_USER_ACCESS_TOKEN の作成方法` に従い、アクセストークンを取得する。
    - OAUTH2_USER_ACCESS_TOKEN
4. (任意) プレミアムなアカウントを持っている場合、そのアクセストークンを取得する。
    - OAUTH2_PREMIUM_ACCESS_TOKEN
5. 開発者としての自分の Twitter の UserId を取得する。
    - USER_ID
6. DM のグループ作成用に、自分以外の UserId を取得する。
    - PARTICIPANT_IDS
7. 外形監視の設定を `true` にする。
    - SYNTHETIC_MONITORING_TEST


#### OAUTH2_USER_ACCESS_TOKEN の作成方法

外形監視用の自動テストのうち、ユーザ認証されたアクセストークンが必要なテストが存在する。
（自動テスト上でアクセストークンが失効すると、 OAuth2UserAccessTokenExpired が発生する。）

下記のサンプルを実行すると、ユーザ認証で得られたアクセストークンを得ることができる。

先に、アプリのコールバックURL を [Twitter 開発者のページ](https://developer.twitter.com/en/portal/projects-and-apps)
で設定しておく必要がある。


```sh
poetry shell

python examples/oauth2/oauth2_flow_with_pkce.py

# Twitter の OAuth2.0 認証のリンクがターミナルに出力されるので、リンク先へ飛び、アプリ認証に同意する。
# 設定したコールバックURL に飛ばされるので、飛ばされた先の URL をコピーし、ターミナルに貼り付ける。
# 認証に成功すればアクセストークンを取得できる。
```
