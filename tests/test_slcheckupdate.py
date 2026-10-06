# -*- coding: utf-8 -*-

import json

import pytest

import SLCheckUpdate
from SLHTMLGeneration import disable_a, placeholder, url_placeholder
from SLCheckUpdate import (check_update, find_unknown_software, load_check_update_items,
                           needs_update, parse_args, query_current_version, web_query)

LOCAL = {
    'Git version 2.44.0': '2.44.0',
    'Vim 9.1': '9.1',
    'Post 0.9': '0.9',
}

SOFTWARE_INFO = {
    'Git': {
        'DownloadURL': 'https://git-scm.com/download/win',
        'CheckUpdateURL': 'https://git-scm.com/',
        'CurrentVersionDetection': {'Type': 'InName', 'Selector': r'Git version ([\d.]+)'},
        'NewestVersionDetection': {'Type': 'Regex', 'Selector': r'Latest: ([\d.]+)'},
        'ReleaseDateDetection': {'Type': 'Regex', 'Selector': r'Released ([\d-]+)'},
    },
    'Vim': {
        'DownloadURL': 'https://vim.org/',
        'CheckUpdateURL': 'https://vim.org/',
        'CurrentVersionDetection': {'Type': 'InVersion', 'Selector': r'Vim'},
    },
    'Post': {
        'CheckUpdateURL': 'https://post/',
        'CurrentVersionDetection': {'Type': 'InName', 'Selector': r'Post ([\d.]+)'},
        'NewestVersionDetection': {'Type': 'Regex', 'Selector': r'v([\d.]+)'},
        'NewestVersionPostProcessing': lambda v: v.replace('.', ''),
    },
}

ROUTES = {
    'https://git-scm.com/': 'Latest: 2.50.0\nReleased 2024-05-01\n',
    'https://vim.org/': 'vim 9.2',
    'https://post/': 'v1.2.3',
}


@pytest.fixture(autouse=True)
def reset_web_query_error():
    SLCheckUpdate._web_query_error = None
    yield
    SLCheckUpdate._web_query_error = None


@pytest.fixture
def iso(monkeypatch, fake_requests):
    """Isolated software database + fake HTTP layer."""
    monkeypatch.setattr(SLCheckUpdate, 'software_info', SOFTWARE_INFO)
    fake = fake_requests(dict(ROUTES))
    monkeypatch.setattr(SLCheckUpdate, 'requests', fake)
    return fake


class RecordingProgress:
    def __init__(self, log, message):
        self.log = log
        self.message = message
        log.append(message)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def stop(self):
        self.log.append('stop')


# ---------------------------------------------------------------- needs_update

@pytest.mark.parametrize('cv, nv, expected', [
    ('1.0', '2.0', True),
    ('2.0', '2.0', False),
    (' 2.0 ', '2.0', False),
    (placeholder, '2.0', True),
    (placeholder, placeholder, True),
    ('[Network Failure]', '[Network Failure]', True),
    ('[Parse Failure]', '[Parse Failure]', True),
    ('[Invalid Selector]', '[Invalid Selector]', True),
    ('1.0', placeholder, True),
])
def test_needs_update(cv, nv, expected):
    assert needs_update(cv, nv) is expected


# ------------------------------------------------------ query_current_version

def test_query_current_version_in_name_extracts_the_version():
    selector = {'Type': 'InName', 'Selector': r'Git version ([\d.]+)'}
    assert query_current_version(LOCAL, selector) == '2.44.0'


def test_query_current_version_in_name_without_match_uses_placeholder():
    selector = {'Type': 'InName', 'Selector': r'Svn ([\d.]+)'}
    assert query_current_version(LOCAL, selector) == placeholder


def test_query_current_version_in_version_returns_the_registry_value():
    selector = {'Type': 'InVersion', 'Selector': r'Vim'}
    assert query_current_version(LOCAL, selector) == '9.1'


def test_query_current_version_in_version_searches_not_just_the_prefix():
    # The selector must be applied with re.search(), not re.match().
    selector = {'Type': 'InVersion', 'Selector': r'version'}
    assert query_current_version(LOCAL, selector) == '2.44.0'


def test_query_current_version_in_version_without_match_uses_placeholder():
    selector = {'Type': 'InVersion', 'Selector': r'Emacs'}
    assert query_current_version(LOCAL, selector) == placeholder


