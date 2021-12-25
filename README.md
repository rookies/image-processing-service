Image Processing Service
========================

This is a small demo application that I'm using to play with RabbitMQ and Kubernetes. While it's
intended to adhere to the best practices defined by the [twelve-factor methodology](https://12factor.net/),
it is not meant to be used for productive systems.

**You will most certainly run into security issues if you deploy this to a system reachable by
people you don't trust! Use at your own risk!**

## Purpose
The purpose of this software is to accept uploaded image files, process them asynchronously, and
allow the user to download the result of the image processing once it is finished. Since it is
only a demo application, the real use case doesn't really matter. The important point was to have
a workload that is potentially long-running and where using a message queue to communicate with
worker processes therefore makes sense.

## Architecture

## Used Technologies and Software
* **[Python](https://www.python.org/)** for all services
* **[FastAPI](https://fastapi.tiangolo.com/)** for implementing the REST API
* **[PostgreSQL](https://www.postgresql.org/)** as a database server
* **[SQLAlchemy](https://www.sqlalchemy.org/)** to talk to the database server
* **[Alembic](https://alembic.sqlalchemy.org/en/latest/)** for database initialization and migration
* **[RabbitMQ](https://www.rabbitmq.com/)** as a message queue
* **[Pika](https://pika.readthedocs.io/en/stable/)** to talk to RabbitMQ
* **Docker** for all services
* **docker-compose** to run the services for development
