# -*- coding: utf-8 -*-

import json
import os
import re
import shutil

import pytest

from SLHTMLGeneration import (CDN_URLs, open_html_in_browser, render_page, render_template)

MAIN_ITEM = {
    'Name': 'Git',
    'Priority': 4,
    'DownloadURL': 'https://git-scm.com/download/win',
    'DownloadAttribute': '',
}


def pin_theme(root, theme='blue'):
    (root / 'Config.json').write_text(json.dumps({'theme': theme}), encoding='utf-8')


def test_render_template_escapes_by_default():
    out = render_template('{{Name}}', {'Name': '<b>a</b> & "quoted"'})
    assert out == '&lt;b&gt;a&lt;/b&gt; &amp; &quot;quoted&quot;'


def test_render_template_escapes_single_quotes():
    assert render_template('{{x}}', {'x': "it's"}) == 'it&#x27;s'


def test_render_template_without_escaping():
    assert render_template('{{x}}', {'x': '<b>'}, escape_html=False) == '<b>'


def test_render_template_replaces_every_occurrence():
    assert render_template('{{x}}-{{x}}-{{x}}', {'x': 'v'}) == 'v-v-v'


def test_render_template_converts_values_to_string():
    assert render_template('{{n}}', {'n': 42}) == '42'


def test_render_template_leaves_unknown_placeholders():
    assert render_template('{{a}} {{b}}', {'a': '1'}) == '1 {{b}}'


@pytest.mark.parametrize('name', ['has space', 'has/slash', 'a.b', '', '..', 'a$b'])
def test_render_page_rejects_invalid_page_names(sandbox, name):
    with pytest.raises(ValueError):
        render_page(name, [])


def test_render_page_rejects_unknown_template(sandbox):
    pin_theme(sandbox)
    with pytest.raises(NameError):
        render_page('Nope', [])


def test_render_page_creates_file_inside_output_dir(sandbox):
    pin_theme(sandbox)
    filename = render_page('Main', [MAIN_ITEM])
    assert filename.startswith(str(sandbox / 'output'))
    assert os.path.isfile(filename)


def test_render_page_filename_encodes_page_and_timestamp(sandbox):
    pin_theme(sandbox)
    filename = render_page('Main', [MAIN_ITEM])
    assert re.fullmatch(r'SoftwareList_Main_\d{14}\.html', os.path.basename(filename))


def test_render_page_substitutes_every_placeholder(sandbox):
    pin_theme(sandbox)
    content = open(render_page('Main', [MAIN_ITEM]), encoding='utf-8').read()
    assert '{{' not in content and '}}' not in content


def test_render_page_renders_one_row_per_item(sandbox):
    pin_theme(sandbox)
    items = [dict(MAIN_ITEM, Name='Git'), dict(MAIN_ITEM, Name='Vim')]
    content = open(render_page('Main', items), encoding='utf-8').read()
    assert content.count('<tr>') == 3  # heading row + two items
    assert '<td>Git</td>' in content
    assert '<td>Vim</td>' in content


def test_render_page_escapes_item_values(sandbox):
    pin_theme(sandbox)
    item = dict(MAIN_ITEM, Name='<script>alert(1)</script>')
    content = open(render_page('Main', [item]), encoding='utf-8').read()
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in content
    assert '<script>alert(1)</script>' not in content


def test_render_page_escapes_priority_but_not_the_template(sandbox):
    pin_theme(sandbox)
    item = dict(MAIN_ITEM, Priority="<script>alert('xss')</script>")
    content = open(render_page('Main', [item]), encoding='utf-8').read()
    assert '&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;' in content


def test_render_page_injects_cdn_urls(sandbox):
    pin_theme(sandbox)
    content = open(render_page('Main', [MAIN_ITEM]), encoding='utf-8').read()
    for url in CDN_URLs.values():
        assert url in content


def test_render_page_uses_the_configured_theme(sandbox):
    pin_theme(sandbox, 'blue')
    content = open(render_page('Main', [MAIN_ITEM]), encoding='utf-8').read()
    assert '#007bff' in content

    pin_theme(sandbox, 'pink')
    content = open(render_page('Main', [MAIN_ITEM]), encoding='utf-8').read()
    assert '#007bff' not in content


def test_render_page_includes_a_generation_timestamp(sandbox):
    pin_theme(sandbox)
    content = open(render_page('Main', [MAIN_ITEM]), encoding='utf-8').read()
    assert re.search(r'Generated at: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content)


def test_render_page_renders_the_update_page(sandbox):
    pin_theme(sandbox)
    item = {
        'Name': 'Git', 'Priority': 1, 'CurrentVersion': '2.40.0', 'NewestVersion': '2.44.0',
        'ReleaseDate': '2024-01-01', 'DownloadURL': 'https://example.com', 'DownloadAttribute': '',
    }
    content = open(render_page('Update', [item]), encoding='utf-8').read()
    assert '<td>2.40.0</td>' in content
    assert '<td>2.44.0</td>' in content


def test_render_page_works_from_a_foreign_working_directory(sandbox, tmp_path, monkeypatch):
    """Regression: templates/themes/output used to be resolved against the CWD."""
    pin_theme(sandbox)
    monkeypatch.chdir(tmp_path)
    filename = render_page('Main', [MAIN_ITEM])
    assert filename.startswith(str(sandbox / 'output'))
    assert os.path.isfile(filename)


def test_render_page_creates_the_output_directory_if_missing(sandbox):
    pin_theme(sandbox)
    shutil.rmtree(sandbox / 'output')
    filename = render_page('Main', [MAIN_ITEM])
    assert os.path.isfile(filename)


def test_render_page_with_no_items_still_generates_a_page(sandbox):
    pin_theme(sandbox)
    content = open(render_page('Main', []), encoding='utf-8').read()
    assert content.count('<tr>') == 1  # heading only
    assert '{{' not in content


def test_open_html_in_browser_uses_a_file_url(tmp_path, monkeypatch):
    from urllib.request import pathname2url

    target = tmp_path / 'SoftwareList_Main_20250101000000.html'
    target.write_text('x', encoding='utf-8')

    opened = []
    monkeypatch.setattr('SLHTMLGeneration.webbrowser.open', opened.append)
    open_html_in_browser(str(target))
    assert opened == ['file:' + pathname2url(str(target))]
