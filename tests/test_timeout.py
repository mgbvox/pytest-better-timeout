import time

import pytest

from pytest_better_timeout import TimeoutHelper


def variable_duration_fn(duration: int):
    t0 = time.time()
    while True:
        _ = 0
        if time.time() - t0 > duration:
            break
    return True


def test_short_fn_with_decorator():
    @TimeoutHelper.set_timeout(seconds=10)
    def helper():
        variable_duration_fn(5)

    helper()


def test_long_fn_with_decorator():
    with pytest.raises(TimeoutError):

        @TimeoutHelper.set_timeout(seconds=5)
        def helper():
            variable_duration_fn(10)

        helper()


def test_long_fn_timeout_zero():
    with pytest.raises(TimeoutError):

        @TimeoutHelper.set_timeout(seconds=0)
        def helper():
            variable_duration_fn(10)

        helper()


@pytest.fixture()
def run_time_duration() -> int:
    return 20


@pytest.fixture()
def short_run_time_duration() -> int:
    return 5


def test_with_fixture(run_time_duration: int):
    @TimeoutHelper.set_timeout(10)
    def helper(run_time_duration: int):
        variable_duration_fn(run_time_duration)

    with pytest.raises(TimeoutError):
        helper(run_time_duration)


def test_with_fixture_short(short_run_time_duration: int):
    @TimeoutHelper.set_timeout(10)
    def helper(short_run_time_duration: int):
        variable_duration_fn(short_run_time_duration)

    helper(short_run_time_duration)


def test_context_manager_long_running():
    # with TimeoutHelper(3):
    #     variable_duration_fn(5)
    with TimeoutHelper.context_timer(3):
        variable_duration_fn(5)


def test_context_manager_short_running():
    # with TimeoutHelper(5):
    #     variable_duration_fn(2)
    with TimeoutHelper.context_timer(5):
        variable_duration_fn(2)


def test_timeout_continues_tests():
    assert True


def test_timeout_continues_tests_again():
    assert True
