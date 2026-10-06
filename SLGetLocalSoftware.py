# -*- coding: utf-8 -*-

import json

import colorlabels as cl

from SLHelper import exec_powershell

registry_locations = [
    'HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
    'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
    'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
]


def get_local_software_registry_items():
    for location in registry_locations:
        output = exec_powershell(f'Get-ItemProperty {location}\\* | ConvertTo-Json')

        # ConvertTo-Json writes nothing when the key holds no items (for example
        # on 32-bit-only systems, where the Wow6432Node key does not exist), so
        # an empty result is not an error.
        if not output.strip():
            continue

        try:
            items = json.loads(output)
        except json.JSONDecodeError as e:
            cl.error(f'Error: cannot parse registry items from {location}: {e}')
            continue

        if isinstance(items, list):
            yield from items
        else:
            yield items


def get_local_software():
    return {
        item['DisplayName']: item.get('DisplayVersion')
        for item in get_local_software_registry_items()
        if isinstance(item, dict) and item.get('DisplayName')
    }
