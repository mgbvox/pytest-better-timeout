import time

import pytest

from tests.tools.TimeoutHelper.timeoutHelper import TimeoutHelper


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

        @TimeoutHelper.set_timeout(seconds=10)
        def helper():
            variable_duration_fn(20)

        helper()


def test_long_fn_timeout_zero():
    with pytest.raises(TimeoutError):

        @TimeoutHelper.set_timeout(seconds=0)
        def helper():
            assert variable_duration_fn(20)

        helper()


def test_timeout_continues_tests():
    assert True


def test_timeout_continues_tests_again():
    assert True
