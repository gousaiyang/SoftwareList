# -*- coding: utf-8 -*-
"""Structural validation of the software info database.

These tests are deliberately data-driven: they catch typos in the 50+ hand
maintained selector definitions (bad regexes, unknown selector types, URLs that
are missing or not HTTP) that would otherwise silently degrade to
``[Parse Failure]`` at runtime.
"""

import re

import pytest

from SLSoftwareInfo import software_info

ALL_NAMES = sorted(software_info)
DETECTION_KEYS = ('CurrentVersionDetection', 'NewestVersionDetection', 'ReleaseDateDetection')
URL_DETECTION_KEYS = ('NewestVersionDetection', 'ReleaseDateDetection')
KNOWN_REMOTE_TYPES = {'Regex', 'BeautifulSoup', 'BeautifulSoupWithRegex'}
KNOWN_LOCAL_TYPES = {'InName', 'InVersion'}


def test_database_is_not_empty():
    assert len(software_info) >= 40


@pytest.mark.parametrize('name', ALL_NAMES)
def test_name_is_a_non_empty_string(name):
    assert isinstance(name, str) and name.strip()


@pytest.mark.parametrize('name', ALL_NAMES)
def test_entry_is_a_mapping(name):
    assert isinstance(software_info[name], dict)


@pytest.mark.parametrize('name', ALL_NAMES)
def test_entry_declares_a_download_url(name):
    assert software_info[name].get('DownloadURL')


@pytest.mark.parametrize('name', ALL_NAMES)
def test_urls_use_http_or_https(name):
    info = software_info[name]
    for key in ('DownloadURL', 'CheckUpdateURL'):
        url = info.get(key)
        if url is not None:
            assert re.match(r'^https?://', url), f'{name}.{key} = {url!r}'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_entries_checked_online_declare_a_check_url(name):
    info = software_info[name]
    if any(key in info for key in URL_DETECTION_KEYS):
        assert info.get('CheckUpdateURL'), f'{name} needs a CheckUpdateURL'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_detection_types_are_known(name):
    info = software_info[name]
    for key in DETECTION_KEYS:
        detection = info.get(key)
        if detection is None:
            continue
        assert detection.get('Type') in KNOWN_REMOTE_TYPES | KNOWN_LOCAL_TYPES, f'{name}.{key}'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_current_version_detection_works_against_the_local_registry(name):
    detection = software_info[name].get('CurrentVersionDetection')
    if detection is not None:
        assert detection.get('Type') in KNOWN_LOCAL_TYPES, f'{name}.CurrentVersionDetection'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_regex_selectors_compile_and_capture(name):
    info = software_info[name]
    for key in DETECTION_KEYS:
        detection = info.get(key)
        if not detection or detection.get('Type') != 'Regex':
            continue
        pattern = re.compile(detection['Selector'])
        # ``web_query`` returns ``re.findall(...)[0]``, so more than one group
        # would yield a tuple instead of a version string.
        assert pattern.groups <= 1, f'{name}.{key} captures {pattern.groups} groups'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_beautifulsoup_with_regex_declares_both_parts(name):
    info = software_info[name]
    for key in DETECTION_KEYS:
        detection = info.get(key)
        if not detection or detection.get('Type') != 'BeautifulSoupWithRegex':
            continue
        assert detection.get('bs'), f'{name}.{key} is missing "bs"'
        assert detection.get('re'), f'{name}.{key} is missing "re"'
        assert re.compile(detection['re']).groups <= 1, f'{name}.{key}'


@pytest.mark.parametrize('name', ALL_NAMES)
def test_post_processing_hooks_are_callable(name):
    info = software_info[name]
    for key in ('CurrentVersionPostProcessing', 'NewestVersionPostProcessing'):
        hook = info.get(key)
        if hook is not None:
            assert callable(hook), f'{name}.{key}'


def test_post_processing_hook_example_behaves():
    # Python 3 has a post-processing hook that strips a trailing '.0'.
    hook = software_info['Python 3'].get('CurrentVersionPostProcessing')
    if hook is not None:
        assert hook('3.12.0') == '312'


def test_every_entry_with_a_check_url_has_a_newest_version_detection():
    for name, info in software_info.items():
        if info.get('NewestVersionDetection') is None:
            continue
        assert info.get('CheckUpdateURL'), name
