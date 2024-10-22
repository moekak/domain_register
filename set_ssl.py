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
            
            if(dns_data == "a @ 139.162.54.8"):
                return [os.getenv("LINODE5_2_URL"), os.getenv("LINODE5_2_ID"), os.getenv("LINODE5_2_PASSWORD")]
        
            if(dns_data == "a @ 172.104.172.127"):
                return [os.getenv("LINODE5_3_URL"), os.getenv("LINODE5_3_ID"), os.getenv("LINODE5_3_PASSWORD")]
        
            if(dns_data == "a @ 139.162.45.31"):
                return [os.getenv("LINODE5_4_URL"), os.getenv("LINODE5_4_ID"), os.getenv("LINODE5_4_PASSWORD")]
            
            if(dns_data == "a @ 172.104.56.67"):
                return [os.getenv("LINODE6_URL"), os.getenv("LINODE6_ID"), os.getenv("LINODE6_PASSWORD")]
            
            if(dns_data == "a @ 172.104.172.147"):
                return [os.getenv("LINODE6_2_URL"), os.getenv("LINODE6_2_ID"), os.getenv("LINODE6_2_PASSWORD")]
        
            if(dns_data == "a @ 172.104.57.116"):
                return [os.getenv("LINODE6_4_URL"), os.getenv("LINODE6_4_ID"), os.getenv("LINODE6_4_PASSWORD")]
            
            if(dns_data == "a @ 52.193.104.121"):
                return [os.getenv("DEVELOPMENT_URL"), os.getenv("DEVELOPMENT_ID"), os.getenv("DEVELOPMENT_PASSWORD")]
            
            if(dns_data == "a @ 192.53.116.144"):
                return [os.getenv("ORIGINAL_URL"), os.getenv("ORIGINAL_ID"), os.getenv("ORIGINAL_PASSWORD")]
            
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

    try:
        if(domain_data[0] == domain):
            print("yey")
            time.sleep(5)
            website_btn = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@href='/site/php']"))
            )

            driver.execute_script("arguments[0].click();", website_btn)
            
            print("click!")
            
            add_site_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='n-button__content' and text()='Add site']")
                )
            )
            
            print(add_site_btn)
            driver.execute_script("arguments[0].click();", add_site_btn)

        if(domain_data[0] != domain):
            add_site_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='n-button__content' and text()='Add site']")
                )
            )
            driver.execute_script("arguments[0].click();", add_site_btn)
    except Exception as e:
        if(retry > 0):
            get_error(e, f"SSLの設定に失敗しました。再度設定を試みます。\n\n domain: {domain}")
            driver.refresh()
            open_ssl_admin(driver, domain_data, domain, retry -1)
        else:
            get_error(e, f"SSLの再度設定を試みましたが失敗しました。\n\n domain: {domain}")


def set_ssl(driver, domain, domain_data, retry=3):
    print(domain)
    try:
        time.sleep(3)
        
        textarea =  WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@class='n-input__textarea-el' and @spellcheck='false' and @rows='3']"))
        )

        textarea.send_keys(domain)

        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'n-button') and .//span[text()='Confirm']]"))
        )
        
        driver.execute_script("arguments[0].click();", submit_btn)

    except Exception as e:
        if(retry > 0):
            driver.refresh()
            get_error(e, f"SSLの設定に失敗しました。再度設定を試みます。\n\n domain: {domain}")
            open_ssl_admin(driver, domain_data, domain, retry -1)
            set_ssl(driver, domain, domain_data, retry -1)
        else:
            get_error(e, f"再度設定を試みましたがSSLの設定に失敗しました。次の処理に入ります。\n\n domain: {domain}")




def set_ssl_process(driver, domain_data):
    for domain in domain_data:
        print(domain_data)
        open_ssl_admin(driver, domain_data, domain)
        print("kokokoko")
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


      