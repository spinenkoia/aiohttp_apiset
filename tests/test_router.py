import asyncio

from aiohttp_apiset.routes import SwaggerRouter


def test_setup(app):
    SwaggerRouter(
        'data/root.yaml',
        search_dirs=['tests']
    ).setup(app)


def test_routes(swagger_router: SwaggerRouter):
    paths = [url for method, url, handler in swagger_router._routes.values()]
    assert '/api/1/file/image' in paths


def test_route_include(swagger_router: SwaggerRouter):
    paths = [url for method, url, handler in swagger_router._routes.values()]
    assert '/api/1/include2/inc/image' in paths


def test_route_swagger_include(swagger_router: SwaggerRouter):
    paths = next(iter(swagger_router._swagger_data.values()))['paths']
    assert '/include/image' in paths


def test_route_swagger_view(swagger_router: SwaggerRouter):
    paths = next(iter(swagger_router._swagger_data.values()))['paths']
    assert '/file/image' in paths


def test_handler(swagger_router: SwaggerRouter):
    paths = [(r.method, r.url) for r in swagger_router._routes.values()]
    assert ('GET', '/api/1/include/image') in paths


def test_definitions(swagger_router: SwaggerRouter):
    d = next(iter(swagger_router._swagger_data.values()))['definitions']
    assert 'File' in d
    assert 'Defi' in d


@asyncio.coroutine
def test_cbv_handler_get(client):
    url = client.app.router['tests.conftest.SimpleView.get'].url()
    res = yield from client.get(url)
    assert (yield from res.text()) == 'simple handler get'


@asyncio.coroutine
def test_cbv_handler_post(client):
    url = client.app.router['tests.conftest.SimpleView.post'].url()
    res = yield from client.post(url)
    assert (yield from res.text()) == 'simple handler post'
