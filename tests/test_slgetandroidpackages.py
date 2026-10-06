# -*- coding: utf-8 -*-

import pytest

import SLGetAndroidPackages as mod
from SLGetAndroidPackages import check_android_device, check_config, get_all_android_apps

LISTING = (
    'package:/data/app/com.example.alpha/base.apk=com.example.alpha\n'
    'package:/data/app/com.example.beta/base.apk=com.example.beta\n'
)

BADGING = {
    '/data/app/com.example.alpha/base.apk': "package: name='com.example.alpha'\napplication-label:'Alpha'\nversionName='1.2.3'\n",
    '/data/app/com.example.beta/base.apk': "package: name='com.example.beta'\napplication-label:'Beta'\n",
}


class Completed:
    def __init__(self, stdout):
        self.stdout = stdout


def install(monkeypatch, listing, badging=None, warnings=None):
    badging = BADGING if badging is None else badging
    monkeypatch.setattr(mod.subprocess, 'check_output', lambda *a, **k: listing)
    monkeypatch.setattr(mod.subprocess, 'run',
                        lambda args, **kwargs: Completed(badging.get(args[-1], '')))
    if warnings is not None:
        monkeypatch.setattr(mod.cl, 'warning', warnings.append)


def test_parses_label_package_and_version(monkeypatch):
    install(monkeypatch, LISTING)
    assert list(get_all_android_apps()) == [
        ('Alpha', 'com.example.alpha', '1.2.3'),
        ('Beta', 'com.example.beta', None),
    ]


def test_app_without_a_label_is_skipped(monkeypatch):
    listing = 'package:/x/base.apk=com.skipped\n'
    install(monkeypatch, listing, badging={'/x/base.apk': "package: name='com.skipped'\n"})
    assert list(get_all_android_apps()) == []


def test_missing_version_name_yields_none(monkeypatch):
    listing = 'package:/x/base.apk=com.noversion\n'
    install(monkeypatch, listing, badging={'/x/base.apk': "application-label:'NoVersion'\n"})
    assert list(get_all_android_apps()) == [('NoVersion', 'com.noversion', None)]


def test_unrecognized_lines_are_skipped_instead_of_crashing(monkeypatch):
    """Regression: a line without the `package:` prefix raised IndexError from
    ``re.findall(...)[0]`` and aborted the whole listing."""
    warnings = []
    listing = 'garbage line\n' + LISTING
    install(monkeypatch, listing, warnings=warnings)
    assert [entry[1] for entry in get_all_android_apps()] == ['com.example.alpha', 'com.example.beta']
    assert warnings == ['Skipping unrecognized package listing: garbage line']


def test_empty_lines_are_ignored(monkeypatch):
    warnings = []
    install(monkeypatch, '\n\n' + LISTING + '\n\n', warnings=warnings)
    assert len(list(get_all_android_apps())) == 2
    assert warnings == []


def test_packages_without_an_equals_sign_are_skipped(monkeypatch):
    warnings = []
    install(monkeypatch, 'package:/data/app/broken/base.apk\n', warnings=warnings)
    assert list(get_all_android_apps()) == []
    assert len(warnings) == 1


def test_paths_containing_equals_split_on_the_last_equals(monkeypatch):
    """Android stores apps under paths such as ``/data/app/~~Ab==/app==/base.apk``."""
    listing = 'package:/data/app/~~Ab==/com.example.gamma-1x==/base.apk=com.example.gamma\n'
    install(monkeypatch, listing, badging={'/data/app/~~Ab==/com.example.gamma-1x==/base.apk':
                                           "application-label:'Gamma'\nversionName='3.0'\n"})
    assert list(get_all_android_apps()) == [('Gamma', 'com.example.gamma', '3.0')]


def test_check_config_rejects_a_missing_adb_path(monkeypatch):
    errors = []
    monkeypatch.setattr(mod, 'adb_exec', None)
    monkeypatch.setattr(mod, 'aapt_exec', 'aapt')
    monkeypatch.setattr(mod.cl, 'error', errors.append)
    monkeypatch.setattr(mod, 'keep_window_open', lambda: None)
    with pytest.raises(SystemExit):
        check_config()
    assert 'adb' in errors[0]


def test_check_config_rejects_a_missing_aapt_path(monkeypatch):
    errors = []
    monkeypatch.setattr(mod, 'adb_exec', 'adb')
    monkeypatch.setattr(mod, 'aapt_exec', None)
    monkeypatch.setattr(mod.cl, 'error', errors.append)
    monkeypatch.setattr(mod, 'keep_window_open', lambda: None)
    with pytest.raises(SystemExit):
        check_config()
    assert 'aapt' in errors[0]


def test_check_config_accepts_a_complete_config(monkeypatch):
    monkeypatch.setattr(mod, 'adb_exec', 'adb')
    monkeypatch.setattr(mod, 'aapt_exec', 'aapt')
    check_config()


def test_check_android_device_requires_a_connected_device(monkeypatch):
    errors = []
    monkeypatch.setattr(mod.subprocess, 'call', lambda *a, **k: 1)
    monkeypatch.setattr(mod.cl, 'error', errors.append)
    monkeypatch.setattr(mod, 'keep_window_open', lambda: None)
    with pytest.raises(SystemExit):
        check_android_device()
    assert 'no Android device' in errors[0]


def test_check_android_device_passes_when_adb_succeeds(monkeypatch):
    monkeypatch.setattr(mod.subprocess, 'call', lambda *a, **k: 0)
    check_android_device()
