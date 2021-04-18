# -*- coding: utf-8 -*-

import subprocess

from SLHelper import keep_window_open

task_name = 'SoftwareList Daily Update'


def main():
    subprocess.call(('schtasks', '/Delete', '/TN', task_name, '/F'))
    keep_window_open()


if __name__ == '__main__':
    main()
