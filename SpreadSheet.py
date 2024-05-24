import gspread
from google.oauth2.service_account import Credentials
from get_server_name import get_server
from error import get_error
from line_notify import send_line_notify

class SpreadSheet:
    def access_to_spreadSheet(self, spreadsheet_id, success_domain):
        try:
            send_line_notify("取得したドメインのスプレッドシートへの書き込みを開始します。")
            # Google APIに接続するためのスコープと認証情報
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file("./file/inspiring-tower-424202-g9-b6ee895eb2c2.json", scopes=scopes)
            # gspreadクライアントを認証
            client = gspread.authorize(credentials)
            # spreadsheet_id = "1drNKOhzedS3Q-owDhzP8z6ZmOQtKQji4gJlCQcELriM"
            spreadsheet = client.open_by_key(spreadsheet_id)
            
            sheet_title = spreadsheet.title
            print(f"Opened sheet title: {sheet_title}")
            
            self.insert_data_operation(spreadsheet, success_domain)
            
            
        except Exception as e:
            print(e)
            get_error(e, "ドメインのスプレッドシートへの書き込みに失敗しました。")
    
    def insert_data_operation(self, sheet, success_domain):
        try:
            
            server_name = get_server()
            workSheet = sheet.worksheet(server_name)
            col_index = 5
            data_index = 0
            data_list = success_domain
            
            

            while data_index < len(data_list):
                # 指定された行の範囲をチェック
                cell_list = workSheet.range(5, col_index, 15, col_index)
                
                # 空のセルを見つけてデータを入れる
                for cell in cell_list:
                    if cell.value == '':
                        cell.value = data_list[data_index]
                        workSheet.update_cells([cell])  # 更新
                        data_index += 1
                        if data_index >= len(data_list):
                            return "All data entered successfully."
                
                
                # 13行目まで空欄がなければ次の列へ
                if col_index >= workSheet.col_count:
                    return "No empty cells found and no more columns available."
                col_index += 1
            
            send_line_notify("取得したドメインのスプレッドシートへの書き込みに成功しました。")
        except Exception as e:
            print(e)
            get_error(e, "ドメインのスプレッドシートへの書き込みに失敗しました。")
    









