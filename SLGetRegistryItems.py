# -*- coding: utf-8 -*-

import traceback

import colorlabels as cl

from SLGetLocalSoftware import get_local_software_registry_items
from SLHelper import keep_window_open, remove_prefix


def main():
    while True:
        name = cl.input('Please input a keyword of the name of the software: ').strip()
        if name:
            break

    result = {
        item['DisplayName']: remove_prefix(item['PSPath'], 'Microsoft.PowerShell.Core\\Registry::')
        for item in get_local_software_registry_items()
        if name.lower() in item.get('DisplayName', '').lower()
    }

    if not result:
        cl.error('Registry item not found')
    else:
        cl.success(f'Found registry items:\n{chr(10).join(f"{k!r} at {v}" for k, v in result.items())}')


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
    keep_window_open()
