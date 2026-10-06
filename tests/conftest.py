# -*- coding: utf-8 -*-
"""Shared fixtures.

Everything here is offline: no registry, no PowerShell, no ``adb``, no network.
"""

import shutil
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import SLHelper  # noqa: E402  (import after sys.path setup)


@pytest.fixture
def project_root():
    return PROJECT_ROOT


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """A throwaway project tree with copies of the real templates and themes.

    ``SLHelper.BASE_DIR`` is repointed at it, which is exactly what every
    module uses to locate ``Config.json``, ``template/``, ``themes/`` and
    ``output/``.
    """
    shutil.copytree(PROJECT_ROOT / 'template', tmp_path / 'template')
    shutil.copytree(PROJECT_ROOT / 'themes', tmp_path / 'themes')
    (tmp_path / 'output').mkdir()
    monkeypatch.setattr(SLHelper, 'BASE_DIR', tmp_path)
    return tmp_path


@pytest.fixture
def bare_sandbox(tmp_path, monkeypatch):
    """An empty project directory (no templates/themes) for edge-case tests."""
    monkeypatch.setattr(SLHelper, 'BASE_DIR', tmp_path)
    return tmp_path


class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeRequests:
    """Minimal stand-in for the ``requests`` module used by ``web_query``."""

    def __init__(self, mapping):
        self.mapping = mapping
        self.calls = []

    def get(self, url, timeout=None, headers=None):  # noqa: A003  (mirror requests API)
        self.calls.append({'url': url, 'timeout': timeout, 'headers': headers})
        if url not in self.mapping:
            raise ConnectionError(f'no fake route for {url}')
        return FakeResponse(self.mapping[url])


@pytest.fixture
def fake_requests():
    return FakeRequests
