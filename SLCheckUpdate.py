# -*- coding: utf-8 -*-

import re
import json
import itertools
import requests
from bs4 import BeautifulSoup

from SLHelper import file_content, date_sanitizer, alert_messagebox
from SLHTMLGeneration import placeholder, url_placeholder, disable_a, render_page, open_html_in_browser
from SLGetLocalSoftware import get_local_software
from SLSoftwareInfo import software_info

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
        elif selector['Type'] == 'BeautifulSoupWithRegex':
            soup = BeautifulSoup(r.text, 'html.parser')
            els = soup.select(selector['bs'])
            if not els:
                return '[Parse Failure]'
            result = re.findall(selector['re'], els[0].string)
            return result[0] if result else '[Parse Failure]'
        else:
            return '[Invalid Selector]'

def query_current_version(local_software, selector):
    if selector['Type'] == 'InName':
        result = list(itertools.chain(*(re.findall(selector['Selector'], x) for x in local_software.keys())))
        return result[0] if result else placeholder
    elif selector['Type'] == 'InVersion':
        result = [x for x in local_software.keys() if re.match(selector['Selector'], x)]
        return local_software[result[0]] if result else placeholder
    else:
        return '[Invalid Selector]'

def needs_update(current_version, newest_version):
    cv = current_version.strip()
    nv = newest_version.strip()
    return cv != nv or cv == placeholder

def check_update(local_software):
    for item in json.loads(file_content('CheckUpdateList.json')):
        if item.get('Ignored'):
            continue

        name = item['Name']
        print('Checking software: %s' % name)

        result = {'Name': name, 'Priority': item.get('Priority', '')}

        info = software_info.get(name, {})
        cuu = info.get('CheckUpdateURL')
        cvd = info.get('CurrentVersionDetection')
        nvd = info.get('NewestVersionDetection')
        rdd = info.get('ReleaseDateDetection')

        result['DownloadURL'] = info.get('DownloadURL', url_placeholder)
        result['DownloadAttribute'] = '' if 'DownloadURL' in info else disable_a
        result['CurrentVersion'] = query_current_version(local_software, cvd) if cvd else placeholder
        result['NewestVersion'] = web_query(cuu, nvd) if nvd else placeholder
        result['ReleaseDate'] = date_sanitizer(web_query(cuu, rdd)) if rdd else placeholder

        if needs_update(result['CurrentVersion'], result['NewestVersion']):
            yield result

def main():
    print('SoftwareList Update Check')
    print('Querying local software information...')
    update_list = list(check_update(get_local_software()))
    if update_list:
        new_file = render_page('Update', update_list)
        open_html_in_browser(new_file)
    else:
        alert_messagebox('SoftwareList Update Checker', 'All the software in the list is up to date!')

if __name__ == '__main__':
    main()
