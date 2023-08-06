import pytest

from async_property import async_cached_property
from async_property.cached import AsyncCachedPropertyDescriptor
from async_property.proxy import AwaitableOnly, AwaitableProxy

pytestmark = pytest.mark.asyncio


class MyModel:
    @async_cached_property
    async def foo(self) -> str:
        return 'bar'


async def test_descriptor():
    assert isinstance(MyModel.foo, AsyncCachedPropertyDescriptor)
    assert MyModel.foo.__name__ == 'foo'
    assert MyModel.foo.__annotations__['return'] == str


async def test_field():
    instance = MyModel()
    assert isinstance(instance.foo, AwaitableOnly)
    assert await instance.foo == 'bar'
    assert 'foo' in instance.__async_property__.cache


async def test_awaited_repeated():
    instance = MyModel()
    assert await instance.foo == 'bar'
    assert isinstance(instance.foo, AwaitableProxy)
    assert instance.foo == 'bar'
    assert await instance.foo == 'bar'


async def test_default_setter():
    instance = MyModel()
    instance.foo = 'abc'
    assert 'foo' in instance.__async_property__.cache
    assert instance.foo == 'abc'


async def test_default_deleter():
    instance = MyModel()
    await instance.foo
    assert 'foo' in instance.__async_property__.cache
    del instance.foo
    assert 'foo' not in instance.__async_property__.cache


class ModelWithSetterDeleter:
    @async_cached_property
    async def foo(self):
        return 'bar'

    @foo.setter
    def foo(self, value):
        self.bar = '123'

    @foo.deleter
    def foo(self):
        del self.bar


async def test_async_property_with_setter():
    instance = ModelWithSetterDeleter()
    instance.foo = 'abc'
    assert instance.foo == 'abc'
    assert await instance.foo == 'abc'
    assert 'foo' in instance.__async_property__.cache
    assert hasattr(instance, 'bar')
    assert instance.bar == '123'


async def test_async_property_with_deleter():
    instance = ModelWithSetterDeleter()
    await instance.foo
    assert 'foo' in instance.__async_property__.cache
    assert hasattr(instance, 'bar')
    del instance.foo
    assert 'foo' not in instance.__async_property__.cache
    assert not hasattr(instance, 'bar')


class MyModelWithMultiple:
    @async_cached_property
    async def first(self):
        return 123

    @async_cached_property
    async def second(self):
        return 456


async def test_multiple_fields():
    instance = MyModelWithMultiple()
    assert await instance.first == 123
    assert await instance.second == 456


async def test_bad_setter_name():
    with pytest.raises(AssertionError):
        class BadSetter:
            @async_cached_property
            async def foo(self):
                return True

            @foo.setter
            def not_foo(self, value):
                pass


async def test_async_setter():
    with pytest.raises(AssertionError):
        class AsyncSetter:
            @async_cached_property
            async def foo(self):
                return True

            @foo.setter
            async def foo(self, value):
                pass
