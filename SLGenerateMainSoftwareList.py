# -*- coding: utf-8 -*-

import json

from SLHelper import file_content
from SLHTMLGeneration import url_placeholder, disable_a, render_page, open_html_in_browser
from SLSoftwareInfo import software_info

def get_main_software():
    for item in json.loads(file_content('MainSoftwareList.json')):
        name = item['Name']
        result = {'Name': name, 'Priority': item.get('Priority', '')}
        info = software_info.get(name, {})
        result['DownloadURL'] = info.get('DownloadURL', url_placeholder)
        result['DownloadAttribute'] = '' if 'DownloadURL' in info else disable_a
        yield result

def main():
    new_file = render_page('Main', get_main_software())
    open_html_in_browser(new_file)

if __name__ == '__main__':
    main()
