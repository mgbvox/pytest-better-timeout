import platform
import signal
import threading
from typing import Callable, Optional, Any

import decorator


class TimeoutHelper:
    # TODO - ability to return values
    def __init__(self, seconds: int = 0, error_message: Optional[str] = None) -> None:
        self.seconds = seconds
        self.error_message = (
            error_message
            or f"Timeout Error! Function took longer than {self.seconds} seconds to "
            f"execute."
        )
        self.alarm: threading.Timer = None

    @staticmethod
    def is_unix() -> bool:
        return platform.system() != "Windows"

    def handle_timeout(
        self, signum: Optional[signal.Signals] = None, frame: Any = None
    ) -> None:
        raise TimeoutError(self.error_message)

    def __enter__(self) -> None:
        if self.is_unix():
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.seconds)
        else:
            self.alarm.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.is_unix():
            signal.alarm(0)
        else:
            self.alarm.cancel()

    @classmethod
    @decorator.contextmanager
    def context_timer(cls, seconds: int = 0):
        handler = cls(seconds)
        if handler.is_unix():
            signal.signal(signal.SIGALRM, handler.handle_timeout)
            signal.alarm(handler.seconds)
        else:
            handler.alarm = threading.Timer(seconds, handler.handle_timeout)
            handler.alarm.start()
        try:
            yield
        finally:
            if handler.is_unix():
                signal.alarm(0)
            else:
                handler.alarm.cancel()

    @classmethod
    def set_timeout(cls, seconds: int) -> Callable:
        if cls.is_unix():
            return cls._set_timeout_unix(seconds=seconds)
        else:
            return cls._set_timeout_win(seconds=seconds)

    @classmethod
    def _set_timeout_unix(cls, seconds: int):
        def deco(fn: Callable):
            def wrapper(*args, **kwargs) -> None:
                with cls(seconds=seconds):
                    fn(*args, **kwargs)

            return wrapper

        return deco

    @classmethod
    def _set_timeout_win(cls, seconds: int):
        def deco(fn: Callable):
            def wrapper(fn: Callable, *args, **kwargs) -> None:
                handler = cls(seconds=seconds)
                wrapped_fn = threading.Thread(target=fn, args=args, kwargs=kwargs)
                wrapped_fn.start()
                wrapped_fn.join(float(seconds))

                if wrapped_fn.is_alive():
                    handler.handle_timeout()

            return decorator.decorator(wrapper, fn)

        return deco
