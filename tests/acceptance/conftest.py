import pytest

from aiocache import SimpleMemoryCache, RedisCache, MemcachedCache, caches
from aiocache.backends.redis import RedisBackend


def pytest_namespace():
    return {
        'KEY': "key",
        'KEY_1': "random"
    }


@pytest.fixture(autouse=True)
def reset_caches():
    caches._caches = {}
    caches.set_config({
        'default': {
            'cache': "aiocache.SimpleMemoryCache",
            'serializer': {
                'class': "aiocache.serializers.NullSerializer"
            }
        }
    })


@pytest.fixture(autouse=True)
def reset_redis_pools():
    RedisBackend.pools = {}


@pytest.fixture
def redis_cache(event_loop):
    cache = RedisCache(namespace="test")
    yield cache

    event_loop.run_until_complete(cache.delete(pytest.KEY))
    event_loop.run_until_complete(cache.delete(pytest.KEY_1))
    event_loop.run_until_complete(cache.delete(pytest.KEY + '-lock'))
    event_loop.run_until_complete(cache.close())


@pytest.fixture
def memory_cache(event_loop):
    cache = SimpleMemoryCache(namespace="test")
    yield cache

    event_loop.run_until_complete(cache.delete(pytest.KEY))
    event_loop.run_until_complete(cache.delete(pytest.KEY_1))
    event_loop.run_until_complete(cache.delete(pytest.KEY + '-lock'))
    event_loop.run_until_complete(cache.close())


@pytest.fixture
def memcached_cache(event_loop):
    cache = MemcachedCache(namespace="test")
    yield cache

    event_loop.run_until_complete(cache.delete(pytest.KEY))
    event_loop.run_until_complete(cache.delete(pytest.KEY_1))
    event_loop.run_until_complete(cache.delete(pytest.KEY + '-lock'))
    event_loop.run_until_complete(cache.close())


@pytest.fixture(params=[
    'redis_cache',
    'memory_cache',
    'memcached_cache',
])
def cache(request):
    return request.getfuncargvalue(request.param)
