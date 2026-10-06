# -*- coding: utf-8 -*-

import subprocess
import sys

import pytest


def test_write_file_creates_nested_directories(tmp_path):
    from SLHelper import file_content, write_file

    target = tmp_path / 'a' / 'b' / 'c.txt'
    write_file(str(target), 'hello ünïcode')
    assert target.read_text(encoding='utf-8') == 'hello ünïcode'
    assert file_content(str(target)) == 'hello ünïcode'


def test_file_content_reads_utf8(tmp_path):
    from SLHelper import file_content

    p = tmp_path / 'x.txt'
    p.write_text('z中文', encoding='utf-8')
    assert file_content(str(p)) == 'z中文'


@pytest.mark.parametrize('raw, expected', [
    ('2025-09-02', '2025-09-02'),
    ('2025/9/2', '2025-09-02'),
    ('2025.9.2', '2025-09-02'),
    ('2025 9 2', '2025-09-02'),
    ('Released 2025-9-2 build 42', '2025-09-02'),
    ('  2025-12-31  ', '2025-12-31'),
])
def test_date_sanitizer_normalizes(raw, expected):
    from SLHelper import date_sanitizer

    assert date_sanitizer(raw) == expected


@pytest.mark.parametrize('raw', ['no date here', '[Network Failure]', '[Parse Failure]', '--', ''])
def test_date_sanitizer_passthrough_when_no_match(raw):
    from SLHelper import date_sanitizer

    assert date_sanitizer(raw) == raw.strip()


def test_remove_prefix():
    from SLHelper import remove_prefix

    assert remove_prefix('Microsoft.PowerShell.Core\\Registry::HKLM:\\X', 'Microsoft.PowerShell.Core\\Registry::') == 'HKLM:\\X'
    assert remove_prefix('HKLM:\\X', 'HKCU:') == 'HKLM:\\X'


def test_lower_name_sorted_is_case_insensitive():
    from SLHelper import lower_name_sorted

    data = [{'Name': 'Zed'}, {'Name': 'apple'}, {'Name': 'Beta'}, {'Name': 'aardvark'}]
    assert [d['Name'] for d in lower_name_sorted(data)] == ['aardvark', 'apple', 'Beta', 'Zed']


def test_tkinter_is_not_imported_at_module_scope():
    """Importing the helpers must not require a GUI toolkit."""
    import SLHelper

    assert not hasattr(SLHelper, 'tkinter')
    assert not hasattr(SLHelper, 'messagebox')


def test_modules_import_on_a_headless_interpreter(project_root):
    """Regression: a top-level ``import tkinter`` made the modules unusable
    (and untestable) on machines without a GUI toolkit installed."""
    code = (
        "import sys; sys.modules['tkinter'] = None;"
        "import SLHelper, SLHTMLGeneration, SLCheckUpdate;"
        "print('imported ok')"
    )
    proc = subprocess.run([sys.executable, '-c', code], cwd=str(project_root),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', check=False)
    assert proc.returncode == 0, proc.stderr
    assert 'imported ok' in proc.stdout


def test_sl_path_is_absolute_and_inside_base_dir(sandbox):
    from SLHelper import sl_path

    path = sl_path('themes', 'blue.json')
    assert path == str(sandbox / 'themes' / 'blue.json')
    assert str(sandbox) in path


def test_sl_path_honours_repointed_base_dir(bare_sandbox, tmp_path, monkeypatch):
    import SLHelper

    assert SLHelper.sl_path('x') == str(bare_sandbox / 'x')
    monkeypatch.setattr(SLHelper, 'BASE_DIR', tmp_path)
    assert SLHelper.sl_path('x') == str(tmp_path / 'x')


def test_keep_window_open_prompts(monkeypatch):
    import SLHelper

    captured = {}

    def fake_input(msg):
        captured['msg'] = msg

    monkeypatch.setattr(SLHelper.cl, 'input', fake_input)
    SLHelper.keep_window_open()
    assert 'Press Enter' in captured['msg']


def test_exec_powershell_invokes_powershell(monkeypatch):
    import SLHelper

    seen = {}

    def fake_check_output(cmd, encoding=None):
        seen['cmd'] = cmd
        seen['encoding'] = encoding
        return 'ok'

    monkeypatch.setattr(SLHelper.subprocess, 'check_output', fake_check_output)
    assert SLHelper.exec_powershell('Get-Date') == 'ok'
    assert seen['cmd'] == ('powershell', 'Get-Date')
    assert seen['encoding'] == 'oem'


def test_alert_messagebox_uses_tkinter_lazily(monkeypatch):
    """The tkinter import must happen inside the function, not at import time."""
    import types

    import SLHelper

    root = type('Root', (), {'withdraw': lambda self: None, 'destroy': lambda self: None})()
    tk = types.ModuleType('tkinter')
    tk.Tk = lambda: root
    messagebox = types.ModuleType('tkinter.messagebox')
    shown = {}
    messagebox.showinfo = lambda title, content: shown.update(title=title, content=content)
    tk.messagebox = messagebox

    monkeypatch.setitem(sys.modules, 'tkinter', tk)
    monkeypatch.setitem(sys.modules, 'tkinter.messagebox', messagebox)
    SLHelper.alert_messagebox('T', 'C')
    assert shown == {'title': 'T', 'content': 'C'}
