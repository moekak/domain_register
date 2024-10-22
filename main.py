from domain_manager import main
from generate_domain import generate_domain
from set_ssl import main_ssl_setting
from SpreadSheet import SpreadSheet
import time

spreadSheet = SpreadSheet()
# # # # # ドメインを20個作成
domain_amount  = int(input("ドメイン作成数を入力してください(半角数字): "))
dns_info = input("DNS情報を入力してください: ")

path = "./dns_info.txt"
with open(path, "w") as f:
    f.write(dns_info)

domain_data = []

while domain_amount > 0:    
    domain = generate_domain()
    domain_data.append(domain)
    domain_amount -= 1

success_domain = main(domain_data)
print(f"{success_domain} 成功したドメイン")


# ドメイン登録してから1時間後にaapanelに登録する

# SSL登録なし！
#SSLも登録する際は30分待つ
main_ssl_setting(success_domain)

spreadSheet.access_to_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00", success_domain)
