# -*- coding: utf-8 -*-

import re

def file_content(filename):
    with open(filename, 'r') as fin:
        content = fin.read()
    return content

def write_file(filename, content):
    with open(filename, 'wb') as fout:
        fout.write(content.encode('utf-8'))

def date_sanitizer(datestring):
    result = re.findall(r'(\d{4})[-./ ](\d{1,2})[-./ ](\d{1,2})', datestring)
    return '%s-%02d-%02d' % (result[0][0], int(result[0][1]), int(result[0][2])) if result else datestring
