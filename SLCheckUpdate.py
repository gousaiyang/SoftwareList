# -*- coding: utf-8 -*-

import re
import json
import itertools
import requests
import colorlabels as cl
from bs4 import BeautifulSoup

from SLHelper import file_content, date_sanitizer, alert_messagebox
from SLHTMLGeneration import placeholder, url_placeholder, disable_a, render_page, open_html_in_browser
from SLGetLocalSoftware import get_local_software
from SLSoftwareInfo import software_info

_web_query_error = None

def web_query(url, selector):
    global _web_query_error

    try:
        _web_query_error = None
        r = requests.get(url, timeout=60)
    except Exception as e:
        _web_query_error = e
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
        result = [x for x in local_software.keys() if re.search(selector['Selector'], x)] # Should not use re.match()!
        return local_software[result[0]] if result else placeholder
    else:
        return '[Invalid Selector]'

def needs_update(current_version, newest_version):
    cv = current_version.strip()
    nv = newest_version.strip()
    return cv != nv or cv == placeholder

def check_update(local_software):
    global _web_query_error

    for item in json.loads(file_content('CheckUpdateList.json')):
        if item.get('Ignored'):
            continue

        name = item['Name']

        with cl.progress('Checking software: %s' % name, cl.PROGRESS_SPIN, color=cl.COLOR_NONE, mark='*') as p:
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
            if _web_query_error:
                p.stop()
                cl.error('Error: %s' % _web_query_error)
                _web_query_error = None

            result['ReleaseDate'] = date_sanitizer(web_query(cuu, rdd)) if rdd else placeholder
            if _web_query_error:
                p.stop()
                cl.error('Error: %s' % _web_query_error)
                _web_query_error = None

            if needs_update(result['CurrentVersion'], result['NewestVersion']):
                yield result

def main():
    cl.section('SoftwareList Update Check')

    with cl.progress('Querying local software information...', cl.PROGRESS_SPIN):
        local_software = get_local_software()

    update_list = list(check_update(local_software))
    if update_list:
        new_file = render_page('Update', update_list)
        open_html_in_browser(new_file)
    else:
        alert_messagebox('SoftwareList Update Checker', 'All the software in the list is up to date!')

if __name__ == '__main__':
    main()
