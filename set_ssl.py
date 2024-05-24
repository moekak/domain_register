# 環境変数を使うための準備
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from line_notify import send_line_notify
import time
from error import get_error
import copy

load_dotenv()


# ChromeDriverManagerを使ってChrome Driverのインスタンスを作成
def create_webdriver_instance():
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')  # SSLエラーを無視する
        driver = webdriver.Chrome(service=service, options=chrome_options)  # optionsを渡す
        return driver


def check_server():
    path = "./dns_info.txt"
    try:
        with open(path) as f:
            dns_data = f.read().strip()
            if(dns_data == "a @ 52.192.39.82"):
                return [os.getenv("AWS4_URL"), os.getenv("AWS4_ID"), os.getenv("AWS4_PASSWORD")]
            
            if(dns_data == "a @ 35.75.34.157"):
                return [os.getenv("AWS5_URL"), os.getenv("AWS5_ID"), os.getenv("AWS5_PASSWORD")]
            
            if(dns_data == "a @ 3.114.217.119"):
                return [os.getenv("AWS6_URL"), os.getenv("AWS6_ID"), os.getenv("AWS6_PASSWORD")]
            
            if(dns_data == "a @ 3.113.226.195"):
                return [os.getenv("AWS7_URL"), os.getenv("AWS7_ID"), os.getenv("AWS7_PASSWORD")]
            
            if(dns_data == "a @ 3.114.226.163"):
                return [os.getenv("AWS8_URL"), os.getenv("AWS8_ID"), os.getenv("AWS8_PASSWORD")]
            
            if(dns_data == "a @ 192.53.173.79"):
                return [os.getenv("LINODE3_URL"), os.getenv("LINODE3_ID"), os.getenv("LINODE3_PASSWORD")]
            
            if(dns_data == "a @ 172.104.32.187"):
                return [os.getenv("LINODE4_URL"), os.getenv("LINODE4_ID"), os.getenv("LINODE4_PASSWORD")]
            
            if(dns_data == "a @ 139.177.191.181"):
                return [os.getenv("LINODE5_URL"), os.getenv("LINODE5_ID"), os.getenv("LINODE5_PASSWORD")]
            
            if(dns_data == "a @ 172.104.56.67"):
                return [os.getenv("LINODE6_URL"), os.getenv("LINODE6_ID"), os.getenv("LINODE6_PASSWORD")]
            
            if(dns_data == "a @ 52.193.104.121"):
                return [os.getenv("DEVELOPMENT_URL"), os.getenv("DEVELOPMENT_ID"), os.getenv("DEVELOPMENT_PASSWORD")]
            
    except FileNotFoundError as e:
        get_error(e, "DNSのファイルが存在しません。")
        return None

    print("ERROR:dnsがマッチしません")
    return None


    

        
def login_to_aapanel(driver, login_url, username, password, retry=3):
    try:
        driver.get(login_url)

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
            EC.presence_of_element_located((By.CSS_SELECTOR, ".login_btn"))
        )
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        if(retry > 0): 
            login_to_aapanel(driver, login_url, username, password, retry - 1)
        else:
            get_error(e, "aapanelへのログインに失敗しました。")
            driver.quit()

def open_ssl_admin(driver, domain_data, domain, retry=3):
    print("Domain data:", domain_data)
    print("Type of domain data:", type(domain_data))
    try:
        if(domain_data[0] == domain):
            time.sleep(5)
            website_btn = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@href='/site']"))
            )

            driver.execute_script("arguments[0].click();", website_btn)

        if(domain_data[0] != domain):
            add_site_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@title='Add site']")
                )
            )
            driver.execute_script("arguments[0].click();", add_site_btn)

        else:
            add_site_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@title='Add site']")
                )
            )
            driver.execute_script("arguments[0].click();", add_site_btn)
    except Exception as e:
        if(retry > 0):
            driver.refresh()
            open_ssl_admin(driver, domain_data, domain, retry -1)
        else:
            get_error(e, "SSLの設定に失敗しました。")


def set_ssl(driver, domain, domain_data, retry=3):
    print(domain)
    try:
        time.sleep(3)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "webname"))
        ).send_keys(domain)
        
       

        force_ssl_check = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "force_ssl"))
        )
        
        

        driver.execute_script("arguments[0].click();", force_ssl_check)
      
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-name='ftp']")
            )
        )
        driver.execute_script("arguments[0].click();", element)
        
        print(f"{domain}だよyo")


        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".layui-layer-btn0"))
        )
        

        
        driver.execute_script("arguments[0].click();", submit_btn)

    except Exception as e:
        if(retry > 0):
            driver.refresh()
            open_ssl_admin(driver, domain_data, domain, retry -1)
            set_ssl(driver, domain, domain_data, retry -1)
        else:
            get_error(e, "SSLの設定に失敗しました。")




def set_ssl_process(driver, domain_data):
    for domain in domain_data:
        print(domain_data)
        open_ssl_admin(driver, domain_data, domain)
        set_ssl(driver, domain, domain_data)
        time.sleep(50)



def main_ssl_setting(domain_data):
        safe_domain_data = copy.deepcopy(domain_data)
        
        print(f"{safe_domain_data}186行目")
            
        try:
            send_line_notify("SSL登録の処理を開始します。")
            driver = create_webdriver_instance()
            aapanel_url = check_server()[0]
            aapanel_id = check_server()[1]
            aapanel_pass = check_server()[2]

            login_to_aapanel(driver, aapanel_url, aapanel_id, aapanel_pass)
            set_ssl_process(driver, safe_domain_data)
            send_line_notify("処理に成功しました。")
            driver.quit()
        except Exception as e:
            get_error(e, "エラーが起きました。")


      