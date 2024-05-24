import traceback
from line_notify import send_line_notify

def get_error(e, message):
    tb = traceback.extract_tb(e.__traceback__)
    # 最後のコールスタックを取得
    last_call_stack = tb[-1]
    file_name = last_call_stack.filename
    line_number = last_call_stack.lineno
    func_name = last_call_stack.name

    send_line_notify(f"{message}.\n\nAn error occurred in file '{file_name}', line {line_number}, in function '{func_name}'.\nError message: {e}")
