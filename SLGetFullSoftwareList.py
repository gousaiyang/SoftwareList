# -*- coding: utf-8 -*-

from SLGetLocalSoftware import get_local_software
from SLHTMLGeneration import render_page, open_html_in_browser

def get_local_software_items():
    for n, v in get_local_software().items():
        yield {'Name': n, 'CurrentVersion': v}

def main():
    new_file = render_page('Full', get_local_software_items())
    open_html_in_browser(new_file)

if __name__ == '__main__':
    main()
