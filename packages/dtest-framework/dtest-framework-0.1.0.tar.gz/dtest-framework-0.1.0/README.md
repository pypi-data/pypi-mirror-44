# dtest

[![CircleCI](https://circleci.com/gh/sjensen85/dtest/tree/master.svg?style=svg)](https://circleci.com/gh/sjensen85/dtest/tree/master)
[![Requirements Status](https://requires.io/github/sjensen85/dtest/requirements.svg?branch=master)](https://requires.io/github/sjensen85/dtest/requirements/?branch=master)

A library to facilitate the testing of data inside data pipelines. Results are pushed to a messaging queue of some sort for consumption by applications, persistence, etc.

Supported messaging queues / streaming platforms

- [x] RabbitMQ
- [ ] MQTT
- [ ] Redis
- [ ] Kafka
- [ ] Kinesis

## Requirements

Package requirements are handled using setup.py. They will be automatically installed on install or during unit testing

## Unit Tests

Testing is set up using Pytest

Install Pytest with `pip3 install -U pytest`

Run the tests with `pytest` in the root directory.

## Circle CI

There is a `.circleci/config.yml` file that will execute the build and the unit tests against Python 3.6.

## Quick Start

```
from dtest.dtest import Dtest

connectionConfig = {
    "host": "localhost",
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test of the assertCondition",
    "topic": "test.dtest",
}
dt = Dtest(connectionConfig, metadata)

dt.assertTrue(len([0, 1]) > 1)
// True
```
