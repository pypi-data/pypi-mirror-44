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

## Installation

`pip3 install dtest-framework`

## Unit Tests

Testing is set up using Pytest

Install Pytest with `pip3 install -U pytest`

Run the tests with `pytest` in the root directory.

## Circle CI

There is a `.circleci/config.yml` file that will execute the build and the unit tests against Python 3.6.

## Quick Start

```
from dtest.dtest import Dtest
from hamcrest import *

connectionConfig = {
    "host": "localhost",
    "username": "guest", # Can be set to None to bypass authentication
    "password": "guest", # Can be set to None to bypass authentication
    "exchange": "test.dtest",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test of the assertCondition",
    "topic": "test.dtest",
    "ruleSet": "Testing some random data",
    "dataSet": "random_data_set_123912731.csv"
}

dt = Dtest(connectionConfig, metadata)

dsQubert = [0,1]

dt.assert_that(dsQubert, has_length(2))
// True

dt.publish()
// Publishes test suite to MQ server
```
