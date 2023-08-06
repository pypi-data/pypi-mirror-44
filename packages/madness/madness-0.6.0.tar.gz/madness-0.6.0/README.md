# madness: a method for your madness

It is built upon WSGI and the fabulous [werkzeug](https://github.com/pallets/werkzeug) routing system, like Flask.



## Guiding Principles

[Don't repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

[Dependency inversion principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

[Do One Thing and Do It Well.](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well)

[The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

## Goals

[Cohesion](https://en.wikipedia.org/wiki/Cohesion_(computer_science))


## Installing

```console
$ pip install -U madness
```

## A Simple Example

```python
from madness import application, get

def hello():
    return 'Hello, world!'

if __name__ == '__main__':
    application(get('/', hello)).run()
```

## Routing

* route and variants

* routes and variants

* defaults

* url parameters

```python
from madness import routes, route, get, post, index

def hello():
  return 'world'

def bar():
  return 'zing!'

# recommended style

urls = routes(
  index(hello),
  routes(
    index(lambda: 'foo')
    route(bar, methods=['GET', 'POST', 'PUT']),
    path = '/foo'
  )
)

# flat style

urls = routes(
  route('/', hello, methods=['GET']),
  route('/foo', lambda: 'foo', methods=['GET']),
  route('/foo/bar', bar, methods=['GET', 'POST', 'PUT']),
)

# add GET to all routes

urls = routes(
  route('/', hello),
  route('/foo', lambda: 'foo'),
  route('/foo/bar', bar, methods=['POST', 'PUT']),
  methods = ['GET']
)


```

## Abstractions (Dependency inversion principle)

* g

* extending g

* madness.G and g_factory


## Middleware (Coroutines)

as decorator

as serializer

as request-contextmanager

as response contextmanager

as request-response contextmanager

as error handler


## Extensions

* json

* cors
