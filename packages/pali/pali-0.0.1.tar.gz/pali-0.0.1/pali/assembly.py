#!/usr/bin/env python
'''
This module defines the Abstract Interface and Implementation for
Pipeline Stages, Pipelines and Assembly.

A Stage is an atomic step as part of whole pipelining process. A Pipeline
is a collection of Stages. An Assembly is collection of Pipelines.

There can be several stages in a pipeline but there must be a serial order
in which they shall be executed. This is the reason Stages are kept in the
form of Linked List inside a pipeline. No two stages of same pipeline can
be executed in parallel. However, there can be multiple pipelines
that can be run in parallel.

A single thread shall be assigned to execute a pipeline stage as it
is always executed in serial order.

Pipelines are nothing but a description of collection of steps to be
executed on a given set of data.

One usecase of pipelines is to configure endpoints / VMs / nodes. Here,
set of steps to be executed is same for all the endpoints but need to be
separately and can also be executed in parallel. In such a case, a pipeline
will be defined once but Assembly will create multiple Pipelines with varying
IP addresses of endpoints to be configured.

'''

import abc
import logging
import task
import worker


class Stage(task.Task):

    """
    Stages are like the atomic step of pipelines execution.
    """

    __metaclass__ = abc.ABCMeta
    WAITING = 0x1
    RUNNING = 0x1 << 1
    PASSED = 0x1 << 2
    FAILED = 0x1 << 3

    def __init__(self, name):
        self.name = name

        self._state = self.WAITING
        self._next = None

        self.log = logging.getLogger(__name__)


class Pipeline(task.Task):

    def __init__(self, stages, data=None):
        """
        A pipeline is a collection of pipeline stages.
        """
        self.stages = []
        self.data = data if data else {}
        self.log = logging.getLogger(__name__)

    def _run(self):
        for stage in self._stages:
            try:
                stage.run(self.data)
            except Exception as err:
                # TODO : Do better Error handling
                self.log.error("Pipeline Error : %r", err)

                # if a pipeline stage fais we need to stop the execution.
                break


class Assembly(task.Task):

    MAX_CONCURRENT_PIPELINES = 5

    def __init__(self, pipelines=None, max_concurrent_pipelines=None):
        '''
        Assembly is a collection of pipelines.
        '''
        self.pipelines = pipelines if pipelines else []
        self.max_threads = max_concurrent_pipelines if max_concurrent_pipelines is not None else self.MAX_CONCURRENT_PIPELINES

    def _run(self):

        tpool = worker.ThreadPool(self.max_threads)

        for pipeline in self.pipelines:
            tpool.append_task(pipeline)

        tpool.close()
