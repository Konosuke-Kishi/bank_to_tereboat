# ======================================================
# ライブラリ
# ======================================================
import logging, os
from main import delete_auto_payment_log, auto_payment
from notify import line_notify
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

# ログディレクトリを作成
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'cron.log')

# ロガー設定
logger = logging.getLogger('cron')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ======================================================
# 定期実行用スクリプト
# ======================================================
if __name__ == '__main__':
    logger.info('cron job started')
    # 月初ならログ削除
    delete_auto_payment_log()
    try:
      # 定額自動入金のメイン処理を実行
      auto_payment()
    # 要素が見つからない場合
    except NoSuchElementException as e:
      msg = "要素が見つかりませんでした"
      logger.exception(f"{msg}\n詳細: {e}")
      line_notify(msg)
    # 処理が遅く、タイムアウトしてしまった場合
    except TimeoutException as e:
      msg = "操作がタイムアウトしました"
      logger.exception(f"{msg}\n詳細: {e}")
      line_notify(msg)
    # WebDriver関連のエラーの場合
    except WebDriverException as e:
      msg = "WebDriverエラーが発生しました"
      logger.exception(f"{msg}\n詳細: {e}")
      line_notify(msg)
    # それ以外のエラーの場合
    except Exception as e:
      msg = f"予期しないエラーが発生しました"
      logger.exception(f"{msg}\n詳細: {e}")
      line_notify(f"{msg}\n{e}")
    # 正常に処理が終了した場合
    else:
      logger.info("正常に処理が完了しました")
      line_notify("正常に処理が完了しました")
    
    logger.info('cron job finished')