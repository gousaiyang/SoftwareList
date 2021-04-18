# -*- coding: utf-8 -*-

import itertools
import re
import subprocess


def exec_powershell(command):
    return subprocess.check_output(('powershell', command), encoding='oem')  # decode using OEM code page


def parse_ps_output(content):
    for s in content.strip().split('\n\n'):
        r = re.findall(r'DisplayName\s*:\s*(.*)\nDisplayVersion\s*:\s*(.*)', s)
        if r:
            yield (r[0][0].strip(), r[0][1].strip())
        else:
            r = re.findall(r'DisplayName\s*:\s*(.*)', s)
            if r:
                yield (r[0].strip(), '')


def get_local_software():
    software_list = {}

    list1 = exec_powershell('Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Format-List DisplayName, DisplayVersion | out-string -Width 2000')
    list2 = exec_powershell('Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Format-List DisplayName, DisplayVersion | out-string -Width 2000')
    list3 = exec_powershell('Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Format-List DisplayName, DisplayVersion | out-string -Width 2000')

    for n, v in itertools.chain(parse_ps_output(list1), parse_ps_output(list2), parse_ps_output(list3)):
        software_list[n] = v

    return software_list
