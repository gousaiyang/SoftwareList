# -*- coding: utf-8 -*-

import argparse
import itertools
import json
import re
import sys
import traceback

import colorlabels as cl
import requests
from bs4 import BeautifulSoup

from SLGetLocalSoftware import get_local_software
from SLHelper import (__version__, alert_messagebox, date_sanitizer, file_content, keep_window_open,
                      lower_name_sorted, sl_path)
from SLHTMLGeneration import (disable_a, open_html_in_browser, placeholder, render_page,
                              url_placeholder)
from SLSoftwareInfo import software_info

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'  # noqa: E501  # pylint: disable=line-too-long

_web_query_error = None


class _NullProgress:
    """No-op stand-in for a colorlabels progress label.

    Used in ``--json`` mode so that probe output never mixes with the JSON
    document written to stdout.
    """

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def stop(self):
        pass


def _null_progress(*args, **kwargs):  # pylint: disable=unused-argument
    return _NullProgress()


def web_query(url, selector):
    global _web_query_error  # pylint: disable=global-statement

    try:
        _web_query_error = None
        r = requests.get(url, timeout=60, headers={'User-Agent': USER_AGENT})
    except Exception as e:  # pylint: disable=broad-except
        _web_query_error = e
        return '[Network Failure]'
    else:
        if selector['Type'] == 'Regex':
            result = re.findall(selector['Selector'], r.text)
            return result[0] if result else '[Parse Failure]'
        if selector['Type'] == 'BeautifulSoup':
            soup = BeautifulSoup(r.text, 'html.parser')
            els = soup.select(selector['Selector'])
            if not els:
                return '[Parse Failure]'
            return els[0].string or '[Parse Failure]'
        if selector['Type'] == 'BeautifulSoupWithRegex':
            soup = BeautifulSoup(r.text, 'html.parser')
            els = soup.select(selector['bs'])
            if not els or not els[0].string:
                return '[Parse Failure]'
            result = re.findall(selector['re'], els[0].string)
            return result[0] if result else '[Parse Failure]'
        return '[Invalid Selector]'


def query_current_version(local_software, selector):
    if selector['Type'] == 'InName':
        result = list(itertools.chain(*(re.findall(selector['Selector'], x) for x in local_software.keys())))
        return result[0] if result else placeholder
    if selector['Type'] == 'InVersion':
        result = [x for x in local_software.keys() if re.search(selector['Selector'], x)]  # Should not use re.match()!
        return local_software[result[0]] if result else placeholder
    return '[Invalid Selector]'


def needs_update(current_version, newest_version):
    cv = current_version.strip()
    nv = newest_version.strip()
    return cv != nv or cv in {placeholder, '[Network Failure]', '[Parse Failure]', '[Invalid Selector]'}


def load_check_update_items(path=None):
    return json.loads(file_content(path or sl_path('CheckUpdateList.json')))


def find_unknown_software(items):
    """Return the configured names that have no entry in the software info database."""
    return [item['Name'] for item in items if not item.get('Ignored') and item['Name'] not in software_info]


def check_update(local_software, items=None, progress=None):
    global _web_query_error  # pylint: disable=global-statement

    if items is None:
        items = load_check_update_items()
    if progress is None:
        progress = cl.progress

    for item in items:
        if item.get('Ignored'):
            continue

        name = item['Name']

        with progress(f'Checking software: {name}', cl.PROGRESS_SPIN, color=cl.COLOR_NONE, mark='*') as p:
            result = {'Name': name, 'Priority': item.get('Priority', '')}

            info = software_info.get(name, {})
            cuu = info.get('CheckUpdateURL')
            cvd = info.get('CurrentVersionDetection')
            cvpp = info.get('CurrentVersionPostProcessing')
            nvd = info.get('NewestVersionDetection')
            nvpp = info.get('NewestVersionPostProcessing')
            rdd = info.get('ReleaseDateDetection')

            result['DownloadURL'] = info.get('DownloadURL', url_placeholder)
            result['DownloadAttribute'] = '' if 'DownloadURL' in info else disable_a
            result['CurrentVersion'] = query_current_version(local_software, cvd) if cvd else placeholder
            if cvpp:
                result['CurrentVersion'] = cvpp(result['CurrentVersion'])

            result['NewestVersion'] = web_query(cuu, nvd) if nvd else placeholder
            if nvpp:
                result['NewestVersion'] = nvpp(result['NewestVersion'])
            if _web_query_error:
                p.stop()
                print(f'Error: {_web_query_error}', file=sys.stderr)
                _web_query_error = None

            result['ReleaseDate'] = date_sanitizer(web_query(cuu, rdd)) if rdd else placeholder
            if _web_query_error:
                p.stop()
                print(f'Error: {_web_query_error}', file=sys.stderr)
                _web_query_error = None

            if needs_update(result['CurrentVersion'], result['NewestVersion']):
                yield result


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog='SLCheckUpdate',
        description='Check the software in CheckUpdateList.json for available updates.')
    parser.add_argument('--list', metavar='PATH',
                        help='path to the check-update list (default: CheckUpdateList.json in the project directory)')
    parser.add_argument('--json', action='store_true',
                        help='write the pending updates as JSON to stdout (implies --no-open)')
    parser.add_argument('--no-open', action='store_true',
                        help='generate the HTML list but do not open it in a browser')
    parser.add_argument('--validate', action='store_true',
                        help='only report configured names missing from the software info database, then exit')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    items = load_check_update_items(args.list)

    if args.validate:
        unknown = find_unknown_software(items)
        if unknown:
            print(f'Unknown software ({len(unknown)}):', file=sys.stderr)
            for name in unknown:
                print(f'  - {name}', file=sys.stderr)
            return 1
        print('All configured software names are known.')
        return 0

    if not args.json:
        cl.section('SoftwareList Update Check')

    progress = _null_progress if args.json else cl.progress

    with progress('Querying local software information...', cl.PROGRESS_SPIN):
        local_software = get_local_software()

    update_list = lower_name_sorted(check_update(local_software, items, progress))

    if args.json:
        json.dump(update_list, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
        return 0

    if update_list:
        new_file = render_page('Update', update_list)
        if args.no_open:
            cl.info(f'Generated {new_file}')
        else:
            open_html_in_browser(new_file)
    else:
        alert_messagebox('SoftwareList Update Checker', 'All the software in the list is up to date!')

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
        sys.exit(1)
