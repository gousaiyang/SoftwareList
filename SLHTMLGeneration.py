# -*- coding: utf-8 -*-

import html
import json
import os
import re
import time
import webbrowser
from urllib.request import pathname2url

from SLConfigReader import get_theme_config
from SLHelper import file_content, write_file

CDN_URLs = {
    'Bootstrap_CSS_CDN': 'https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css',
    'DataTables_Bootstrap_CSS_CDN': 'https://cdn.bootcss.com/datatables/1.10.16/css/dataTables.bootstrap4.min.css',
    'FontAwesome_CSS_CDN': 'https://cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'jQuery_JS_CDN': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
    'DataTables_JS_CDN': 'https://cdn.bootcss.com/datatables/1.10.16/js/jquery.dataTables.min.js',
    'DataTables_Bootstrap_JS_CDN': 'https://cdn.bootcss.com/datatables/1.10.16/js/dataTables.bootstrap4.min.js'
}

placeholder = '--'
url_placeholder = 'javascript:void(0)'
disable_a = 'disabled'


def render_template(template, data, escape_html=True):
    result = template

    for key, value in data.items():
        v = str(value)
        result = result.replace('{{%s}}' % key, html.escape(v) if escape_html else v)

    return result


def render_page(pagename, data_items):
    if not re.fullmatch(r'[-_0-9A-Za-z]+', pagename):
        raise ValueError('Invalid pagename')

    heading_template_filename = os.path.join('template', 'heading_%s.html' % pagename.lower())
    item_template_filename = os.path.join('template', 'item_%s.html' % pagename.lower())

    if not os.path.isfile(heading_template_filename) or not os.path.isfile(item_template_filename):
        raise NameError('No template found with name %s' % pagename)

    layout_template = file_content(os.path.join('template', 'layout.html'))
    heading_template = file_content(heading_template_filename)
    item_template = file_content(item_template_filename)

    items_html = ''.join(render_template(item_template, s) for s in data_items)

    theme_parameters = json.loads(file_content(os.path.join('themes', '%s.json' % get_theme_config())))

    output_html = render_template(layout_template, CDN_URLs, False)
    output_html = render_template(output_html, theme_parameters, False)
    output_html = render_template(output_html, {
        'PageName': pagename,
        'Heading': heading_template,
        'Items': items_html,
        'TimeOfGeneration': time.strftime('%Y-%m-%d %H:%M:%S')
    }, False)

    new_filename = os.path.join('output', time.strftime('SoftwareList_' + pagename + '_%Y%m%d%H%M%S.html'))
    write_file(new_filename, output_html)
    return new_filename


def open_html_in_browser(filename):
    webbrowser.open('file:' + pathname2url(os.path.abspath(filename)))
