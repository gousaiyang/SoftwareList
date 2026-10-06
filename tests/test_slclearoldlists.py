# -*- coding: utf-8 -*-

import SLClearOldLists as mod
from SLClearOldLists import clear_old_lists, find_lists


def make_lists(root, names):
    output = root / 'output'
    output.mkdir(exist_ok=True)
    for name in names:
        (output / name).write_text('x', encoding='utf-8')
    return output


def test_find_lists_groups_by_page_and_sorts_oldest_first(tmp_path):
    make_lists(tmp_path, [
        'SoftwareList_Main_20250102000000.html',
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Full_20250101000000.html',
    ])
    groups = find_lists(str(tmp_path / 'output'))
    assert sorted(groups) == ['Full', 'Main']
    assert groups['Main'] == [
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Main_20250102000000.html',
    ]


def test_find_lists_ignores_unrelated_files(tmp_path):
    make_lists(tmp_path, [
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Main_backup.html',
        'SoftwareList_Main_202501010000.html',
        'SoftwareList_20250101000000.html',
        'notes.txt',
    ])
    groups = find_lists(str(tmp_path / 'output'))
    assert groups == {'Main': ['SoftwareList_Main_20250101000000.html']}


def test_find_lists_is_repeatable(tmp_path):
    """Regression: module-level accumulators made a second call double-count."""
    make_lists(tmp_path, ['SoftwareList_Main_20250101000000.html'])
    first = find_lists(str(tmp_path / 'output'))
    second = find_lists(str(tmp_path / 'output'))
    assert first == second


def test_clear_old_lists_keeps_only_the_newest_per_group(tmp_path):
    output = make_lists(tmp_path, [
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Main_20250102000000.html',
        'SoftwareList_Main_20250103000000.html',
        'SoftwareList_Full_20250101000000.html',
    ])
    deleted = clear_old_lists(str(output))
    assert sorted(deleted) == [
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Main_20250102000000.html',
    ]
    assert sorted(p.name for p in output.iterdir()) == [
        'SoftwareList_Full_20250101000000.html',
        'SoftwareList_Main_20250103000000.html',
    ]


def test_clear_old_lists_is_idempotent(tmp_path):
    output = make_lists(tmp_path, [
        'SoftwareList_Main_20250101000000.html',
        'SoftwareList_Main_20250102000000.html',
    ])
    assert clear_old_lists(str(output)) == ['SoftwareList_Main_20250101000000.html']
    assert clear_old_lists(str(output)) == []


def test_clear_old_lists_keeps_a_lone_list(tmp_path):
    output = make_lists(tmp_path, ['SoftwareList_Update_20250101000000.html'])
    assert clear_old_lists(str(output)) == []
    assert (output / 'SoftwareList_Update_20250101000000.html').is_file()


def test_clear_old_lists_on_an_empty_directory(tmp_path):
    (tmp_path / 'output').mkdir()
    assert clear_old_lists(str(tmp_path / 'output')) == []


def test_default_directory_is_the_script_directory(sandbox):
    (sandbox / 'output' / 'SoftwareList_Main_20250101000000.html').write_text('x', encoding='utf-8')
    (sandbox / 'output' / 'SoftwareList_Main_20250102000000.html').write_text('x', encoding='utf-8')
    assert clear_old_lists() == ['SoftwareList_Main_20250101000000.html']


def test_main_clears_old_lists(sandbox):
    (sandbox / 'output' / 'SoftwareList_Main_20250101000000.html').write_text('x', encoding='utf-8')
    (sandbox / 'output' / 'SoftwareList_Main_20250102000000.html').write_text('x', encoding='utf-8')
    mod.main()
    assert [p.name for p in (sandbox / 'output').iterdir()] == ['SoftwareList_Main_20250102000000.html']


def test_filename_pattern_is_anchored():
    assert mod.list_filename_pattern.match('SoftwareList_Main_20250101000000.html')
    assert not mod.list_filename_pattern.match('XSoftwareList_Main_20250101000000.html')
    assert not mod.list_filename_pattern.match('SoftwareList_Main_20250101000000.html.bak')
