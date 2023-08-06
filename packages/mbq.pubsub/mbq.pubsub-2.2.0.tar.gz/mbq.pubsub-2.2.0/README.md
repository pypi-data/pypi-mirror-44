# mbq.pubsub

[![PyPI Version](https://img.shields.io/pypi/v/mbq.pubsub.svg)](repo)
[![PyPI License](https://img.shields.io/pypi/l/mbq.pubsub.svg)](repo)
[![Python Versions](https://img.shields.io/pypi/pyversions/mbq.pubsub.svg)](repo)
[![Travis CI Status](https://img.shields.io/travis/managedbyq/mbq.pubsub/master.svg)](repo)

[repo]: https://pypi.python.org/pypi/mbq.pubsub


## Installation

```bash
$ pip install mbq.pubsub
🚀✨
```

Guaranteed fresh.

## Configuration

```python
# settings.py

SERVICE_NAME = "my-service"

PUBSUB = {
    "ENV": mbq.get_environment("ENV_NAME"),
    "SERVICE": SERVICE_NAME,
    "QUEUES": [
        "foo-updates",
        "bar-updates",
    ],
    "MESSAGE_HANDLERS": {
        "foo.updated": "path.to.handlers.handle_foo_updated",
        "bar.updated": "path.to.handlers.handle_bar_updated",
    },
}

INSTALLED_APPS = {
  ...
  'mbq.pubsub',
  ...
}
```

```yaml
# convox.yml

services:
  foo-consumer:
    image: {{DOCKER_IMAGE_NAME}}
    command: newrelic-admin run-python -m manage pubsub consume --queue foo-updates
    init: true
    environment:
      - "*"

  bar-consumer:
    image: {{DOCKER_IMAGE_NAME}}
    command: newrelic-admin run-python -m manage pubsub consume --queue bar-updates
    init: true
    environment:
      - "*"
```

### Using PubSub Without a Database

If your service does not have a database - fear not. The Infra team hath taken pity on you and your brethren. 
Simply add the setting `"USE_DATABASE": False` to your `PUBSUB` config. 

Things to keep in mind:
- There will be no Django admin for viewing/deleting/replaying DLQ messages. 
- To replay the DLQ use the management command `./manage.py pubsub replay --queue <queue_name> <number_of_messages>`.


### Local Development

Add `127.0.0.1 pubsub.lcl.mbq.io` to your `/etc/hosts`.

Find the `env/pubsub/lcl.env` Secure Note in 1Password and copy it to `env/lcl.env`.

```sh
$ pbpaste > env/lcl.env
```

Run migrations and bring up admin the server:

```sh
$ docker-compose run tests-admin python -m manage migrate
$ docker-compose up tests-admin
```

To use the Django admin, you'll need a superuser:

```sh
$ docker-compose run tests-admin python -m manage createsuperuser
```

To end-to-end test mbq.pubsub, you can publish a test message from SNS with:
```sh
$ docker-compose run tests-admin python -m manage publish_exception
```

Then bring up the consumer:
```sh
$ docker-compose up pubsub-pubsub-consume-updates
```

The test message will eventually land on the DLQ, which you can inspect & replay from http://pubsub.lcl.mbq.io:8080/admin/pubsub/undeliverablemessage
