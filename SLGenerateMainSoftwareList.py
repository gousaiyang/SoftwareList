# -*- coding: utf-8 -*-

import json

from SLHelper import file_content, lower_name_sorted
from SLHTMLGeneration import disable_a, open_html_in_browser, render_page, url_placeholder
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
    new_file = render_page('Main', lower_name_sorted(get_main_software()))
    open_html_in_browser(new_file)


if __name__ == '__main__':
    main()
