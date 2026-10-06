# -*- coding: utf-8 -*-

import re
import subprocess  # nosec
import traceback

import colorlabels as cl

from SLHelper import keep_window_open, sl_path

task_name = 'SoftwareList Daily Update'


def check_task_time(t):
    return re.fullmatch(r'(?:[0-1][0-9]|2[0-3]):[0-5][0-9]', t)


def input_task_time():
    t = ''
    while not check_task_time(t):
        t = cl.input('Please set the time of daily update (in HH:MM 24 hours format): ')
    return t


def get_updater():
    # Anchor to the script directory: the task will later be launched by
    # Windows with an unrelated working directory.
    return sl_path('CheckUpdate.bat')


def main():
    start_time = input_task_time()
    updater = get_updater()
    subprocess.call((  # nosec
        'schtasks', '/Create', '/SC', 'DAILY',
        '/TN', task_name, '/TR', updater, '/ST', start_time, '/F'
    ))


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
    keep_window_open()
