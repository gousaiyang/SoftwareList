# -*- coding: utf-8 -*-

import re
import subprocess
import sys

from SLConfigReader import get_aapt_config, get_adb_config
from SLHelper import keep_window_open

adb_exec = get_adb_config()
adb_shell = (adb_exec, 'shell')
aapt_exec = get_aapt_config()


def check_config():
    if not adb_exec:
        print('Error: adb executable path not configured.')
        keep_window_open()
        sys.exit(0)

    if not aapt_exec:
        print('Error: aapt executable path not configured.')
        keep_window_open()
        sys.exit(0)


def check_android_device():
    if subprocess.call(adb_shell + ('id',), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
        print('Error: no Android device connected.')
        keep_window_open()
        sys.exit(0)


def get_all_android_apps():
    all_packages_info = subprocess.check_output(adb_shell + ('cmd', 'package', 'list', 'packages', '-f', '-3'))
    for line in all_packages_info.decode().split('\r\n'):
        line = line.strip()

        if line:
            package_path, package_name = re.findall(r'package:(.*)=(.*)', line)[0]

            package_info = subprocess.run(adb_shell + (aapt_exec, 'd', 'badging', package_path),
                                          check=False, stdout=subprocess.PIPE).stdout

            try:
                common_name = re.findall(rb"application-label:'(.*)'\r?\n", package_info)[0].decode()
            except Exception:
                continue

            try:
                version = re.findall(rb"versionName='([^']+)'", package_info)[0].decode()
            except Exception:
                version = None

            yield (common_name, package_name, version)
