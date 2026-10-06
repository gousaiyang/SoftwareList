# -*- coding: utf-8 -*-

import re

import SLHelper


def read_pyproject_version(project_root):
    text = (project_root / 'pyproject.toml').read_text(encoding='utf-8')
    match = re.search(r'^version\s*=\s*[\'"]([^\'"]+)[\'"]', text, re.MULTILINE)
    assert match, 'pyproject.toml has no static version'
    return match.group(1)


def test_pyproject_version_matches_the_shared_helper_version(project_root):
    """Keep ``SLHelper.__version__`` (used by ``--version``) in sync."""
    assert read_pyproject_version(project_root) == SLHelper.__version__


def test_version_is_a_three_part_string():
    assert re.fullmatch(r'\d+\.\d+\.\d+', SLHelper.__version__)


def test_declared_python_floor_supports_removesuffix(project_root):
    """``str.removesuffix`` (used by a post-processing rule) needs 3.9+."""
    text = (project_root / 'pyproject.toml').read_text(encoding='utf-8')
    match = re.search(r"requires-python\s*=\s*['\"]>=(\d+)\.(\d+)", text)
    assert match
    assert (int(match.group(1)), int(match.group(2))) >= (3, 9)
