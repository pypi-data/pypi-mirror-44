# Statsdecor

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.txt)
[![Build Status](https://api.travis-ci.org/freshbooks/statsdecor.svg)](https://travis-ci.org/freshbooks/statsdecor)

A set of decorators and helper methods for adding statsd metrics to applications.

## Installation

You can use pip to install statsdecor:

```shell
pip install statsdecor
```

## Configuration

You must use `statsdecor.configure` to configure the internal statsd client before
calling other methods:

```python
import statsdecor

statsdecor.configure(host='localhost', prefix='superapp.')
```

Configuration is generally setup during your application's bootstrap. Once
set configuration values are re-used in all clients that `statsdecor` creates.


## Usage

You can track metrics with either the module functions, or decorators. Incrementing
and decrementing counters looks like:

### Metric functions

```python
import statsdecor

statsdecor.incr('save.succeeded')
statsdecor.decr('attempts.remaining')
statsdecor.gauge('sessions.active', 9001)
```

Counters and timers can also be set through decorators:

```python
import statsdecor.decorators as stats

@stats.increment('save.succeeded')
def save(self):
    pass

@stats.decrement('attempts.remaining')
def attempt():
    pass

@stats.timed('api_request.duration')
def perform_request(self, req)
    pass
```

When using decorators, metrics are only tracked if the decorated function
does not raise an error.
