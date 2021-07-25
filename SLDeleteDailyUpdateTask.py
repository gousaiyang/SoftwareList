# -*- coding: utf-8 -*-

import subprocess  # nosec
import traceback

from SLHelper import keep_window_open

task_name = 'SoftwareList Daily Update'


def main():
    subprocess.call(('schtasks', '/Delete', '/TN', task_name, '/F'))  # nosec


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
    keep_window_open()
