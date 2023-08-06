# madness

Madness orchestrates the HTTP request-response cycle using middleware for abstractions and routes for transformations.

It is built upon WSGI and the fabulous [werkzeug](https://github.com/pallets/werkzeug) routing system.


## Guiding Principles

[Don't repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

[Dependency inversion principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

[Do One Thing and Do It Well.](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well)

[The Zen of Python](https://www.python.org/dev/peps/pep-0020/)

## Installing

```console
$ pip install -U madness
```

## A Simple Example

```python
from madness import run

def hello():
    return 'Hello, world!'

if __name__ == '__main__':
    run(hello)
```

## Routing

a route may be specified with methods, middleware and defaults

```python
from madness import routes, route, get, post, put, delete, patch, index

users = routes(
  index(lambda: 'users!'), # GET /
  get('/<int:user_id>', lambda user_id: f'id is {user_id}')
)

site = routes(
  get('/', lambda: 'homepage'), # GET / .. aka index
  route(my_function) # /my_function, any method
  # add users routes under the /users prefix
  routes(users, path = '/users'),
  # limit the request methods
  route('/foo', lambda: 'bar', methods = ['GET', 'POST']),
  post(my_other_function), # POST /my_other_function
)

```


## Application / Serving

initialize an application to serve your routes through WSGI

### handling routing errors using middleware

```python
from madness import application, NotFound, index

def custom404():
  try:
    yield # application tries to find a route
  except NotFound:
    yield 'custom 404 body', 404

app = application(
  index(lambda: 'Hello, world!'),
  middleware = [custom404]
)

if __name__ == '__main__':
  app.run()
```

***

## Nesting routes / middleware

you can nest routes and middleware as much as you need

```python
from madness import routes, cors, route, index, get, abort

api = routes(

  # public API
  index(lambda: '1.0.0'),
  post('/login', lambda: abort(401)),

  # login required
  routes(
    routes(
      users,
      path = '/users',
      middleware = [
        # middleware to abstract the user database implementation
        users_database_implementation
      ]
    ),
    get('/groups', lambda: 'groups resource')
    middleware = [
      # check that the client is logged in
      authorize
    ]
  ),

  middleware = [
    # authenticate any client that accesses the API
    authenticate
  ]

)

app = application(
  index(lambda: 'Welcome to my app!'),
  # enable CORS for our API and static resources
  cors(
    routes(api, path = '/api'),
    route('/static/<path:filename>', lambda: 'not implemented'),
    # CORS settings
    origin = '*'
  ),
  middleware = [my_application_middleware]
)

if __name__ == '__main__':
  app.run()
```


***

## Middleware

use madness.context to store *abstractions* for your higher level middleware/routes

[rule args](http://werkzeug.pocoo.org/docs/0.14/routing/) are added to context after successful routing

middleware has full access to request/response/exceptions

passing middleware to a madness.application will allow you to catch routing errors

the response/exception is bubbled through the middleware

```python
from madness import request, json

def overkill_middleware():
    """demonstrates every """
    # before_request
    if request.headers.get('x-api-key') != 'valid-api-key':
        # abort
        yield json.response({'message': 'invalid api key'}, status = 403)
    else:
        try:
            response = yield
        except MyException as exception:
            yield json.response({'message': exception.message}, status = 500)
        else:
            # modify the response headers
            response.headers['x-added-by-context'] = 'value'
            # abort
            yield json.response('we decided to not send the original response, isn\'t that weird?')
        finally:
            # after_request
            pass
```


### RESTful routes

inspired by Ruby on Rails' `resources` and these links

https://gist.github.com/alexpchin/09939db6f81d654af06b

https://medium.com/@shubhangirajagrawal/the-7-restful-routes-a8e84201f206

```python
from madness import routes, index, new, create, show, edit, update, destroy

users = routes(
  index(get_all_users),
  new(new_user_form),
  create(add_user),
  show(get_one_user),
  edit(edit_user_form),
  update(update_user),
  destroy(delete_user),
  path = '/users'
)
```
