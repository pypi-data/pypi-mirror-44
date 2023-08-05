"""
    Manager
    =======

    Contains the interface for the test framework.

    .. Copyright:
        Copyright 2018 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""


import time
import random
import logging
import datetime
import multiprocessing


class TestManager(object):
    """
    Test Manager

    Simple test framework to hold common methods for test cases

    Attributes:

    tx_queue:

    """

    def __init__(self,
                 tx_queue: multiprocessing.Queue,
                 rx_queue: multiprocessing.Queue,
                 start_signal: multiprocessing.Event,
                 exit_signal: multiprocessing.Event,
                 logger=None):

        super(TestManager, self).__init__()
        self.tx_queue = tx_queue
        self.rx_queue = rx_queue
        self.start_signal = start_signal
        self.exit_signal = exit_signal
        self.number_of_runs = 0
        self._jitter_interval = dict(min=0, max=0)

        self._tasks = list()
        self.logger = logger or logging.getLogger(__name__)

    def until(self, deadline: datetime) -> int:
        """ returns the amount of seconds until the next deadline"""
        now = datetime.datetime.utcnow()
        return (deadline - now).total_seconds()

    # Move to interface
    def register_task(self, cb: callable, number_of_runs=1)->None:
        """
        Registers a task within the Manager's stack

        cb: argument-less function
        """
        for _ in range(0, number_of_runs):
            self._tasks.append(cb)

        self.number_of_runs = len(self._tasks)

    def execution_jitter(self, min=0, max=0):
        """ Defines the jitter amount"""
        self._jitter_interval['min'] = min
        self._jitter_interval['max'] = max

    def jitter(self):
        """ sleep for a random amount of seconds """
        rnd = random.uniform(self._jitter_interval[
                             'min'], self._jitter_interval['max'])
        self.logger.info('Applying task jitter {}s'.format(rnd))
        time.sleep(rnd)

    def reset(self):
        """ Resets the start signal """
        try:
            self.start_signal.clear()
        except:
            pass

    def run(self)->None:
        """ Executes each task in the Manager's stack, one by one """
        try:
            task_counter = 0
            for task in self._tasks:
                task_counter = task_counter + 1
                self.logger.info("starting task: {}".format(task_counter))
                self.jitter()
                task(task_counter)
                self.reset()
        except:
            print('something went wrong')
            self.exit_signal.set()
