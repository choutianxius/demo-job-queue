# A Demo Web Server Running Tasks with A Job Queue

This is an example application that:

- Provides services through a web server;
- Uses a job queue to dispatch tasks to workers with limited concurrency (one task at a time).

## Quick Start

To start,

```shell
docker compose up
```

To stop, use `CTRL + C`

To shutdown,

```shell
docker compose down
```

Go to <https://localhost:8000/docs> to view the API endpoints for enqueuing tasks and checking tasks status.

## Motivation

Python job queue libraries like `celery` and `rq` all couple task-enqueuing and task execution by forcing the import of task functions. This coupling enables generalizability (any arbitrary task function can be enqued), but is not immediately suitable for use cases where:

- Only a few well-defined task functions will be used;
- Task execution requires some expensive overhead, like loading large datasets.

## Web Server

The server is implemented with FastAPI.

## Job Queue

The queue is implemented with Valkey and uses the `redis` Python library for connection.

## Worker

The worker gets tasks by polling the queue in a while-true loop.

## Possible Improvements

- [ ] Use multiple queues and workers for different types of tasks
- [ ] K8s integration for worker scaling
- [ ] Multi-processing within a single worker
