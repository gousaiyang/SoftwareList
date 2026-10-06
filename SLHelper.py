# -*- coding: utf-8 -*-

import os
import re
import subprocess  # nosec
from pathlib import Path

import colorlabels as cl

__version__ = '2.0.0'

# Data files (Config.json, CheckUpdateList.json, MainSoftwareList.json) and
# resource directories (template/, themes/, output/) live next to the scripts.
# Resolve them against the script directory instead of the current working
# directory so the tools keep working when they are launched from anywhere,
# for example by the Windows Task Scheduler (which starts in C:\Windows\System32).
BASE_DIR = Path(__file__).resolve().parent


def sl_path(*parts):
    """Return an absolute path inside the SoftwareList project directory."""
    return str(BASE_DIR.joinpath(*parts))


def file_content(filename):
    with open(filename, 'rb') as fin:
        content = fin.read()
    return content.decode('utf-8')


def write_file(filename, content):
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, 'wb') as fout:
        fout.write(content.encode('utf-8'))


def date_sanitizer(datestring):
    result = re.findall(r'(\d{4})[-./ ](\d{1,2})[-./ ](\d{1,2})', datestring, re.ASCII)
    return f'{result[0][0]}-{result[0][1]:0>2}-{result[0][2]:0>2}' if result else datestring.strip()


def alert_messagebox(title, content):
    # Import tkinter lazily so that importing the modules (and the HTML/JSON
    # code paths) does not require a GUI toolkit to be installed.
    import tkinter
    from tkinter import messagebox

    root = tkinter.Tk()
    root.withdraw()
    try:
        messagebox.showinfo(title, content)
    finally:
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
