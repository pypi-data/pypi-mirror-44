
# wrapAPI

Requests wrapper for API testing


## Usage

### conftest
conftest.py
```python
import pytest

from wrapapi import Application, Settings


@pytest.fixture(scope='session')
def settings() -> Settings:
    config = Settings()
    config.base_url = 'http://localhost:5555'
    config.headers['Autorization'] = 'Basic secret'
    return config


@pytest.fixture(scope='session')
def client(settings) -> Application:
    app = Application(settings)
    client = app.create()
    yield client
    client.close()


@pytest.fixture(scope='function')
def app(client) -> Application:
    yield client
    client.report.build()

```
tests with pytest fixture
```python
def test_main(app):
    response = app.get('/api/main', status=200)
    response.json.should.be.is_instance(list)


def test_main_item(app):
    response = app.get('/api/main/666', status=200)
    response.json.should.be.equal({'id': 666, 'name': 'test'})

```

### TestCase

with TestSuite
```python
from wrapapi import TestSuite


class TestExample(TestSuite):

    def test_main(self):
        response = self.app.get('/api/main', status=200)
        response.json.should.be.is_instance(list)

    def test_main_item(self):
        response = self.app.get('/api/main/666', status=200)
        response.json.should.be.equal({'id': 666, 'name': 'test'})

```

### AssertionErrors
If we have any errors, raise exception with full request data:
```bash
E           AssertionError: 
E           ===========================================================
E           GET: http://localhost:5555/api/main/666
E           -----------------------------------------------------------
E               Status: 200
E               Body: None
E               Headers: {'Date': 'Wed, 27 Mar 2019 12:17:48 GMT', 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Content-Length': '51'....}
E           ===========================================================
E           Not equal: {'id': 666, 'name': 'test'} == {'id': 1, 'name': 'test'}
E                -> expected: {'id': 666, 'name': 'test'}
E                -> current: {'id': 1, 'name': 'test'}

```