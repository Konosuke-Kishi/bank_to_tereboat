# TEREBOAT自動入金ツール

TEREBOATに毎月入金するのを自動化しました。<br>

## 使い方

### 1. ソースコードをクローン

```
git clone https://github.com/Konosuke-Kishi/bank_to_tereboat.git
```

### 2. 事前準備

各金融機関からTEREBOATの登録を行い <br>
加入者番号、暗証番号、ログインパスワード、投票用パスワードを控えておく<br>

### 3. 設定ファイルの編集

config.py を開いて、下記必須の設定値を入力してください。<br>

```
CONFIG = {
    # 使用するブラウザの種類
    'useBrowser': 'Chrome', # Firefox or Chrome
    # TEREBOAT情報（必須）
    'tereboatMemberNo': '<加入者番号>', 
    'tereboatPin': '<PIN>',
    'tereboatLoginPassword': '<ログインパスワード>',
    'tereboatAmountOfMoney': 1, #入金金額
    'tereboatBetPassword': '<取引パスワード>'
    ...
}
```

### 4. 準備完了！

これで、スクリプトの準備が完了しました。<br>
下記コマンドを入力すれば、自動入金作業が動作するはずです。

```
python3 main.py
```

### 5.定期実行の設定

定期実行する場合は cron.py を実行することでエラーの内容を LINE に通知することができる<br>
config.py に必要なクレデンシャル情報を設定すれば notify.py から LINE へ通知が飛ぶ<br>
