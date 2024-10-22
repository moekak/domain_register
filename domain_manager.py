from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from line_notify import send_line_notify
from error import get_error
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
# 環境変数を使うための準備
from dotenv import load_dotenv
import os, time, logging, configparser
from get_server_name import get_server
load_dotenv()

# confファイルを使用する
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')


# グローバル変数の初期化(ユーザーがドメインを入力したとき用)
user_input_data = None
# success_domain = None



# ChromeDriverManagerを使ってChrome Driverのインスタンスを作成
def create_webdriver_instance():
      from webdriver_manager.chrome import ChromeDriverManager
      from selenium.webdriver.chrome.service import Service
      service = Service(ChromeDriverManager().install())
      driver = webdriver.Chrome(service=service)
      return driver


# valueドメインにログインする処理
def access_to_site(driver, login_url, retry=2):
      try:
            logging.info(config["logtext"]["AccessToSite"])
            # URLにアクセスする
            driver.get(login_url)
            # ログインボタンを押す
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            login_btn = WebDriverWait(driver, 30).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "#hd_login"))
            )
            logging.info(config["logtext"]["FindLoginBtn"])
            driver.execute_script("arguments[0].click();", login_btn)
      except Exception as e:
            if(retry > 0):
                  print(f"Error occurred: {e}. Retrying...")
                  access_to_site(driver, login_url, retry - 1)
            else:
                  get_error(e, "value domainへのアクセスに失敗しました。")
                  driver.quit()

def login_to_site(driver,username, password, retry=3):
      try:
            # ユーザーネームを入力する
            WebDriverWait(driver, 10).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
            ).send_keys(username)

            # パスワードを入力する
            WebDriverWait(driver, 10).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
            ).send_keys(password)

            #ログインする  
            login_button = WebDriverWait(driver, 10).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "#login_submit_btn"))
            )
            driver.execute_script("arguments[0].click();", login_button)
      except Exception as e:
            if(retry > 0): 
                  driver.refresh()  # ページを更新する
                  login_to_site(driver, username, password, retry-1)
                  print(f"Error occurred: {e}. Retrying...")
            else: 
                  get_error(e, "value domainへのログインに失敗しました")
                  driver.quit()

            


# 登録したいドメインを入力する処理
def enter_domain_name(driver, retry=3):
      try:
            # ドメイン一括登録ボタンを押す
            register_btn = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#cpside_domain_all"))
                  )
            driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
            driver.execute_script("arguments[0].click();", register_btn)

            link_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//a[text()="ドメインの一括空き検索"]'))
                  )

            driver.execute_script("arguments[0].click();", link_element)
      except Exception as e:
            if(retry > 0): 
                  driver.refresh()  # ページを更新する
                  enter_domain_name(driver, retry -1)
            else:
                  get_error(e, "ドメイン一括検索に失敗しました")
                  driver.quit()

# todo
# 登録したいドメインの価格を表示させるための処理
def display_domain_price(driver, user_input_data, retry=3):
      try:
            for data in user_input_data:
                  textarea  = driver.find_element(by=By.CSS_SELECTOR, value="#searchArea")
                  textarea.send_keys(data)
                  textarea.send_keys(Keys.ENTER)

            # ドメイン検索ボタンをクリックする
            result_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchdom_list")))
            driver.execute_script("arguments[0].click();", result_btn)

            # 各ドメインの情報が載ってるtrタグを返す
            return driver.find_elements(by=By.CSS_SELECTOR, value='[data-tld_puny]')
      except Exception as e:
            if(retry > 0): 
                  driver.refresh()  # ページを更新する
                  display_domain_price(driver, user_input_data, retry -1)
            else:
                  get_error(e,"ドメイン価格表示に失敗しました")


# ドメインの価格が範囲内かチェックする(boolean)
def check_domain_price(driver, user_input_data, retry=3):
      try:
            tr_elements = display_domain_price(driver, user_input_data)
            for element in tr_elements:
                  try:
                        price_element = element.find_element(By.CSS_SELECTOR, ".price")
                        price_text = price_element.text.replace("円", "")
                  except NoSuchElementException:
                        print("Price element not found in this row")
                        continue

                  if int(price_text) <= 500:
                        return True
                  else:
                        return False
      except Exception as e:
            if(retry > 0): 
                  driver.refresh()  # ページを更新する
                  check_domain_price(driver, user_input_data, retry -1)
            else:
                  get_error(e, "ドメイン価格表示に失敗しました")

            
