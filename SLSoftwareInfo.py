# -*- coding: utf-8 -*-

# TODO: Enrich this list with more software.

software_info = {
    'Git': {
        'DownloadURL': 'https://git-scm.com/',
        'CheckUpdateURL': 'https://git-scm.com/',
        'CurrentVersionDetection': r'Git version',
        'NewestVersionDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'span[class="version"]'
        },
        'ReleaseDateDetection': {
            'Type': 'BeautifulSoup',
            'Selector': 'span[class="release-date"]'
        }
    },
    'Python 3': {
        'DownloadURL': 'https://www.python.org/downloads/',
        'CheckUpdateURL': 'https://www.python.org/',
        'CurrentVersionDetection': r'Python 3\..*Core Interpreter',
        'NewestVersionDetection': {
            'Type': 'Regex',
            'Selector': r'Latest: <a href="[^"]*">Python (3\.[\d.]+)</a>'
        },
    },
    'QQ': {
        'DownloadURL': 'https://im.qq.com/',
        'CurrentVersionDetection': r'腾讯QQ'
    },
    'Wechat': {
        'DownloadURL': 'https://pc.weixin.qq.com/'
    }
}
