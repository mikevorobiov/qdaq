import json
import queue
import threading
from pathlib import Path

class Logbook:
    '''Maintains a signle append-only JSONL event stream with a
    global monotonic `count`.

    Every caller funnels through `.event(**fields)`; one background
    thread does the actual file write, so `count` can never race across
    threads and lines are never interleaved mid-write.
    '''

    def __init__(self, path: Path):
        self.path: Path = Path(path) # path to JSONL file
        self._queue: queue.Queue = queue.Queue() # organize entries into a queue for threading
        self._count: int = 0 # event sequence counter
        self._count_lock = threading.Lock() # locks the sequence of events
        self._stop = threading.Event()
        self._fh = open(self.path, 'a', buffering=1) # open log file handler to write into
        self._writer_thread = threading.Thread(target=self._drain, daemon=True)
        self._writer_thread.start() # start events writing thread

    def event(self, **fields):
        with self._count_lock: # locked sequence of events
            count = self._count  # get current sequence counter value
            self._count += 1   # increase sequence counter for the next entry
        record = {'#': count, **fields} # prepare record for append to JSONL file
        self._queue.put(record) # put into the FIFO queue
        return count

    def _drain(self):
        '''Drain the queue into the logbook JSONL file'''
        while not self._stop.is_set() or not self._queue.empty():
            try:
                record = self._queue.get(timeout=0.1) # retrieve record fron the queue
            except queue.Empty:
                continue
            self._fh.write(json.dumps(record, default=str) + '\n')
            self._fh.flush()

    def close(self):
        '''Safely close the Labbook'''
        self._stop.set()
        self._writer_thread.join(timeout=5)
        self._fh.close()
