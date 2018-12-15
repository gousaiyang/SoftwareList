# -*- coding: utf-8 -*-

from SLGetAndroidPackages import check_android_device, check_config, get_all_android_apps
from SLHTMLGeneration import open_html_in_browser, placeholder, render_page


def get_android_software_items():
    for cn, pn, v in get_all_android_apps():
        yield {'Name': cn, 'PackageName': pn, 'CurrentVersion': v or placeholder}


def main():
    check_config()
    check_android_device()
    new_file = render_page('Android', get_android_software_items())
    open_html_in_browser(new_file)


if __name__ == '__main__':
    main()