def test_query_current_version_unknown_type():
    assert query_current_version(LOCAL, {'Type': 'Whatever', 'Selector': 'x'}) == '[Invalid Selector]'


# ------------------------------------------------------------------ web_query

def test_web_query_regex(iso):
    selector = {'Type': 'Regex', 'Selector': r'Latest: ([\d.]+)'}
    assert web_query('https://git-scm.com/', selector) == '2.50.0'


def test_web_query_regex_without_match(iso):
    selector = {'Type': 'Regex', 'Selector': r'Nothing: ([\d.]+)'}
    assert web_query('https://git-scm.com/', selector) == '[Parse Failure]'


def test_web_query_beautifulsoup(iso):
    selector = {'Type': 'BeautifulSoup', 'Selector': 'b'}
    assert web_query('https://git-scm.com/', selector) == '[Parse Failure]'
    iso.mapping['https://git-scm.com/'] = '<html><b>9.9</b></html>'
    assert web_query('https://git-scm.com/', selector) == '9.9'


def test_web_query_beautifulsoup_without_match(iso):
    selector = {'Type': 'BeautifulSoup', 'Selector': 'i'}
    assert web_query('https://git-scm.com/', selector) == '[Parse Failure]'


def test_web_query_beautifulsoup_with_regex(iso):
    iso.mapping['https://git-scm.com/'] = '<html><b>version 7.7.7</b></html>'
    selector = {'Type': 'BeautifulSoupWithRegex', 'bs': 'b', 're': r'version ([\d.]+)'}
    assert web_query('https://git-scm.com/', selector) == '7.7.7'


def test_web_query_beautifulsoup_with_regex_without_match(iso):
    iso.mapping['https://git-scm.com/'] = '<html><b>nothing</b></html>'
    selector = {'Type': 'BeautifulSoupWithRegex', 'bs': 'b', 're': r'version ([\d.]+)'}
    assert web_query('https://git-scm.com/', selector) == '[Parse Failure]'


def test_web_query_unknown_selector_type(iso):
    assert web_query('https://git-scm.com/', {'Type': 'Nope'}) == '[Invalid Selector]'


def test_web_query_reports_network_failure(iso):
    assert web_query('https://unreachable/', {'Type': 'Regex', 'Selector': 'x'}) == '[Network Failure]'
    assert isinstance(SLCheckUpdate._web_query_error, Exception)


def test_web_query_sends_a_user_agent_with_a_timeout(iso):
    web_query('https://git-scm.com/', {'Type': 'Regex', 'Selector': r'Latest: ([\d.]+)'})
    call = iso.calls[-1]
    assert call['timeout'] == 60
    assert 'User-Agent' in call['headers']


# -------------------------------------------------------------- list loading

def test_load_check_update_items_from_the_script_dir(sandbox):
    (sandbox / 'CheckUpdateList.json').write_text(json.dumps([{'Name': 'Git'}]), encoding='utf-8')
    assert load_check_update_items() == [{'Name': 'Git'}]


def test_load_check_update_items_from_an_explicit_path(tmp_path):
    path = tmp_path / 'list.json'
    path.write_text(json.dumps([{'Name': 'Vim'}]), encoding='utf-8')
    assert load_check_update_items(str(path)) == [{'Name': 'Vim'}]


def test_load_check_update_items_ignores_the_working_directory(sandbox, tmp_path, monkeypatch):
    (sandbox / 'CheckUpdateList.json').write_text(json.dumps([{'Name': 'Git'}]), encoding='utf-8')
    monkeypatch.chdir(tmp_path)
    assert load_check_update_items() == [{'Name': 'Git'}]


# ----------------------------------------------------------- find_unknown_sw

def test_find_unknown_software(iso):
    items = [{'Name': 'Git'}, {'Name': 'Nope'}, {'Name': 'Vim'}]
    assert find_unknown_software(items) == ['Nope']


def test_find_unknown_software_skips_ignored_entries(iso):
    items = [{'Name': 'Nope', 'Ignored': True}, {'Name': 'AlsoNope'}]
    assert find_unknown_software(items) == ['AlsoNope']


# -------------------------------------------------------------- check_update

def test_check_update_yields_only_software_that_needs_an_update(iso):
    items = [{'Name': 'Git', 'Priority': 4}, {'Name': 'Vim'}]
    results = list(check_update(LOCAL, items, progress=SLCheckUpdate._null_progress))
    assert [r['Name'] for r in results] == ['Git', 'Vim']


