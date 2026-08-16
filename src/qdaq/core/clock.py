import time
from datetime import datetime

class Clock:
    '''
    Single time source shared by everything inside an experiment Session.

    `t_mono` (monotomic) is the primary key for ordering and joining data
    across instruments -- immune to NTP jumps.
    `t_wall` rides alongside for human-readable / external use.
    '''

    def mono(self) -> float:
        '''
        Returns monotonic time `t_mono` for ordering and joining data
        across intruments
        '''
        return time.monotonic()

    def wall(self) -> str:
        '''
        Returns human-readable `t_wall` string time in ISO format.
        The output is used for time-stamping data.
        '''
        return datetime.now().astimezone().isoformat()
