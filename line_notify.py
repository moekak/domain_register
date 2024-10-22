import requests

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'n3ta88vAQMihAzyJq20bJfB5j0pkiTTWoD40ofab4qK'  # アクセストークンをここに入力
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': notification_message}
    response = requests.post(line_notify_api, headers=headers, data=data)
    return response.status_code, response.text

