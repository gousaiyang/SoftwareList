# -*- coding: utf-8 -*-

import re
import itertools
from subprocess import Popen, PIPE, STDOUT

def exec_powershell(command):
    p = Popen(['powershell', command], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    return p.communicate()[0]

def get_name_and_version(content):
    for s in content.strip().split('\r\n\r\n'):
        r = re.findall(r'DisplayName(?:\s*):(?:\s*)(.*)\r\nDisplayVersion(?:\s*):(?:\s*)(.*)', s)
        if r:
            yield (r[0][0].strip(), r[0][1].strip())
        else:
            r = re.findall(r'DisplayName(?:\s*):(?:\s*)(.*)', s)
            if r:
                yield (r[0].strip(), '')

def get_local_software():
    software_list = {}

    list1_b = exec_powershell('Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Format-List DisplayName, DisplayVersion | out-string -Width 2000')
    list2_b = exec_powershell('Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Format-List DisplayName, DisplayVersion | out-string -Width 2000')

    for n, v in itertools.chain(get_name_and_version(list1_b.decode('gbk')), get_name_and_version(list2_b.decode('gbk'))):
        software_list[n] = v

    return software_list
