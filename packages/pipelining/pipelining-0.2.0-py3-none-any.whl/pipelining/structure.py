from multiprocessing import Process
from multiprocessing import managers, Manager
from multiprocessing.queues import JoinableQueue
from time import time
import abc

class WorkUnit():
    def __init__(self, id: str=None, payload=None):
        self.id = id
        self.payload = payload
        self.start_ts = time()
        self.finish_ts = None


class PipeStage(Process):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.ticks: managers.Value = None

    def tick(self):
        if self.ticks:
            current = self.ticks.get()
            self.ticks.set(current + 1)

    @abc.abstractmethod
    def will_start(self):
        pass

    @abc.abstractmethod
    def will_stop(self):
        pass

    @abc.abstractmethod
    def work(self):
        pass

    @abc.abstractmethod
    def ports(self):
        pass

    def run(self):
        try:
            self.will_start()
            self.work()
        except KeyboardInterrupt:
            self.will_stop()

class OutputPort():
    def __init__(self, name: str, owner: PipeStage):
        self.name = name
        self.direction = "OUTPUT"
        self.owner = owner
        self.__queue = None

    def connect_to(self, queue: 'PipeQueue'):
        if self.__queue:
            raise Exception("port already connected")
        self.__queue = queue
        queue.track_producer(self)

    def put(self, work: WorkUnit):
        if not self.__queue:
            raise Exception("port not connected")
        self.__queue.put(work)

class InputPort():
    def __init__(self, name: str, owner: PipeStage):
        self.name = name
        self.direction = "INPUT"
        self.owner = owner
        self.__queue = None

    def connect_to(self, queue: 'PipeQueue'):
        if self.__queue:
            raise Exception("port already connected")
        self.__queue = queue
        queue.track_consumer(self)

    def get(self):
        if not self.__queue:
            raise Exception("port not connected")
        return self.__queue.get()

    def task_done(self):
        if not self.__queue:
            raise Exception("port not connected")
        self.__queue.task_done()

class PipeQueue(JoinableQueue):
    def __init__(self, name: str, ctx, maxsize: int=None):
        super().__init__(ctx=ctx, maxsize=maxsize)
        self.name = name
        self.producers = []
        self.consumers = []
    
    def track_producer(self, port: OutputPort):
        self.producers.append(port)

    def track_consumer(self, port: InputPort):
        self.consumers.append(port)


class Pipeline():
    def __init__(self):
        self.__ctx = managers.get_context()
        self.__manager = Manager()
        self.stages = {}
        self.queues = {}
        self.start_ts = None
        self.ticks_ts = None

    def add_stage(self, stage: PipeStage):
        stage.ticks = self.__manager.Value('i', 0)
        self.stages[stage.name] = stage

    def reset_ticks(self):
        self.ticks_ts = time()
        for _, stage in self.stages.items():
            stage.ticks.set(0)

    def add_pipe(self, name: str):
        queue = PipeQueue(name=name, ctx=self.__ctx, maxsize=10000)
        self.queues[name] = queue
        return queue

    def start(self):
        self.start_ts = time()
        self.ticks_ts = self.start_ts

        for name, stage in self.stages.items():
            print(f"starting stage {name}", flush=True)
            stage.start()

    def terminate(self):
        for name, stage in self.stages.items():
            print(f"terminating stage {name}", flush=True)
            stage.terminate()
