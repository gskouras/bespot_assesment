

# Besport Technical Assignment


## Table of Contents

- [Besport Technical Assignment](#besport-technical-assignment)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Software Stack](#software-stack)
  - [API Documentation](#api-documentation)
  - [Web Interface](#web-interface)
  - [Installation and Setup](#installation-and-setup)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Build and Start](#2-build-and-start)
  - [Run Tests](#run-tests)

## Introduction

Welcome to the documentation for the `bespot_assesement` project. This document provides step-by-step instructions on how to set up and run the project using Docker and Docker Compose. `bespot_assesement` is a Django-based application for managing places.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Software Stack

The software stack for this application is composed of various services defined in the local.yaml configuration file. The backend of the application is implemented using Django Rest Framework. To store and manage data, PostgreSQL has been chosen as the database of choice.

Redis serves a dual role within the application. First, it functions as a caching mechanism, improving performance by storing frequently accessed data and reducing the need for repetitive database queries. Second, Redis serves as a message broker for Celery. While Celery may not perform specific tasks within this project, it is included to demonstrate its capabilities and potential use for background processing in future developments.

As an additional component, Flower, a web-based monitoring tool for Celery, has been integrated into the stack. Flower provides a graphical user interface (GUI) for monitoring and managing Celery tasks, offering insights into task execution and system performance.

## API Documentation

The API documentation for the `bespot_assessement` project is available at the following URL:

```bash
http://localhost:8000/swagger/
```

## Web Interface
The web application is provided through the Django Admin Panel. A user can perform CRUID operations in Place models. Also he can perform search, filtering and sorting by address name, code and uuid. 

It is available in the following URL:

```bash
http://localhost:8000/admin/
```

## Installation and Setup

### 1. Clone the Repository

Clone the `bespot_assesement` repository to your local machine:

```bash
git clone https://github.com/GaSkouras/bespot_assesment.git
cd bespot_assesment
```

### 2. Build and Start

The entire stack can be run with the above command. More options can be found in Makefile

```bash
make build
```

## Run Tests

Unittests are implemented with the Python's unittest framework and are executed with pytest. Coverage is used to monitor the overall test coverage of the source code. 

```bash
make build
```