def purchase_domain(driver, user_input_data):
      try:

            if(check_domain_price(driver, user_input_data)):
                  # 購入ボタンをクリックする」
                  purchase_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchdom_check02_entry"))
                  )
                  # ボタンが画面上に表示されてないからその要素までスクロールさせる
                  driver.execute_script("arguments[0].scrollIntoView(true);", purchase_btn)
                  driver.execute_script("arguments[0].click();", purchase_btn)

                  #登録させるドメイン
                  domain_data_list = user_input_data

                  # ドメインをtextareaに自動で入力させる
                  for data in domain_data_list:
                        textarea_el = driver.find_element(by=By.NAME, value="domains")
                        textarea_el.send_keys(data)
                        textarea_el.send_keys(Keys.ENTER)

                  # 次の画面で価格表示・登録者情報を設定するボタンをクリックする
                  next_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "modglobal3")))
                  driver.execute_script("arguments[0].click();", next_btn)

                  # 名義を代理公開する
                  open_el = driver.find_element(by=By.XPATH, value="//a[@href='#end']")
                  driver.execute_script("arguments[0].scrollIntoView(true);", open_el)
                  driver.execute_script("arguments[0].click();", open_el)

                  # アラートを取得
                  alert = Alert(driver)
                  # アラートのOKボタンをクリック
                  alert.accept()

                  # 次の画面で価格表示・登録者情報を設定するボタンをクリックする
                  register_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#searchdom_list02_entry")))
                  driver.execute_script("arguments[0].click();", register_btn)

                  # アラートのOKボタンをクリック
                  alert.accept()
            else:
                  send_line_notify("ドメインが500円超えています")
                  driver.quit()
      except Exception as e:
            get_error(e, "ドメインの購入に失敗しました")


# ドメイン登録処理中にエラーが起きた場合はの登録ドメインチェック
def process_purchase(driver, login_url, username, password, domain_data):
      try:
            # ドメイン登録処理に時間かかることがあるから、最大で1分待機させる
            success_el = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.NAME, "domains_list_success")))
            # ドメイン処理に成功したドメインを取得
            domain = success_el.text
            # 文字列をリストにへんぁん
            domain_list = domain.split()
            success_domain = domain_list
            success_domain_str = "\n".join(success_domain)
            send_line_notify(f"成功したドメイン:\n\n{success_domain_str}")
            return success_domain
      except  Exception:
            try: 
                  success_domain = check_success_domain(driver, login_url, username, password, domain_data)
                  success_domain_str = "\n".join(success_domain)
                  send_line_notify(f"成功したドメイン:\n\n{success_domain_str}")
                  return success_domain
            except Exception as e:
                  get_error(e, "ドメイン登録中にエラーが発生しました。")


def check_success_domain(driver, login_url, username, password, domain_data):
      success_domain = []
      try:
            create_webdriver_instance()
            access_to_site(driver, login_url, retry=3)
            login_to_site(driver,username, password)
            

            for domain in domain_data:
                  print(domain)

                  hover_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#cpside_domain"))
                  )

                  # ActionChainsを作成して要素にhoverする
                  actions = ActionChains(driver)
                  actions.move_to_element(hover_element).perform()


                  WebDriverWait(driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[placeholder=\"登録済みドメインを検索\"]"))
                  ).send_keys(domain)


                  search_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#btnDomainSearch"))
                  )
                  driver.execute_script("arguments[0].click();", search_btn)

                  try: 
                        domain_data = WebDriverWait(driver, 10).until(
                              EC.visibility_of_element_located((By.XPATH, f"//a[@href='/analyzer/{domain}']"))
                        )

                        success_domain.append(domain)
                  except:
                        print("no data")

            return success_domain

      except  Exception as e:
            get_error(e, "成功したドメインはありません。")


############################################### DNS設定 ########################################################

