from time import time
from .structure import Pipeline, PipeStage

def compute_throughput(pipeline: Pipeline):
    if not pipeline.ticks_ts:
        raise Exception("Pipeline hasn't started")

    time_delta = time() - pipeline.ticks_ts

    output = {}

    for name, stage in pipeline.stages.items():
        tp = stage.ticks.get() / time_delta
        output[name]= tp

    return output


def compute_pipe_sizes(pipeline: Pipeline):
    output = {}

    for name, queue in pipeline.queues.items():
        output[name] = queue.qsize()

    return output