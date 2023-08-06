# Airflow Docker Helper
[![CircleCI](https://circleci.com/gh/huntcsg/airflow-docker-helper/tree/master.svg?style=svg)](https://circleci.com/gh/huntcsg/airflow-docker-helper/tree/master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e2f177d8c314f43903fe9d9b7af0647)](https://www.codacy.com/app/fool.of.god/airflow-docker-helper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=huntcsg/airflow-docker-helper&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/huntcsg/airflow-docker-helper/branch/master/graph/badge.svg)](https://codecov.io/gh/huntcsg/airflow-docker-helper)

## Description
A light sdk to be used by the operators in airflow-docker and in task code to participate in host/container communication.

## Installation

```bash
pip install airflow-docker-helper
```

## Usage

### Sensor
```python
from airflow_docker_helper import client

if sensed:
    client.sensor(True)
else:
    client.sensor(False)
```

### Short Circuit

```python
from airflow_docker_helper import client

if should_short_circuit:
    client.short_circuit()
```

### Branching

You can pass a list...
```python
from airflow_docker_helper import client

branch_to_task_ids = ['foo', 'bar']

client.branch_to_tasks(branch_to_task_ids)

```

... or a string.
```python
from airflow_docker_helper import client

client.branch_to_tasks('some-other-task')

```

### Testing

This library ships with a test client that mocks out all io and filesystem calls.  This client 
also provides all of the relevant mocked out files to allow for assertions around the io.

Some higher level assertions are provided. These assertions are based on the lower level file mocks.

```python
from airflow_docker_helper.testing import test_client
client = test_client()
client.assert_not_short_circuited()  # Passes

client.short_circuit()
client.assert_short_circuited()  # Passes

client.sensor(True)

client.assert_sensor_called_with(True)          # Passes
client.assert_sensor_called_with(False)         # Fails

client.assert_branched_to_tasks([])             # Passes

client.branch_to_tasks(['foo', 'bar'])
client.assert_branched_to_tasks(['bar', 'foo']) # Passes

```

For power users, the mocks may be used directly:

```python
>>> from airflow_docker_helper.testing import test_client
>>> client = test_client()
>>> client.branch_to_tasks(['foo', 'bar'])
>>> client._mock_branch_to_tasks_file.mock_calls
[call('./__AIRFLOW_META__/branch_operator.txt', 'wb'),
 call().__enter__(),
 call().write(b'["foo", "bar"]'),
 call().__exit__(None, None, None)]
>>> client.short_circuit()
>>> client._mock_short_circuit_file.mock_calls
[call('./__AIRFLOW_META__/short_circuit.txt', 'wb'),
 call().__enter__(),
 call().write(b'false'),
 call().__exit__(None, None, None)]
>>> client.sensor(True)
>>> client._mock_sensor_file.mock_calls
[call('./__AIRFLOW_META__/sensor.txt', 'wb'),
 call().__enter__(),
 call().write(b'true'),
 call().__exit__(None, None, None)] 
```
