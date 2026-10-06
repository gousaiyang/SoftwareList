# -*- coding: utf-8 -*-

import json
import types

import pytest

from SLConfigReader import get_aapt_config, get_adb_config, get_all_themes, get_theme_config


def write_config(root, obj):
    (root / 'Config.json').write_text(json.dumps(obj), encoding='utf-8')


def test_get_all_themes_is_sorted(sandbox):
    assert get_all_themes() == ['blue', 'green', 'pink', 'purple']


def test_get_all_themes_ignores_non_json_and_directories(bare_sandbox):
    themes = bare_sandbox / 'themes'
    themes.mkdir()
    (themes / 'blue.json').write_text('{}', encoding='utf-8')
    (themes / 'notes.txt').write_text('x', encoding='utf-8')
    (themes / 'sub.json').mkdir()
    assert get_all_themes() == ['blue']


def test_get_all_themes_without_themes_dir_raises(bare_sandbox):
    with pytest.raises(FileNotFoundError):
        get_all_themes()


def test_theme_config_lowercases_the_value(sandbox):
    write_config(sandbox, {'theme': 'BLUE'})
    assert get_theme_config() == 'blue'


def test_theme_config_reads_the_configured_theme(sandbox):
    write_config(sandbox, {'theme': 'pink'})
    assert get_theme_config() == 'pink'


def test_theme_config_unknown_theme_falls_back_to_a_real_theme(sandbox):
    write_config(sandbox, {'theme': 'does-not-exist'})
    assert get_theme_config() in get_all_themes()


def test_theme_config_missing_file_falls_back(sandbox):
    assert get_theme_config() in get_all_themes()


def test_theme_config_malformed_json_falls_back(sandbox):
    (sandbox / 'Config.json').write_text('{not json', encoding='utf-8')
    assert get_theme_config() in get_all_themes()


def test_theme_config_non_string_theme_falls_back(sandbox):
    write_config(sandbox, {'theme': 42})
    assert get_theme_config() in get_all_themes()


def test_theme_config_random_returns_a_known_theme(sandbox):
    write_config(sandbox, {'theme': 'Random'})
    assert get_theme_config() in get_all_themes()


def test_theme_config_random_uses_random_choice(sandbox, monkeypatch):
    write_config(sandbox, {'theme': 'random'})
    monkeypatch.setattr('SLConfigReader.random', types.SimpleNamespace(choice=lambda seq: 'pink'))
    assert get_theme_config() == 'pink'


def test_theme_config_without_themes_raises_clear_error(bare_sandbox):
    """Regression: ``random.choice([])`` raised an opaque IndexError when no
    theme definitions were found."""
    with pytest.raises(FileNotFoundError) as excinfo:
        get_theme_config()
    assert 'theme' in str(excinfo.value)


def test_theme_config_is_resolved_from_the_script_dir_not_the_cwd(sandbox, tmp_path, monkeypatch):
    write_config(sandbox, {'theme': 'green'})
    monkeypatch.chdir(tmp_path)
    assert get_theme_config() == 'green'


def test_adb_config_valid(sandbox):
    write_config(sandbox, {'adb_exec': '/usr/bin/adb'})
    assert get_adb_config() == '/usr/bin/adb'


def test_adb_config_non_string_returns_none(sandbox):
    write_config(sandbox, {'adb_exec': 1})
    assert get_adb_config() is None


@pytest.mark.parametrize('payload', [{}, {'aapt_exec': 'x'}, {'adb_exec': None}])
def test_adb_config_missing_or_null_returns_none(sandbox, payload):
    write_config(sandbox, payload)
    assert get_adb_config() is None


def test_adb_config_without_file_returns_none(bare_sandbox):
    assert get_adb_config() is None


def test_aapt_config_valid(sandbox):
    write_config(sandbox, {'aapt_exec': '/data/local/tmp/aapt'})
    assert get_aapt_config() == '/data/local/tmp/aapt'


def test_aapt_config_non_string_returns_none(sandbox):
    write_config(sandbox, {'aapt_exec': ['aapt']})
    assert get_aapt_config() is None


def test_aapt_config_without_file_returns_none(bare_sandbox):
    assert get_aapt_config() is None


def test_adb_and_aapt_use_the_same_config_file(sandbox):
    write_config(sandbox, {'adb_exec': 'adb', 'aapt_exec': 'aapt'})
    assert (get_adb_config(), get_aapt_config()) == ('adb', 'aapt')
