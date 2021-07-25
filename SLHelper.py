# -*- coding: utf-8 -*-

import re
import subprocess  # nosec
import tkinter
from tkinter import messagebox

import colorlabels as cl


def file_content(filename):
    with open(filename, 'rb') as fin:
        content = fin.read()
    return content.decode('utf-8')


def write_file(filename, content):
    with open(filename, 'wb') as fout:
        fout.write(content.encode('utf-8'))


def date_sanitizer(datestring):
    result = re.findall(r'(\d{4})[-./ ](\d{1,2})[-./ ](\d{1,2})', datestring, re.ASCII)
    return f'{result[0][0]}-{result[0][1]:0>2}-{result[0][2]:0>2}' if result else datestring.strip()


def alert_messagebox(title, content):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo(title, content)
    root.destroy()


def keep_window_open():
    cl.input('Press Enter to exit...')


def lower_name_sorted(data):
    return sorted(data, key=lambda x: x['Name'].lower())


def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s


def exec_powershell(command):
    # decode using OEM code page
    return subprocess.check_output(('powershell', command), encoding='oem')  # nosec
