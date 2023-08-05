# Sanic OpenAPI v3e

Give your Sanic API an OpenAPI v3 specification.

## Installation

```shell
pip install sanic-openapi3e
```

## Usage

### Import blueprint and use simple decorators to document routes:

```python
import sanic
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc

app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/user/<user_id:int>")
@doc.summary("Fetches a user by ID")
@doc.response(200, "The user")
async def get_user(request, user_id):
    return sanic.response.json(locals())

app.go_fast()
```

You'll now have a specification at the URL `/openapi/spec.json`.
Your routes will be automatically categorized by their blueprints' 
names.


### Configure some of the things

```python
app.config.API_VERSION = '1.0.0'
app.config.API_TITLE = 'An API'
app.config.API_DESCRIPTION = 'An API description'
```

To have a `contact`, set at least one of (but preferably all) 
`app.config.API_CONTACT_NAME`, 
`app.config.API_CONTACT_URL` or
`app.config.API_CONTACT_EMAIL`. 

To have a `license`, `set app.config.API_LICENSE_NAME"` and 
optionally `app.config."API_LICENSE_URL"`.

To have a `termsOfService`, set
`app.config.API_TERMS_OF_SERVICE_URL`. 

Setting `components`, `security` and `externalDocs` requires you to 

* first create the relevant objects somewhere in your code (near to 
  where you create the `app`),
* set the appropriate `app.config.OPENAPI_COMPONENTS`, 
  `app.config.OPENAPI_SECURITY`,  
  `app.config.OPENAPI_EXTERNAL_DOCS`.
 
#### Use `app.config` to control spec generation


    hide_openapi_self = app.config.get("HIDE_OPENAPI_SELF", True)
    show_excluded = app.config.get("SHOW_OPENAPI_EXCLUDED", False)
    show_unused_tags = app.config.get("SHOW_OPENAPI_UNUSED_TAGS", False)
    
In practice, you don't usually want to document the `/swagger` nor 
`/openapi` routes, but by setting `app.config.HIDE_OPENAPI_SELF = False`
you can have them appear in the generated spec (and therefore swagger 
too). 

Your `@doc.exclude()` annotations are always respected, but if your 
config has `app.config.SHOW_OPENAPI_EXCLUDED = True` then a *second* 
spec at `/openapi/spec.all.json` is created. You generally won't want 
these to be on your production deployment, but you may want it for dev
and test purposes. 




### Describe route path parameters

```python
import sanic
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc
app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/examples/test_id/<an_id:int>")
@doc.parameter(name="an_id", description="An ID", required=True, _in="path")
def test_id(request, an_id):
    return sanic.response.json(locals())
```

``sanic-openapiv3`` will recognise that the path parameter ``an_id`` is
described with ``@doc.parameter`` and will merge the details together.

You may wish to specify that a parameter be limited to a set of choices,
such as day-of-week or that it has a minimum value. These can be done 
for parameters in ``path``, ``query``, ``header`` and ``cookie``:

```python
import sanic
import sanic.request
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc

app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/test/some_ids")
@doc.parameter(
    name="ids",
    description="Some IDs",
    required=True,
    choices=[1, 3, 5, 7, 11, 13],
    _in="query",
    schema=doc.Schema.Integers,
)
def test_some_ids(request: sanic.request.Request):
    query = request.query_string
    return sanic.response.json(locals())
     


@app.get("/examples/test_id_min/<an_id:int>")
@doc.parameter(
    name="an_id", description="An ID", required=True, _in="path", schema=int_min_4
)
def test_id_min(request, an_id: int):
    return sanic.response.json(locals())


int_min_4 = doc.Schema(
    _type="integer", _format="int32", minimum=4, description="Minimum: 4"
)  

```

### Deprecate route paths or parameters

A parameter can be marked as ``@deprecated()``:

```python
import sanic
import sanic.request
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc

app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/examples/test_parameter__deprecated/<an_id:int>")
@doc.parameter(
    name="an_id", description="An ID", required=True, _in="path", deprecated=True
)
@doc.summary("A path deprecated parameter")
@doc.description("The parameter should be marked as deprecated")
def param__deprecated(request, an_id: int):
    return sanic.response.json(locals())
```

as can a whole route:

```python
import sanic
import sanic.request
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc

app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/examples/test_path__deprecated/<an_id:int>")
@doc.parameter(
    name="an_id",
    description="An ID",
    required=True,
    _in="path",
)
@doc.summary("A path with parameter examples")
@doc.description("This is marked as being deprecated")
@doc.deprecated()
def path__deprecated(request, an_id: int):
    return sanic.response.json(locals())
```


### Exclude routes from appearing in the OpenAPI spec (and swagger)

Need to soft-launch an endpoint, or keep your swagger simple? 

```python
import sanic
import sanic.request
import sanic.response
from sanic_openapi3e import openapi_blueprint, swagger_blueprint, doc

app = sanic.Sanic(strict_slashes=True)
app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.get("/test/alpha_release")
@doc.exclude()
@doc.parameter(
    name="ids",
    description="Some IDs",
    required=True,
    choices=[1, 3, 5, 7, 11, 13],
    _in="query",
    schema=doc.Schema.Integers,
)
def test_some_ids(request: sanic.request.Request):
    query = request.query_string
    return sanic.response.json(locals())
```



