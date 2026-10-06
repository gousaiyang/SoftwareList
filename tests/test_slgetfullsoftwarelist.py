# -*- coding: utf-8 -*-

import json

import SLGetFullSoftwareList as mod
from SLGetFullSoftwareList import get_local_software_items
from SLHTMLGeneration import placeholder


def test_items_use_a_placeholder_for_missing_versions(monkeypatch):
    monkeypatch.setattr(mod, 'get_local_software', lambda: {'App A': '1.0', 'App B': None})
    assert list(get_local_software_items()) == [
        {'Name': 'App A', 'CurrentVersion': '1.0'},
        {'Name': 'App B', 'CurrentVersion': placeholder},
    ]


def test_items_for_an_empty_installation(monkeypatch):
    monkeypatch.setattr(mod, 'get_local_software', dict)
    assert list(get_local_software_items()) == []


def test_main_generates_the_full_page_sorted_by_name(sandbox, monkeypatch):
    (sandbox / 'Config.json').write_text(json.dumps({'theme': 'blue'}), encoding='utf-8')
    monkeypatch.setattr(mod, 'get_local_software', lambda: {'Zed': '1', 'alpha': '2'})
    opened = []
    monkeypatch.setattr(mod, 'open_html_in_browser', opened.append)

    mod.main()
    assert len(opened) == 1
    files = list((sandbox / 'output').glob('SoftwareList_Full_*.html'))
    assert len(files) == 1
    content = files[0].read_text(encoding='utf-8')
    assert content.index('<td>alpha</td>') < content.index('<td>Zed</td>')
