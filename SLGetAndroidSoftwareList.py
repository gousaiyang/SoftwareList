# -*- coding: utf-8 -*-

import traceback

from SLGetAndroidPackages import check_android_device, check_config, get_all_android_apps
from SLHelper import keep_window_open, lower_name_sorted
from SLHTMLGeneration import open_html_in_browser, placeholder, render_page


def get_android_software_items():
    for cn, pn, v in get_all_android_apps():
        yield {'Name': cn, 'PackageName': pn, 'CurrentVersion': v or placeholder}


def main():
    check_config()
    check_android_device()
    new_file = render_page('Android', lower_name_sorted(get_android_software_items()))
    open_html_in_browser(new_file)


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
