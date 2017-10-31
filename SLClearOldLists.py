# -*- coding: utf-8 -*-

import os
import re

html_files = set()
html_file_groups = {}
newest_files = set()

def add_element_to_group(k, v):
    if k in html_file_groups:
        html_file_groups[k].append(v)
    else:
        html_file_groups[k] = [v]

def get_all_files():
    for n in os.listdir('output'):
        r = re.findall(r'SoftwareList_([-_0-9A-Za-z]+)_\d{14}\.html', n)
        if r:
            html_files.add(n)
            add_element_to_group(r[0], n)

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
    main()
