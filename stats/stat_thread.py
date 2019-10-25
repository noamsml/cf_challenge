from queue import Queue
from threading import Thread

class StatThread(Thread):
    def __init__(self, stat_processor):
        super().__init__()
        self.stat_processor = stat_processor
        self.queue = Queue()
    def push_datapoint(self, datapoint):
        self.queue.put(datapoint)
    def run(self):
        while True:
            datapoint = self.queue.get()
            self.stat_processor.process_datapoint(datapoint)
