import gspread
from google.oauth2.service_account import Credentials


from error import get_error
from line_notify import send_line_notify
import time


def access_to_spreadSheet(spreadsheet_id, server_name):
      try:
  
            # Google APIに接続するためのスコープと認証情報
            scopes = [
                  'https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file("C:\\Users\\user\\Dropbox\\domain_auto\\file\\inspiring-tower-424202-g9-b6ee895eb2c2.json", scopes=scopes)
            # gspreadクライアントを認証
            client = gspread.authorize(credentials)
            # spreadcheet
            spreadsheet = client.open_by_key(spreadsheet_id)
            
            return spreadsheet
            
            check_D_row(spreadsheet, "D", 5, 15, server_name)
            check_spreadSheet(spreadsheet, server_name)

      
      
      except Exception as e:
            print(e)
            get_error(e, "ドメインのスプレッドシートチェックに失敗しました。")

def col_index_to_letter(col_index):
      """
      Convert a column index to a column letter (e.g., 1 -> 'A', 2 -> 'B', ..., 26 -> 'Z', 27 -> 'AA').
      """
      if col_index > 26:
            letter = chr((col_index - 1) // 26 + 64) + chr((col_index - 1) % 26 + 65)
      else:
            letter = chr(col_index + 64)
      return letter

def a1_to_col(col_label):
    col_index = 0
    for char in col_label.upper():
        col_index = col_index * 26 + (ord(char) - ord('A') + 1)
    return col_index

def check_D_row(sheet, column, start_row, end_row, server_name):
      try:
            workSheet = sheet.worksheet(server_name)
            # D列の1～15行目までのデータをすべて取り出す
            cells = workSheet.range(f"{column}{start_row}:{column}{end_row}")
            
            target_cells = workSheet.range(5, 3, 15, 3)
            
            value_list = []
            
            for cell in cells:
                  if cell.value != "":
                        value_list.append(cell.value)
            
            print(value_list)

            if len(value_list) <= 4 and len(value_list) != 0:
                  for i, cell in enumerate(cells):
                        target_cells[i].value = cell.value
                        cell.value = ''  # 現在の列のデータをクリア
                  workSheet.update_cells(target_cells)
                  workSheet.update_cells(cells)
            
      
      except Exception as e:
            print(e)
            
      

def check_row(sheet):
      try:
            max_col = 11

            # データが存在する列を格納する辞書
            filled_columns = []

            # 各列を調べる
            for col_index in range(5, max_col + 1):
                  # 指定された範囲内のセルを取得
                  cells = sheet.range(5, col_index, 15, col_index)
                  # この列にデータが入っているか確認
                  if any(cell.value for cell in cells):
                        # データがあれば、その列のデータを全て取得
                        filled_columns.append(col_index_to_letter(col_index))
                        

            return filled_columns
      except Exception as e:
            get_error(e, "エラーが起きました")

def is_empty(sheet):
      try:
            col_index = ord("D".upper()) - ord('A') + 1
            cells = sheet.range(5, col_index, 15, col_index)

            # すべてのセルが空かどうかをチェック
            is_empty = all(cell.value == '' for cell in cells)

            return is_empty
      except Exception as e:
            get_error(e, "エラーが起きました")
            
      
def check_spreadSheet(spreadsheet_id,server_name):
      try: 
            sheet = access_to_spreadSheet(spreadsheet_id, server_name)
            workSheet = sheet.worksheet(server_name)
            
            check_D_row(sheet, "D", 5, 15, server_name)
            
            
            if is_empty(workSheet):
                  columns = check_row(workSheet)
                  for col in columns:
                        current_col_index = a1_to_col(col)
                        target_col_index = current_col_index - 1

                        # 現在の列の全データを取得
                        current_cells = workSheet.range(5, current_col_index, 15, current_col_index)
                        # 移動先の列の全データを取得
                        target_cells = workSheet.range(5, target_col_index, 15, target_col_index)

                        # 現在の列のデータを移動先の列にコピー
                        for i, cell in enumerate(current_cells):
                              target_cells[i].value = cell.value
                              cell.value = ''  # 現在の列のデータをクリア

                        # セルを更新する
                        workSheet.update_cells(target_cells)
                        workSheet.update_cells(current_cells)
      except Exception as e: 
            get_error(e, f"スプレッドシートのドメインチェックに失敗しました。\n\n シート名: {server_name}")


def check_start():    
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","AWS@4号機" )
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","AWS@5号機" )
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","AWS@6号機" )
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","AWS@7号機" )
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","AWS@8号機" )
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode3（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode4（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode5（他社）")
      time.sleep(90)
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode5-2（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode5-3（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode5-4（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode6（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode6-2（他社）")
      check_spreadSheet("1tycxRzP4PT07_8Qy56zw1UxEgssNUXq439gzDoaEx00","Linode6-4（他社）")

check_start()