def test_check_update_result_has_every_field_the_template_needs(iso):
    items = [{'Name': 'Git', 'Priority': 4}]
    result = list(check_update(LOCAL, items, progress=SLCheckUpdate._null_progress))[0]
    assert result == {
        'Name': 'Git',
        'Priority': 4,
        'DownloadURL': 'https://git-scm.com/download/win',
        'DownloadAttribute': '',
        'CurrentVersion': '2.44.0',
        'NewestVersion': '2.50.0',
        'ReleaseDate': '2024-05-01',
    }


def test_check_update_omits_up_to_date_software(iso):
    iso.mapping['https://git-scm.com/'] = 'Latest: 2.44.0\nReleased 2024-05-01\n'
    items = [{'Name': 'Git'}]
    assert list(check_update({'Git version 2.44.0': '2.44.0'}, items,
                             progress=SLCheckUpdate._null_progress)) == []


def test_check_update_skips_ignored_entries(iso):
    items = [{'Name': 'Git', 'Ignored': True}]
    assert list(check_update(LOCAL, items, progress=SLCheckUpdate._null_progress)) == []


def test_check_update_default_priority_is_an_empty_string(iso):
    result = list(check_update(LOCAL, [{'Name': 'Git'}], progress=SLCheckUpdate._null_progress))[0]
    assert result['Priority'] == ''


def test_check_update_disables_download_button_for_untracked_software(iso):
    result = list(check_update(LOCAL, [{'Name': 'Post'}], progress=SLCheckUpdate._null_progress))[0]
    assert result['DownloadURL'] == url_placeholder
    assert result['DownloadAttribute'] == disable_a


def test_check_update_applies_newest_version_post_processing(iso):
    result = list(check_update(LOCAL, [{'Name': 'Post'}], progress=SLCheckUpdate._null_progress))[0]
    assert result['NewestVersion'] == '123'


def test_check_update_uses_the_placeholder_when_there_is_no_newest_detection(iso):
    result = list(check_update(LOCAL, [{'Name': 'Vim'}], progress=SLCheckUpdate._null_progress))[0]
    assert result['NewestVersion'] == placeholder
    assert result['ReleaseDate'] == placeholder


def test_check_update_handles_a_name_missing_from_the_database(iso):
    result = list(check_update(LOCAL, [{'Name': 'Mystery'}], progress=SLCheckUpdate._null_progress))[0]
    assert result['CurrentVersion'] == placeholder
    assert result['NewestVersion'] == placeholder
    assert result['DownloadAttribute'] == disable_a


def test_check_update_reports_network_errors_on_stderr_only(iso, capsys):
    iso.mapping.pop('https://git-scm.com/')
    results = list(check_update(LOCAL, [{'Name': 'Git'}], progress=SLCheckUpdate._null_progress))
    # Git still lands in the list (current version is known, newest is not).
    assert results[0]['NewestVersion'] == '[Network Failure]'
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'Error:' in captured.err


def test_check_update_stops_the_progress_label_on_error(iso, capsys):
    iso.mapping.pop('https://git-scm.com/')
    log = []
    progress = lambda msg, *a, **k: RecordingProgress(log, msg)  # noqa: E731
    list(check_update(LOCAL, [{'Name': 'Git'}], progress=progress))
    assert 'stop' in log
    capsys.readouterr()


def test_check_update_loads_the_list_itself_when_not_given_one(sandbox, iso):
    (sandbox / 'CheckUpdateList.json').write_text(json.dumps([{'Name': 'Git'}]), encoding='utf-8')
    results = list(check_update(LOCAL, progress=SLCheckUpdate._null_progress))
    assert [r['Name'] for r in results] == ['Git']


# ------------------------------------------------------------------- parse_args

def test_parse_args_defaults():
    args = parse_args([])
    assert (args.json, args.no_open, args.validate, args.list) == (False, False, False, None)


def test_parse_args_flags():
    args = parse_args(['--json', '--no-open', '--list', 'x.json'])
    assert (args.json, args.no_open, args.list) == (True, True, 'x.json')


def test_parse_args_rejects_unknown_options():
    with pytest.raises(SystemExit) as excinfo:
        parse_args(['--nope'])
    assert excinfo.value.code == 2


