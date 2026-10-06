# -*- coding: utf-8 -*-

import json

import SLGenerateMainSoftwareList as mod
from SLGenerateMainSoftwareList import get_main_software
from SLHTMLGeneration import disable_a, url_placeholder


def test_get_main_software_builds_download_fields(monkeypatch):
    monkeypatch.setattr(mod, 'software_info', {'Git': {'DownloadURL': 'https://git-scm.com/'}})
    items = [{'Name': 'Git', 'Priority': 4}, {'Name': 'Unknown'}]
    assert list(get_main_software(items)) == [
        {'Name': 'Git', 'Priority': 4, 'DownloadURL': 'https://git-scm.com/', 'DownloadAttribute': ''},
        {'Name': 'Unknown', 'Priority': '', 'DownloadURL': url_placeholder, 'DownloadAttribute': disable_a},
    ]


def test_get_main_software_defaults_priority_to_an_empty_string(monkeypatch):
    monkeypatch.setattr(mod, 'software_info', {'Git': {'DownloadURL': 'https://git-scm.com/'}})
    assert list(get_main_software([{'Name': 'Git'}]))[0]['Priority'] == ''


def test_get_main_software_reads_the_list_from_the_script_dir(sandbox, monkeypatch):
    (sandbox / 'MainSoftwareList.json').write_text(json.dumps([{'Name': 'Git'}]), encoding='utf-8')
    monkeypatch.setattr(mod, 'software_info', {'Git': {'DownloadURL': 'https://git-scm.com/'}})
    assert [item['Name'] for item in get_main_software()] == ['Git']


def test_get_main_software_reads_the_list_from_the_script_dir_not_the_cwd(sandbox, tmp_path, monkeypatch):
    (sandbox / 'MainSoftwareList.json').write_text(json.dumps([{'Name': 'Git'}]), encoding='utf-8')
    monkeypatch.setattr(mod, 'software_info', {'Git': {'DownloadURL': 'https://git-scm.com/'}})
    monkeypatch.chdir(tmp_path)
    assert [item['Name'] for item in get_main_software()] == ['Git']


def test_main_generates_the_main_page(sandbox, monkeypatch):
    (sandbox / 'MainSoftwareList.json').write_text(
        json.dumps([{'Name': 'Git', 'Priority': 1}]), encoding='utf-8')
    (sandbox / 'Config.json').write_text(json.dumps({'theme': 'blue'}), encoding='utf-8')
    monkeypatch.setattr(mod, 'software_info', {'Git': {'DownloadURL': 'https://git-scm.com/'}})
    opened = []
    monkeypatch.setattr(mod, 'open_html_in_browser', opened.append)

    mod.main()
    assert len(opened) == 1
    generated = (sandbox / 'output').glob('SoftwareList_Main_*.html')
    assert len(list(generated)) == 1
