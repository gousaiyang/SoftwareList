# -*- coding: utf-8 -*-

import os
import re
import traceback
from collections import defaultdict

from SLHelper import keep_window_open

html_files = set()
html_file_groups = defaultdict(list)
newest_files = set()


def get_all_files():
    for n in os.listdir('output'):
        r = re.findall(r'\ASoftwareList_([-_0-9A-Za-z]+)_\d{14}\.html\Z', n)
        if r:
            html_files.add(n)
            html_file_groups[r[0]].append(n)

    for k in html_file_groups:
        html_file_groups[k].sort()
        newest_files.add(html_file_groups[k][-1])


def delete_old_files():
    for f in html_files - newest_files:
        os.remove(os.path.join('output', f))


def main():
    get_all_files()
    delete_old_files()


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