def login_to_site_for_dns(driver, login_url, retry = 3):
      try:
            driver.get(login_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            login_btn = WebDriverWait(driver, 30).until(
                  EC.presence_of_element_located((By.CSS_SELECTOR, "#hd_login"))
            )
            driver.execute_script("arguments[0].click();", login_btn)
      except Exception as e:
            if(retry > 0):
                  login_to_site_for_dns(driver, login_url, retry -1)
            else:
                  get_error(e, "DNSの設定に失敗しました。")
                  

def set_dns_for_each_domain(domain, driver, dns_data, retry = 3):
      try:
            # ドメイン名を入力する
            
            print("実行１")
            domain_input_field = WebDriverWait(driver, 50).until(
                  EC.visibility_of_element_located((By.CSS_SELECTOR, ".w43per"))
            )

            domain_input_field.send_keys(domain)
            
            
            print("実行2")
            search_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btnSubmitBlack")))
            driver.execute_script("arguments[0].click();", search_btn) 


            open_btn = WebDriverWait(driver, 20).until(
                  EC.visibility_of_element_located((By.XPATH, f"//a[@href='moddns.php?action=moddns2&domainname={domain}']"))
            )
            
            time.sleep(3)
            
            driver.execute_script("arguments[0].click();", open_btn)
         
            
            # DNS情報を入力する
            print("実行3")
            textarea = WebDriverWait(driver, 20).until(
                  EC.visibility_of_element_located((By.CSS_SELECTOR, "#records"))
            )
            
            textarea_value = textarea.get_attribute("value")
            
            if(textarea_value == ""):
                  print("実行4")
                  textarea.send_keys(dns_data)  
            
            time.sleep(3)
                  

            print("実行5")
            send_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inputSend")))
            driver.execute_script("arguments[0].scrollIntoView(true);", send_btn)
            driver.execute_script("arguments[0].click();", send_btn)

            print("実行6")
            return_button = WebDriverWait(driver, 30).until(
                  EC.visibility_of_element_located((By.XPATH, f"//a[@href='modall.php']"))
            )
            

            
            print("実行7")
            driver.execute_script("arguments[0].click();", return_button)
            send_line_notify(f"{domain}のDNS登録に成功しました。")
            time.sleep(5)
            
            
      except Exception as e:
            if(retry > 0):
                  get_error(e, f"DNS登録の最中にエラーが発生しました。再登録を試みます。 \n\n domain: {domain}")
                  elements = driver.find_elements(By.NAME, "btn_back")
                  if elements:
                        print("elment 見つかった！")
                        elements[0].click()
                        send_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inputSend")))
                        
                        print(send_btn)
                        
                        driver.execute_script("arguments[0].scrollIntoView(true);", send_btn)
                        driver.execute_script("arguments[0].click();", send_btn)

                  
                        return_button = WebDriverWait(driver, 60).until(
                              EC.visibility_of_element_located((By.XPATH, f"//a[@href='modall.php']"))
                        )
                        driver.execute_script("arguments[0].click();", return_button)
                        send_line_notify(f"再度の試みで{domain}のDNS登録に成功しました。")
                  else:
                        print("elment ない！")
                        driver.refresh()
                        set_dns_for_each_domain(domain, driver, dns_data, retry -1)
                        
                  
            else:
                  get_error(e, f"再登録を試みましたが失敗しました。 \n\n domain: {domain}")

def set_dns(driver, success_domain, dns_data):
      try:
            # ドメインの設定操作
            setting_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cpside_domain_config")))
            driver.execute_script("arguments[0].click();", setting_btn)
            

            for domain in success_domain:
                  set_dns_for_each_domain(domain, driver, dns_data, retry = 3)
                  
                  server_info = get_server()
                  
            send_line_notify(f"全てのドメインへのDNS設定に成功しました。次の処理が開始されます。\n\n サーバー名: {server_info}")
            print(f"{success_domain}346行目")
    
      except Exception as e:
            get_error(e, "DNS登録の最中にエラーが発生しました。")


def set_dns_process(success_domain, driver, login_url):
# # # DNS設定
      path = "./dns_info.txt"
      with open(path) as f:
            dns_data = f.read().strip()
            
      login_to_site_for_dns(driver, login_url)
      set_dns(driver, success_domain, dns_data)
      
      

def main(domain_data):
      try:
            driver = create_webdriver_instance()
            login_url = os.getenv("SITE_URL")
            username = os.getenv("LOGIN_ID")
            password = os.getenv("LOGIN_PASSWORD")


            access_to_site(driver, login_url)
            login_to_site(driver,username, password)
            enter_domain_name(driver)
            purchase_domain(driver, domain_data)
            # 成功したドメイン
            success_domain = process_purchase(driver, login_url, username, password, domain_data)
            
            # domain = ['bison-dolphin.info', 'panda-crocodile.click', 'arrow-banana.site', 'xylophone-van.site', 'yeti-yacht.click']
            print(f"{success_domain} 377行目")
            set_dns_process(success_domain, driver, login_url)
            
            return success_domain
      except Exception as e:
            get_error(e, "エラー発生")
            
