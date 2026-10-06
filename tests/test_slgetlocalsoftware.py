# -*- coding: utf-8 -*-

import json

import SLGetLocalSoftware as mod
from SLGetLocalSoftware import get_local_software, get_local_software_registry_items, registry_locations


def make_powershell(routes, default=''):
    calls = []

    def run(command):
        calls.append(command)
        for needle, output in routes.items():
            if needle in command:
                return output
        return default

    run.calls = calls
    return run


def test_all_three_registry_locations_are_queried(monkeypatch):
    fake = make_powershell({}, json.dumps([]))
    monkeypatch.setattr(mod, 'exec_powershell', fake)
    list(get_local_software_registry_items())
    assert len(registry_locations) == 3
    for location in registry_locations:
        assert any(location in command for command in fake.calls)


def test_items_from_every_location_are_yielded(monkeypatch):
    routes = {
        'Wow6432Node': json.dumps([{'DisplayName': 'WowApp', 'DisplayVersion': '1.0'}]),
        'HKCU': json.dumps([{'DisplayName': 'UserApp', 'DisplayVersion': '2.0'}]),
    }
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell(routes, json.dumps([])))
    names = [item['DisplayName'] for item in get_local_software_registry_items()]
    assert names == ['WowApp', 'UserApp']


def test_single_object_output_is_yielded_as_one_item(monkeypatch):
    """PowerShell's ConvertTo-Json emits a bare object when there is one match."""
    monkeypatch.setattr(mod, 'exec_powershell',
                        make_powershell({'Wow6432Node': json.dumps({'DisplayName': 'Only', 'DisplayVersion': '1'})},
                                        json.dumps([])))
    items = [item['DisplayName'] for item in get_local_software_registry_items()]
    assert items == ['Only']


def test_empty_output_is_not_an_error(monkeypatch):
    """Regression: ``json.loads('')`` used to raise when a registry hive held
    no uninstall entries (e.g. the Wow6432Node key on a 32-bit-only system)."""
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell({}, ''))
    assert list(get_local_software_registry_items()) == []


def test_whitespace_only_output_is_not_an_error(monkeypatch):
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell({}, '  \r\n '))
    assert list(get_local_software_registry_items()) == []


def test_malformed_json_is_reported_and_skipped(monkeypatch):
    errors = []
    monkeypatch.setattr(mod.cl, 'error', errors.append)
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell({'Wow6432Node': '{not json'}, ''))
    assert list(get_local_software_registry_items()) == []
    assert len(errors) == 1
    assert 'Wow6432Node' in errors[0]


def test_get_local_software_maps_display_name_to_version(monkeypatch):
    payload = json.dumps([
        {'DisplayName': 'App A', 'DisplayVersion': '1.2.3'},
        {'DisplayName': 'App B'},
        {'DisplayVersion': '9.9'},
        'not-a-dict',
    ])
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell({'Wow6432Node': payload}, ''))
    assert get_local_software() == {'App A': '1.2.3', 'App B': None}


def test_get_local_software_ignores_the_cwd(monkeypatch, tmp_path):
    payload = json.dumps([{'DisplayName': 'App', 'DisplayVersion': '1'}])
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell({'HKCU': payload}, ''))
    monkeypatch.chdir(tmp_path)
    assert get_local_software() == {'App': '1'}


def test_later_locations_do_not_shadow_earlier_versions(monkeypatch):
    routes = {
        'Wow6432Node': json.dumps([{'DisplayName': 'Dup', 'DisplayVersion': 'old'}]),
        'HKCU': json.dumps([{'DisplayName': 'Dup', 'DisplayVersion': 'new'}]),
    }
    monkeypatch.setattr(mod, 'exec_powershell', make_powershell(routes, ''))
    assert get_local_software() == {'Dup': 'new'}
