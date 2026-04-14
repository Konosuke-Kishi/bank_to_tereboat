# ======================================================
# ライブラリ
# ======================================================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, chromedriver_autoinstaller, geckodriver_autoinstaller
from config import CONFIG

# ======================================================
# 設定ファイルの読み込み
# ======================================================
# 使用するブラウザの種類
USE_BROWSER = CONFIG['useBrowser']
# ヘッドレスブラウザを使用するかどうか
USE_HEADLESS_BROWSER = CONFIG['useHeadlessBrowser']
# TEREBOAT情報（必須）
TEREBOAT_PIN = CONFIG['tereboatPin']
TEREBOAT_BET_PWD = CONFIG['tereboatBetPassword']
TEREBOAT_MEMBER_NO = CONFIG['tereboatMemberNumber']
TEREBOAT_LOGIN_PWD = CONFIG['tereboatLoginPassword']
TEREBOAT_MONEY_AMT = CONFIG['tereboatAmountOfMoney']
# 待機時間
ELEMENT_WAIT_TIME = CONFIG['elementWaitTime']

# ======================================================
# ドライバの設定
# ======================================================
def create_driver():
  if(USE_BROWSER == "Firefox"):
    executable_path = geckodriver_autoinstaller.install()
    options = webdriver.FirefoxOptions()
    options.add_argument('--disable-popup-blocking')
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.firefox.service.Service(executable_path)
    return webdriver.Firefox(service=service, options=options)
  if(USE_BROWSER == "Chrome"):
    executable_path = chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-popup-blocking')
    options.headless = USE_HEADLESS_BROWSER
    service = webdriver.chrome.service.Service(executable_path)
    return webdriver.Chrome(service=service, options=options)

# ======================================================
# 定額自動入金のメイン処理
# ======================================================
def auto_payment():
  # driverの設定
  driver = create_driver()
  # ======================================================
  # 1. TEREBOATログイン処理
  # ======================================================
  # TEREBOATのログインページを開く
  driver.get("https://ib.mbrace.or.jp/")
  # TEREBOATの加入者番号入力
  member_no = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.NAME, "memberNo")))
  member_no.send_keys(TEREBOAT_MEMBER_NO)
  # TEREBOATのPIN入力
  pin = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.NAME, "pin")))
  pin.send_keys(TEREBOAT_PIN)
  # TEREBOATのログインパスワード入力
  password = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.NAME, "authPassword")))
  password.send_keys(TEREBOAT_LOGIN_PWD)
  # TEREBOATのログインボタン押下
  login_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "loginButton")))
  login_button.click()

  # ======================================================
  # 2. TEREBOAT振込指示処理
  # ======================================================
  # 現在のウィンドウハンドルを保存
  main_window_handle = driver.current_window_handle
  # 新しいウィンドウが開くのを待つ
  WebDriverWait(driver, ELEMENT_WAIT_TIME).until(EC.number_of_windows_to_be(2))
  # 新しいウィンドウへ切り替え
  for handle in driver.window_handles:
      if handle != main_window_handle:
          driver.switch_to.window(handle)
          break
  # 未読のお知らせがあれば閉じるボタン押下
  time.sleep(ELEMENT_WAIT_TIME)
  news_close_button = driver.find_elements(By.ID, "newsoverviewdispCloseButton")
  if news_close_button:
      news_close_button[0].click()
      print("お知らせスキップ")
  else: pass
  # メニューボタン押下
  menu_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "gnavi01")))
  menu_button.click()
  # 入金開始ボタン押下
  charge_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "charge")))
  charge_button.click()
  # 入金額を入力
  input_money = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "chargeInstructAmt")))
  input_money.send_keys(TEREBOAT_MONEY_AMT)
  # 取引パスワード入力
  input_bet_passwd = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "chargeBetPassword")))
  input_bet_passwd.send_keys(TEREBOAT_BET_PWD)
  # 入金指示ボタン押下
  execute_charge_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "executeCharge")))
  execute_charge_button.click()
  # 入金指示確認ボタン押下
  ok_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "ok")))
  ok_button.click()
  # 入金指示完了後の閉じるボタン押下
  close_button = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(
    EC.element_to_be_clickable((By.ID, "closeChargecomp")))
  close_button.click()
  # 処理終了
  driver.quit()

if __name__ == "__main__":
    auto_payment()