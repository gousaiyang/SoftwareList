# -*- coding: utf-8 -*-

import json

from SLHelper import exec_powershell

registry_locations = [
    'HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
    'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
    'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
]


def get_local_software_registry_items():
    for location in registry_locations:
        items = json.loads(exec_powershell(f'Get-ItemProperty {location}\\* | ConvertTo-Json'))
        if isinstance(items, list):
            yield from items
        else:
            yield items


def get_local_software():
    return {
        item['DisplayName']: item.get('DisplayVersion')
        for item in get_local_software_registry_items()
        if item.get('DisplayName')
    }
