from error import get_error
def get_server():
    path = "./dns_info.txt"
    try:
        with open(path) as f:
            dns_data = f.read().strip()
            if(dns_data == "a @ 52.192.39.82"):
                  return "AWS@4号機"
            
            if(dns_data == "a @ 35.75.34.157"):
                return "AWS@5号機"
            
            if(dns_data == "a @ 3.114.217.119"):
                return "AWS@6号機"
            
            if(dns_data == "a @ 3.113.226.195"):
                return "AWS@7号機"
            
            if(dns_data == "a @ 3.114.226.163"):
                return "AWS@8号機"
            
            if(dns_data == "a @ 192.53.173.79"):
                return "Linode3（他社）"
            
            if(dns_data == "a @ 172.104.32.187"):
                return "Linode4（他社）"
            
            if(dns_data == "a @ 139.177.191.181"):
                return "Linode5（他社）"
            
            if(dns_data == "a @ 172.104.56.67"):
                return "Linode6（他社）"
            
      
            
    except FileNotFoundError as e:
            get_error(2, "サーバーの名前取得に失敗しました。")
            return None

    print("ERROR:dnsがマッチしません")
    return None