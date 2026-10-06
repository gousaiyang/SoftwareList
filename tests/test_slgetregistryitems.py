# -*- coding: utf-8 -*-

import SLGetRegistryItems as mod
from SLGetRegistryItems import main

ITEMS = [
    {'DisplayName': 'Git', 'PSPath': 'Microsoft.PowerShell.Core\\Registry::HKLM:\\Software\\Git'},
    {'DisplayName': 'Google Chrome', 'PSPath': 'Microsoft.PowerShell.Core\\Registry::HKCU:\\Software\\Chrome'},
]


def run_main(monkeypatch, answers, items=ITEMS):
    messages = {'input': [], 'success': [], 'error': []}
    queue = list(answers)

    monkeypatch.setattr(mod, 'get_local_software_registry_items', lambda: iter([dict(i) for i in items]))
    monkeypatch.setattr(mod.cl, 'input', lambda msg: (messages['input'].append(msg), queue.pop(0))[1])
    monkeypatch.setattr(mod.cl, 'success', messages['success'].append)
    monkeypatch.setattr(mod.cl, 'error', messages['error'].append)
    main()
    return messages


def test_reports_matching_items_with_the_powershell_prefix_stripped(monkeypatch):
    messages = run_main(monkeypatch, ['git'])
    assert len(messages['success']) == 1
    report = messages['success'][0]
    assert 'Git' in report
    assert 'HKLM:\\Software\\Git' in report
    assert 'Microsoft.PowerShell.Core\\Registry::' not in report


def test_matching_is_case_insensitive(monkeypatch):
    messages = run_main(monkeypatch, ['CHROME'])
    assert 'Google Chrome' in messages['success'][0]


def test_empty_input_is_rejected_and_re_prompted(monkeypatch):
    messages = run_main(monkeypatch, ['', '   ', 'git'])
    assert len(messages['input']) == 3
    assert len(messages['success']) == 1


def test_unknown_keyword_is_reported(monkeypatch):
    messages = run_main(monkeypatch, ['does-not-exist'])
    assert messages['success'] == []
    assert messages['error'] == ['Registry item not found']


def test_matching_falls_back_to_an_empty_display_name(monkeypatch):
    messages = run_main(monkeypatch, ['x'], items=[{'PSPath': 'p'}])
    assert messages['error'] == ['Registry item not found']
