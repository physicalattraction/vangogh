import time
from humanfriendly import format_timespan


class measure_time:
    """
    Class, used as a context manager, to measure the time spent within the context.

    After exiting this context, the object variable `total_seconds` contains the spent time in seconds.

    Typical usage:

    with measure_time() as t:
        do_something_lengthy()
    print(f'The operation took {t.total_seconds} seconds to complete')
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()

    def __str__(self) -> str:
        """
        Return the measured time in a human readable format

        Output under 24 hours: 0:01:30
        Output over 24 hours:  7 days, 10:13:56
        """

        return format_timespan(self.total_seconds, max_units=2)

    @property
    def total_seconds(self) -> float:
        """
        Return the time spent since entering the context manager in seconds
        """

        if self.start_time is None:
            raise ValueError('Not started yet')
        end_time = self.end_time or time.time()
        return end_time - self.start_time
