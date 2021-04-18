# -*- coding: utf-8 -*-

import os
import re
import subprocess

from SLHelper import keep_window_open

task_name = 'SoftwareList Daily Update'


def check_task_time(t):
    return re.match(r'^(?:[0-1][0-9]|2[0-3]):[0-5][0-9]$', t)


def input_task_time():
    t = ''
    while not check_task_time(t):
        t = input('Please set the time of daily update (in HH:mm 24 hours format):')
    return t


def get_updater():
    return os.path.abspath('CheckUpdate.bat')


def main():
    start_time = input_task_time()
    updater = get_updater()
    subprocess.call(('schtasks', '/Create', '/SC', 'DAILY', '/TN', task_name, '/TR', updater, '/ST', start_time, '/F'))
    keep_window_open()


if __name__ == '__main__':
    main()
