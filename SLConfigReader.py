# -*- coding: utf-8 -*-

import os
import re
import json
import random

from SLHelper import file_content

default_theme = 'Random'
all_themes = [f[:-5] for f in os.listdir('themes')
    if os.path.isfile(os.path.join('themes', f)) and re.match(r'^[-_0-9A-Za-z]+\.json$', f)]

def get_theme_config():
    try:
        data = json.loads(file_content('Config.json'))
        theme = data['theme'].lower()
        assert theme == 'random' or theme in all_themes
    except:
        theme = default_theme.lower()

    if theme == 'random':
        return random.choice(all_themes)
    else:
        return theme

def get_adb_config():
    try:
        data = json.loads(file_content('Config.json'))
        adb_exec = data['adb_exec']
        assert isinstance(adb_exec, str)
        return adb_exec
    except:
        return None

def get_aapt_config():
    try:
        data = json.loads(file_content('Config.json'))
        aapt_exec = data['aapt_exec']
        assert isinstance(aapt_exec, str)
        return aapt_exec
    except:
        return None
