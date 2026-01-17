# ======================================================
# ライブラリ
# ======================================================
from config_edit import CONFIG
import requests
# ======================================================
# LINE通知処理
# ======================================================
def line_notify(message):
    # ConfigからLINE Messaging API情報読み込み
    LINE_USER_ID = CONFIG['lineUserId']
    LINE_C_TOKEN = CONFIG['lineChannelToken']
    # ヘッダー部分の内容を設定
    headers = {
        'Authorization': f'Bearer {LINE_C_TOKEN}',
        'Content-Type': 'application/json'
    }
    # データ部分の内容を設定
    title = "TEREBOAT即時入金"
    data = {
        'to': LINE_USER_ID,
        'messages': [{'type': 'text','text': f"{title}:\n{message}"}]
    }
    # LINE Messaging APIエンドポイント
    url = 'https://api.line.me/v2/bot/message/push'
    # メッセージ送信
    response = requests.post(url, headers=headers, json=data)
    # ログ出力設定
    with open("line_notify.log","w") as o:
        # ステータスを確認
        if response.status_code == 200:
            print(f"下記メッセージが正常に送信されました\n\"{title}:{message}\"",file=o)
        else:
            print(f"メッセージ送信エラーが発生しました\n\"{response.status_code}:{response.text}\"",file=o)