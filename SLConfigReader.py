# -*- coding: utf-8 -*-

import json
import os
import random
import re

from SLHelper import file_content, sl_path

default_theme = 'Random'


def get_all_themes():
    themes_dir = sl_path('themes')
    return sorted(
        f[:-5] for f in os.listdir(themes_dir)
        if os.path.isfile(os.path.join(themes_dir, f)) and re.fullmatch(r'[-_0-9A-Za-z]+\.json', f)
    )


def get_theme_config():
    all_themes = get_all_themes()
    theme = default_theme.lower()

    try:
        data = json.loads(file_content(sl_path('Config.json')))
        theme = data['theme'].lower()

        if theme not in all_themes and theme != 'random':
            raise ValueError('invalid theme')
    except Exception:  # pylint: disable=broad-except
        theme = default_theme.lower()

    if theme == 'random':
        if not all_themes:
            raise FileNotFoundError(f'No theme definitions found in {sl_path("themes")}')
        return random.choice(all_themes)  # nosec
    return theme


def get_adb_config():
    try:
        data = json.loads(file_content(sl_path('Config.json')))
        adb_exec = data['adb_exec']

        if not isinstance(adb_exec, str):
            raise TypeError("'adb_exec' should be str")

        return adb_exec
    except Exception:  # pylint: disable=broad-except
        return None


def get_aapt_config():
    try:
        data = json.loads(file_content(sl_path('Config.json')))
        aapt_exec = data['aapt_exec']

        if not isinstance(aapt_exec, str):
            raise TypeError("'aapt_exec' should be str")

        return aapt_exec
    except Exception:  # pylint: disable=broad-except
        return None
