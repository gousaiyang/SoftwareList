# -*- coding: utf-8 -*-

import os
import re
import traceback
from collections import defaultdict

from SLHelper import keep_window_open, sl_path

list_filename_pattern = re.compile(r'\ASoftwareList_([-_0-9A-Za-z]+)_\d{14}\.html\Z')


def find_lists(output_dir=None):
    """Return ``{page name: [filenames]}`` for the generated lists, oldest first."""
    groups = defaultdict(list)

    for name in os.listdir(output_dir or sl_path('output')):
        match = list_filename_pattern.match(name)
        if match:
            groups[match.group(1)].append(name)

    # Filenames embed a YYYYmmddHHMMSS timestamp, so lexicographic order is
    # chronological order.
    for files in groups.values():
        files.sort()

    return groups


def clear_old_lists(output_dir=None):
    """Delete every generated list except the newest one of each kind.

    Returns the filenames that were deleted.
    """
    output_dir = output_dir or sl_path('output')
    deleted = []

    for files in find_lists(output_dir).values():
        for name in files[:-1]:
            os.remove(os.path.join(output_dir, name))
            deleted.append(name)

    return deleted


def main():
    clear_old_lists()


if __name__ == '__main__':
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()
        keep_window_open()
