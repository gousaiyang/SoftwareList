# -*- coding: utf-8 -*-

import json
import os
import random
import re

from SLHelper import file_content

default_theme = 'Random'
all_themes = [f[:-5] for f in os.listdir('themes')
              if os.path.isfile(os.path.join('themes', f)) and re.fullmatch(r'[-_0-9A-Za-z]+\.json', f)]


def get_theme_config():
    try:
        data = json.loads(file_content('Config.json'))
        theme = data['theme'].lower()

        if theme not in all_themes and theme != 'random':
            raise ValueError('invalid theme')
    except Exception:
        theme = default_theme.lower()

    if theme == 'random':
        return random.choice(all_themes)
    else:
        return theme


def get_adb_config():
    try:
        data = json.loads(file_content('Config.json'))
        adb_exec = data['adb_exec']

        if not isinstance(adb_exec, str):
            raise TypeError("'adb_exec' should be str")

        return adb_exec
    except Exception:
        return None


def get_aapt_config():
    try:
        data = json.loads(file_content('Config.json'))
        aapt_exec = data['aapt_exec']

        if not isinstance(aapt_exec, str):
            raise TypeError("'aapt_exec' should be str")

        return aapt_exec
    except Exception:
        return None
