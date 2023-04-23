# 開発用のドキュメント

## 初期化

```sh
# Add .env loader
poetry self add poetry-dotenv-plugin

# Install Packages
poetry install
```


## 外形監視用の自動テスト用の環境変数の設定

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


### OAUTH2_USER_ACCESS_TOKEN の作成方法

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


## サンプルの実行

```sh
poetry run python examples/${EXAMPLE_FILE}.py
```

## 自動テストの実行

```sh
# 静的解析の実行
poetry run task lint

# 自動テストの実行
poetry run task test
```

### 外形監視用の自動テスト

本ツールには Twitter API を実際を呼んでレスポンスのフィールド項目を確認する自動テストが用意されています。

Twitter API の挙動がおかしくなったかは、簡単に確認することができます。
Twitter API が時たま起こす奇妙な挙動のテストケースを教えていただけると、大変助かります。
