# -*- coding: utf-8 -*-

import pytest

import SLDeleteDailyUpdateTask as delete_task
import SLCreateDailyUpdateTask as create_task


@pytest.mark.parametrize('value', ['00:00', '09:05', '23:59', '07:30', '19:00'])
def test_check_task_time_accepts_valid_times(value):
    assert create_task.check_task_time(value)


@pytest.mark.parametrize('value', ['24:00', '9:05', '07:60', '7:30', '', 'noon', '07:5'])
def test_check_task_time_rejects_invalid_times(value):
    assert not create_task.check_task_time(value)


def test_input_task_time_re_prompts_until_valid(monkeypatch):
    answers = iter(['nope', '25:00', '07:30'])
    monkeypatch.setattr(create_task.cl, 'input', lambda msg: next(answers))
    assert create_task.input_task_time() == '07:30'


def test_get_updater_points_at_the_script_directory(sandbox):
    """Regression: the updater path used to depend on the working directory."""
    assert create_task.get_updater() == str(sandbox / 'CheckUpdate.bat')


def test_create_task_registers_a_daily_schtasks_job(sandbox, monkeypatch):
    calls = []
    monkeypatch.setattr(create_task.subprocess, 'call', calls.append)
    monkeypatch.setattr(create_task.cl, 'input', lambda msg: '07:30')

    create_task.main()

    assert calls == [(
        'schtasks', '/Create', '/SC', 'DAILY',
        '/TN', create_task.task_name, '/TR', str(sandbox / 'CheckUpdate.bat'), '/ST', '07:30', '/F',
    )]


def test_delete_task_removes_the_schtasks_job(monkeypatch):
    calls = []
    monkeypatch.setattr(delete_task.subprocess, 'call', calls.append)

    delete_task.main()

    assert calls == [('schtasks', '/Delete', '/TN', delete_task.task_name, '/F')]


def test_both_task_scripts_share_the_same_task_name():
    assert create_task.task_name == delete_task.task_name
