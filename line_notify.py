import requests
import os

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")  # アクセストークンをここに入力
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': notification_message}
    response = requests.post(line_notify_api, headers=headers, data=data)
    return response.status_code, response.text

