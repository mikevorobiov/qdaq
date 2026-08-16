import time
from datetime import datetime

from qdaq.core.clock import Clock

# -------------------------------------------
# Test monotomic clock
# -------------------------------------------

def test_mono_returns_a_float():
    clock = Clock()
    assert isinstance(clock.mono(), float)

def test_mono_is_non_decreasing():
    clock = Clock()
    t1 = clock.mono()
    t2 = clock.mono()
    assert t2 >= t2

def test_two_clock_instances_read_the_same_system_clock():
    '''
    Test if two instances read the same underlying system clock:
        if it is true that created and called back-to-back must
        return nearly identical monotonic time values.
    '''
    clk1 = Clock()
    clk2 = Clock()
    assert abs(clk2.mono() - clk1.mono()) < 0.01

# ----------------------------------------------
# Test wall (human-readable) clock for time stamping
# ----------------------------------------------

def test_wall_returns_an_iso_parseable_string():
    clk = Clock()
    wall = clk.wall()
    assert isinstance(wall, str)
    parsed = datetime.fromisoformat(wall)
    assert parsed.tzinfo is not None

# ----------------------------------------------
# Test mono/wall clock consistency
# ----------------------------------------------

def test_mono_wall_orderings_agree_across_repeated_calls():
    clk = Clock()
    monos, walls = [], []
    for _ in range(5):
        monos.append(clk.mono())
        walls.append(clk.wall())
        time.sleep(0.001)
    assert monos == sorted(monos)
    assert walls == sorted(walls)
