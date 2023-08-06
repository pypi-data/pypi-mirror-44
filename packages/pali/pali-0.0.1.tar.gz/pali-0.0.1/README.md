# Pali

Pali is a simple Thread Pool library for Python. It is compatible with Python3 as well as Python2.

Pali can be used for:
- Creating Data Pipelines.
- Handling requests in Messaging Brokers (on the top of TCP/IP layer).
- Simulating any stress testing systems.
- API Testing systems.

Usage
------------

Pali is simple to use. Pali's Worker Pool works on tasks with well defined interface in ```pali.task.Task```.
New Tasks can be extended from it as following. ```_run``` method is important and mandatory to define as the
Thread Pool internally looks and invokes this function as start of the task.

```
>>> from pali import worker, task
>>> class MyTask(task.Task):
...     def __init__(self, ident):
...         self.task_id = ident
...         self.done = False
...
...     def _run(self):
...         self.done = True

```

Thread Pool in itself can work either as context manager or can be invoked manually. Example below shows it's use
as context manager.

```
# create 10 tasks
>>> tasks = [MyTask(i) for i in range(10)]

# Start a Thread Pool and push tasks on it.
# Tasks are processed as and when they come.
>>> with worker.ThreadPool(3) as tpool:
...     _ = [tpool.append_task(t) for t in tasks]

# Check the status of Tasks
>>> status = [t.done for t in tasks]
>>> status
[True, True, True, True, True, True, True, True, True, True]
```

Further examples can be found at https://github.com/gitvipin/Pali/tree/master/tests that reflect different ways os using ThreadPool.


Requirements
------------
Python 2.7+ and Python 3.4+

Share and enjoy!
