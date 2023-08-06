import pytest

from kafka.errors import KafkaError
from kafkahelpers import ReconnectingClient


class FakeMQ:
    async def start(self):
        return True


class FakeMQFails:
    failures = 0

    async def start(self):
        if not self.failures:
            self.failures = 1
            raise KafkaError("fakemq fails")

        else:
            return True


@pytest.mark.asyncio
async def test_connects():
    mq = FakeMQ()
    cl = ReconnectingClient(mq, "connects")
    await cl.start()
    assert cl.connected is True


@pytest.mark.asyncio
async def test_reconnects():
    mq = FakeMQFails()
    cl = ReconnectingClient(mq, "reconnects", retry_interval=0.1)
    await cl.start()
    assert cl.connected is True


async def wrkr(client):
    return True


async def wrkr_fails(client):
    print(client.failures)
    if client.failures < 2:
        client.failures += 1
        raise KafkaError("wrkr_fails")

    return True


@pytest.mark.asyncio
async def test_work():
    mq = FakeMQ()
    cl = ReconnectingClient(mq, "works")
    await cl.work(wrkr)


@pytest.mark.asyncio
async def test_work_fails():
    mq = FakeMQFails()
    cl = ReconnectingClient(mq, "works_fails", retry_interval=0.1)
    await cl.work(wrkr_fails)
    await cl.start()
    assert cl.connected is True


def done(v):
    return v is False


@pytest.mark.asyncio
async def test_callback(event_loop):
    mq = FakeMQ()
    cl = ReconnectingClient(mq, "callback")
    coro = cl.get_callback(wrkr, done)
    task = event_loop.create_task(coro())
    await task
    assert task.result() is None


@pytest.mark.asyncio
async def test_callback_retries(event_loop):
    mq = FakeMQFails()
    cl = ReconnectingClient(mq, "callback_retries", retry_interval=0.1)
    coro = cl.get_callback(wrkr_fails, done)
    task = event_loop.create_task(coro())
    await task
    assert task.result() is None


@pytest.mark.asyncio
async def test_run(event_loop):
    mq = FakeMQ()
    cl = ReconnectingClient(mq, "callback")
    task = event_loop.create_task(cl.run(wrkr, done))
    await task
    assert task.result() is None
