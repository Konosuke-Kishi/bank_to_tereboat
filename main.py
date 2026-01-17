# ======================================================
# ライブラリ
# ======================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from config_edit import CONFIG
import time, datetime, logging, os

# ======================================================
# 設定ファイル（config.py）の読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# TEREBOAT情報（必須）
TEREBOAT_MEMBER_NO = CONFIG['tereboatMemberNo']
TEREBOAT_PIN = CONFIG['tereboatPin']
TEREBOAT_LOGIN_PWD = CONFIG['tereboatLoginPassword']
TEREBOAT_MONEY_AMT = CONFIG['tereboatAmountOfMoney']
TEREBOAT_BET_PWD = CONFIG['tereboatBetPassword']

# ======================================================
# ログ削除メソッド(cron.pyから呼び出される)
# ======================================================
# 月初にログを削除する
def delete_auto_payment_log():
  # 今日の日付を取得
  today = datetime.date.today()
  # 今月の初日を取得
  first_date_month = today.replace(day=1)
  # 月初ならログファイル削除
  if(today == first_date_month):
    os.remove('./auto_payment.log')


# ======================================================
# ドライバの設定
# ======================================================
# 使用するブラウザのバージョンと一致するdriverをダウンロードし
# ブラウザごとにオプション・プロファイルを設定する
if(USE_BROWSER == "Firefox"):
  executable_path = "/usr/local/bin/geckodriver"
  options = webdriver.FirefoxOptions()
  options.add_argument('--headless') 
  options.add_argument('--disable-popup-blocking')
  service = webdriver.firefox.service.Service(executable_path=executable_path)
else:
  executable_path = "/usr/local/bin/chromedriver"
  options = webdriver.ChromeOptions()
  options.add_argument('--headless') 
  options.add_argument('--disable-popup-blocking')
  service = webdriver.chrome.service.Service(executable_path=executable_path)

# ======================================================
# 定額自動入金のメイン処理
# ======================================================
def auto_payment():

  # ======================================================
  # 0. 起動設定
  # ======================================================
  # ログ出力設定
  logging.basicConfig(
  # ログを保存するファイル名
  filename='auto_payment.log',
  # ログレベル（INFO以上を記録）
  level=logging.INFO,
  # ログ出力のフォーマット形式
  format='%(asctime)s - %(levelname)s - %(message)s'
  )
  # ブラウザを開く
  logging.info("==========処理開始==========")
  # 使用するブラウザによって分岐
  if(USE_BROWSER == "Firefox"):
    driver = webdriver.Firefox(options=options, service=service)
  else:
    driver = webdriver.Chrome(options=options, service=service)
  logging.info("WebDriver：ブラウザ起動完了")

  # ======================================================
  # 1. TEREBOATログイン処理
  # ======================================================
  # TEREBOATのログインページを開く
  driver.get("https://ib.mbrace.or.jp/")
  logging.info("WebDriver：サイトアクセス成功")
  time.sleep(5)
  # TEREBOATのユーザ名入力
  userid = driver.find_element(by=By.NAME, value="memberNo")
  userid.send_keys(TEREBOAT_MEMBER_NO)
  logging.info("TEREBOAT：ユーザ名入力")
  # TEREBOATのPIN入力
  userid = driver.find_element(by=By.NAME, value="pin")
  userid.send_keys(TEREBOAT_PIN)
  logging.info("TEREBOAT：PIN入力")
  # TEREBOATのログインパスワード入力
  password = driver.find_element(by=By.NAME, value="authPassword")
  password.send_keys(TEREBOAT_LOGIN_PWD)
  logging.info("TEREBOAT：ログインパスワード入力")
  # TEREBOATのログインボタン押下
  driver.find_element(by=By.ID, value="loginButton").click()
  logging.info("TEREBOAT：ログイン成功")
  time.sleep(5)

  # ======================================================
  # 2. TEREBOAT振込指示処理
  # ======================================================
    # ウインドウを切り替える（ポップアップウィンドウが開くまで待機）
  print(f"Window count before wait: {len(driver.window_handles)}")
  # ポップアップウィンドウが開くまで待機（最大15秒）
  for attempt in range(15):
    if len(driver.window_handles) > 1:
      break
    time.sleep(1)
  
  newhandles = driver.window_handles
  logging.info(f"ウィンドウ数: {len(newhandles)}")
  
  if len(newhandles) > 1:
    driver.switch_to.window(newhandles[1])
    logging.info("NEOBANK：ウィンドウ切替成功")
    time.sleep(3)
    # 入金開始ボタン押下
    try:
      driver.find_element(By.XPATH, "//*[@id=\"gnavi01\"]/span").click()
      logging.info("TEREBOAT：入金指示開始")
    except Exception as e:
      logging.warning(f"TEREBOAT：入金指示開始スキップ - {e}")
    time.sleep(3)
  else:
    logging.warning("TEREBOAT：ウィンドウが開かれていません")
    raise Exception("TEREBOAT ウィンドウが開かれていません")
  driver.find_element(By.XPATH, "//*[@id=\"charge\"]").click()
  # TEREBOATの入金額を入力
  input_money = driver.find_element(by=By.ID, value="chargeInstructAmt")
  input_money.send_keys(TEREBOAT_MONEY_AMT)
  logging.info("TEREBOAT：金額入力")
  # TEREBOATの取引パスワード入力
  input_bet_passwd = driver.find_element(by=By.ID, value="chargetBetPassword")
  input_bet_passwd.send_keys(TEREBOAT_BET_PWD)
  logging.info("TEREBOAT：取引パスワード入力")
  # TEREBOATの入金指示ボタン押下
  driver.find_element(by=By.ID, value="executeCharge").click()
  logging.info("TEREBOAT：入金指示確認ボタン押下")
  time.sleep(5)
  # TEREBOATの入金指示確認ボタン押下
  driver.find_element(by=By.ID, value="ok").click()
  logging.info("TEREBOAT：入金指示完了")
  time.sleep(5)
  driver.find_element(by=By.LINK_TEXT, value="閉じる").click()
  # TEREABOATのログアウト処理
  time.sleep(5)
  driver.find_element(by=By.LINK_TEXT, value="ログアウト").click()
  time.sleep(5)
  driver.find_element(by=By.ID, value="ok").click()