# ======================================================
# 設定ファイル
# ======================================================
CONFIG = {
    # 使用するブラウザの種類
    'useBrowser': 'Chrome', # "Chrome" or "Firefox"
    # ヘッドレスブラウザを使用するかどうか
    'useHeadlessBrowser': False, #True or False
    # TEREBOAT情報（必須）
    'tereboatMemberNumber': '<加入者番号>', 
    'tereboatPin': '<PIN>',
    'tereboatLoginPassword': '<ログインパスワード>',
    'tereboatAmountOfMoney': 1, #入金金額
    'tereboatBetPassword': '<投票用パスワード>',
    # LINE Messaging API情報（任意）
    'lineUserId': '<LINE Messaging API設定で払い出したユーザID>',
    'lineChannelToken': '<LINE Messaging API設定で払い出したチャネルアクセストークン（長期）>'
}