def test_parse_args_version_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as excinfo:
        parse_args(['--version'])
    assert excinfo.value.code == 0
    assert 'SLCheckUpdate' in capsys.readouterr().out


# ------------------------------------------------------------------------ main

def write_list(root, items, name='CheckUpdateList.json'):
    path = root / name
    path.write_text(json.dumps(items), encoding='utf-8')
    return str(path)


def pin_theme(root, theme='blue'):
    (root / 'Config.json').write_text(json.dumps({'theme': theme}), encoding='utf-8')


def test_main_validate_reports_unknown_names(sandbox, iso, capsys):
    path = write_list(sandbox, [{'Name': 'Git'}, {'Name': 'Nope'}])
    code = SLCheckUpdate.main(['--validate', '--list', path])
    captured = capsys.readouterr()
    assert code == 1
    assert 'Nope' in captured.err
    assert 'Git' not in captured.err


def test_main_validate_returns_zero_when_everything_is_known(sandbox, iso, capsys):
    path = write_list(sandbox, [{'Name': 'Git'}, {'Name': 'Vim'}])
    assert SLCheckUpdate.main(['--validate', '--list', path]) == 0
    assert 'All configured software names are known.' in capsys.readouterr().out


def test_main_json_prints_a_parseable_document(sandbox, iso, monkeypatch, capsys):
    path = write_list(sandbox, [{'Name': 'Git', 'Priority': 4}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: LOCAL)
    opened = []
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', opened.append)

    assert SLCheckUpdate.main(['--json', '--list', path]) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert [r['Name'] for r in payload] == ['Git']
    assert captured.out.count('Checking software') == 0
    assert opened == []


def test_main_json_prints_an_empty_array_when_up_to_date(sandbox, iso, monkeypatch, capsys):
    iso.mapping['https://git-scm.com/'] = 'Latest: 2.44.0\nReleased 2024-05-01\n'
    path = write_list(sandbox, [{'Name': 'Git'}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: {'Git version 2.44.0': '2.44.0'})

    assert SLCheckUpdate.main(['--json', '--list', path]) == 0
    assert json.loads(capsys.readouterr().out) == []


def test_main_no_open_generates_the_page_without_a_browser(sandbox, iso, monkeypatch, capsys):
    pin_theme(sandbox)
    path = write_list(sandbox, [{'Name': 'Git'}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: LOCAL)
    opened = []
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', opened.append)

    assert SLCheckUpdate.main(['--no-open', '--list', path]) == 0
    assert opened == []
    assert list((sandbox / 'output').glob('SoftwareList_Update_*.html'))
    assert 'Generated' in capsys.readouterr().out


def test_main_opens_the_browser_when_updates_exist(sandbox, iso, monkeypatch):
    pin_theme(sandbox)
    path = write_list(sandbox, [{'Name': 'Git'}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: LOCAL)
    opened = []
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', opened.append)

    assert SLCheckUpdate.main(['--list', path]) == 0
    assert len(opened) == 1
    assert 'file:' in opened[0]


def test_main_shows_a_message_box_when_everything_is_up_to_date(sandbox, iso, monkeypatch):
    pin_theme(sandbox)
    iso.mapping['https://git-scm.com/'] = 'Latest: 2.44.0\nReleased 2024-05-01\n'
    path = write_list(sandbox, [{'Name': 'Git'}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: {'Git version 2.44.0': '2.44.0'})

    shown = []
    monkeypatch.setattr(SLCheckUpdate, 'alert_messagebox', lambda t, c: shown.append((t, c)))
    opened = []
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', opened.append)

    assert SLCheckUpdate.main(['--list', path]) == 0
    assert len(shown) == 1
    assert 'up to date' in shown[0][1]
    assert opened == []


def test_main_uses_the_real_progress_label_outside_json_mode(sandbox, iso, monkeypatch, capsys):
    pin_theme(sandbox)
    path = write_list(sandbox, [{'Name': 'Git'}])
    monkeypatch.setattr(SLCheckUpdate, 'get_local_software', lambda: LOCAL)
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', lambda url: None)

    log = []

    def fake_progress(msg, mode=0, **kwargs):
        return RecordingProgress(log, msg)

    monkeypatch.setattr(SLCheckUpdate.cl, 'progress', fake_progress)
    SLCheckUpdate.main(['--no-open', '--list', path])
    assert any('Checking software: Git' in m for m in log)
    assert any('Querying local software' in m for m in log)
