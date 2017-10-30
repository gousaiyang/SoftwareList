# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

from SLHelper import date_sanitizer
from SLHTMLGeneration import placeholder, render_page, open_html_in_browser
from SLUpdateDetection import update_detection_list

def web_query(url, selector):
    try:
        r = requests.get(url)
    except Exception as e:
        print('Error: %s' % (e))
        return '[Network Failure]'
    else:
        if selector['Type'] == 'Regex':
            result = re.findall(selector['Selector'], r.text)
            return result[0] if result else '[Parse Failure]'
        elif selector['Type'] == 'BeautifulSoup':
            soup = BeautifulSoup(r.text, 'html.parser')
            els = soup.select(selector['Selector'])
            return els[0].string if els else '[Parse Failure]'
        else:
            return '[Invalid Selector]'

def query_software():
    # TODO: Should read a "update list", only check them for update. Should read current version of them.
    for s in update_detection_list:
        print('Querying software: %s' % s['Name'])

        # Priority should be set in the update list.
        result = {'Name': s['Name'], 'Priority': 0, 'DownloadURL': s['DownloadURL']}

        if s['VersionDetection']:
            result['NewestVersion'] = web_query(s['CheckURL'], s['VersionDetection'])
        else:
            result['NewestVersion'] = placeholder

        if s['DateDetection']:
            result['Date'] = date_sanitizer(web_query(s['CheckURL'], s['DateDetection']))
        else:
            result['Date'] = placeholder

        yield result

def main():
    new_file = render_page(query_software(), 'Update')
    open_html_in_browser(new_file)

if __name__ == '__main__':
    main()
