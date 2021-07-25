# -*- coding: utf-8 -*-

import traceback

from SLGetLocalSoftware import get_local_software
from SLHelper import keep_window_open, lower_name_sorted
from SLHTMLGeneration import open_html_in_browser, placeholder, render_page


def get_local_software_items():
    for n, v in get_local_software().items():
        yield {'Name': n, 'CurrentVersion': v or placeholder}


def main():
    new_file = render_page('Full', lower_name_sorted(get_local_software_items()))
    open_html_in_browser(new_file)


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
