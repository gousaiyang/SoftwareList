# -*- coding: utf-8 -*-

# TODO: Enrich this list with more software.

update_detection_list = [
    {
        'Name': 'Git',
        'DownloadURL': 'https://git-scm.com/',
        'CheckURL': 'https://git-scm.com/',
        'VersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'span[class="version"]'
        },
        'DateDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'span[class="release-date"]'
        }
    },
    {
        'Name': 'Python 3',
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckURL': 'https://www.python.org/',
        'VersionDetection': {
            'Type': 'Regex',
            'Selector': r'Latest: <a href="[^"]*">Python (3\.[\d.]+)</a>'
        },
        'DateDetection': None
    },
    {
        'Name': 'QQ',
        'DownloadURL': 'https://im.qq.com/',
        'VersionDetection': None,
        'DateDetection': None
    }
]
