# -*- coding: utf-8 -*-

import json
import traceback

from SLHelper import file_content, keep_window_open, lower_name_sorted
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
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
