# -*- coding: utf-8 -*-

import re
import subprocess  # nosec
import sys

import colorlabels as cl

from SLConfigReader import get_aapt_config, get_adb_config
from SLHelper import keep_window_open

adb_exec = get_adb_config()
adb_shell = (adb_exec, 'shell')
aapt_exec = get_aapt_config()


def check_config():
    if not adb_exec:
        cl.error('Error: adb executable path not configured.')
        keep_window_open()
        sys.exit(0)

    if not aapt_exec:
        cl.error('Error: aapt executable path not configured.')
        keep_window_open()
        sys.exit(0)


def check_android_device():
    if subprocess.call(adb_shell + ('id',), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):  # nosec
        cl.error('Error: no Android device connected.')
        keep_window_open()
        sys.exit(0)


def get_all_android_apps():
    all_packages_info = subprocess.check_output(adb_shell + ('cmd', 'package', 'list', 'packages', '-f', '-3'),  # nosec
                                                encoding='utf-8')
    for line in all_packages_info.splitlines():
        line = line.strip()

        if line:
            package_path, package_name = re.findall(r'package:(.*)=(.*)', line)[0]

            package_info = subprocess.run(adb_shell + (aapt_exec, 'd', 'badging', package_path),  # nosec
                                          check=False, stdout=subprocess.PIPE, encoding='utf-8').stdout

            try:
                common_name = re.findall(r"application-label:'(.*)'\n", package_info)[0]
            except Exception:  # pylint: disable=broad-except  # nosec
                continue

            try:
                version = re.findall(r"versionName='([^']+)'", package_info)[0]
            except Exception:  # pylint: disable=broad-except
                version = None

            yield (common_name, package_name, version)
