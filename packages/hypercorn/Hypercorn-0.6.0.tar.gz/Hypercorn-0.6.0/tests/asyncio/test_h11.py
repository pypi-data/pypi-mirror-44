import asyncio
import json
from typing import Union
from unittest.mock import Mock

import h11
import pytest

from hypercorn.asyncio.h11 import H11Server
from hypercorn.config import Config
from hypercorn.typing import ASGIFramework
from .helpers import MockTransport
from ..helpers import chunked_response_framework, echo_framework

BASIC_HEADERS = [("Host", "hypercorn"), ("Connection", "close")]
BASIC_DATA = "index"


class MockConnection:
    def __init__(
        self, event_loop: asyncio.AbstractEventLoop, *, framework: ASGIFramework = echo_framework
    ) -> None:
        self.transport = MockTransport()
        self.client = h11.Connection(h11.CLIENT)
        self.server = H11Server(framework, event_loop, Config(), self.transport)  # type: ignore

    async def send(self, event: Union[h11.Request, h11.Data, h11.EndOfMessage]) -> None:
        await self.send_raw(self.client.send(event))

    async def send_raw(self, data: bytes) -> None:
        self.server.data_received(data)
        await asyncio.sleep(0)  # Yield to allow the server to process

    def get_events(self) -> list:
        events = []
        self.client.receive_data(self.transport.data)
        while True:
            event = self.client.next_event()
            if event in (h11.NEED_DATA, h11.PAUSED):
                break
            events.append(event)
            if isinstance(event, h11.ConnectionClosed):
                break
        return events


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method, headers, body",
    [
        ("GET", BASIC_HEADERS, ""),
        ("POST", BASIC_HEADERS + [("content-length", str(len(BASIC_DATA.encode())))], BASIC_DATA),
    ],
)
async def test_request(
    method: str, headers: list, body: str, event_loop: asyncio.AbstractEventLoop
) -> None:
    connection = MockConnection(event_loop)
    await connection.send(h11.Request(method=method, target="/", headers=headers))
    await connection.send(h11.Data(data=body.encode()))
    await connection.send(h11.EndOfMessage())
    await connection.transport.closed.wait()
    response, *data, end = connection.get_events()
    assert isinstance(response, h11.Response)
    assert response.status_code == 200
    assert (b"server", b"hypercorn-h11") in response.headers
    assert b"date" in (header[0] for header in response.headers)
    assert all(isinstance(datum, h11.Data) for datum in data)
    data = json.loads(b"".join(datum.data for datum in data).decode())
    assert data["request_body"] == body  # type: ignore
    assert isinstance(end, h11.EndOfMessage)


@pytest.mark.asyncio
async def test_protocol_error(event_loop: asyncio.AbstractEventLoop) -> None:
    connection = MockConnection(event_loop)
    await connection.send_raw(b"broken nonsense\r\n\r\n")
    response = connection.get_events()[0]
    assert isinstance(response, h11.Response)
    assert response.status_code == 400
    assert (b"connection", b"close") in response.headers


@pytest.mark.asyncio
async def test_pipelining(event_loop: asyncio.AbstractEventLoop) -> None:
    connection = MockConnection(event_loop)
    # Note that h11 does not support client pipelining, so this is all raw checks
    await connection.send_raw(
        b"GET / HTTP/1.1\r\nHost: hypercorn\r\nConnection: keep-alive\r\n\r\n"
        b"GET / HTTP/1.1\r\nHost: hypercorn\r\nConnection: close\r\n\r\n"
    )
    await connection.transport.closed.wait()
    assert connection.transport.data.decode().count("HTTP/1.1") == 2


@pytest.mark.asyncio
async def test_client_sends_chunked(event_loop: asyncio.AbstractEventLoop,) -> None:
    connection = MockConnection(event_loop)
    chunked_headers = [("transfer-encoding", "chunked"), ("expect", "100-continue")]
    await connection.send(
        h11.Request(method="POST", target="/echo", headers=BASIC_HEADERS + chunked_headers)
    )
    await connection.transport.updated.wait()
    informational_response = connection.get_events()[0]
    assert isinstance(informational_response, h11.InformationalResponse)
    assert informational_response.status_code == 100
    connection.transport.clear()
    for chunk in [b"chunked ", b"data"]:
        await connection.send(h11.Data(data=chunk, chunk_start=True, chunk_end=True))
    await connection.send(h11.EndOfMessage())
    await connection.transport.closed.wait()
    response, *data, end = connection.get_events()
    assert isinstance(response, h11.Response)
    assert response.status_code == 200
    assert all(isinstance(datum, h11.Data) for datum in data)
    data = json.loads(b"".join(datum.data for datum in data).decode())
    assert data["request_body"] == "chunked data"  # type: ignore
    assert isinstance(end, h11.EndOfMessage)


@pytest.mark.asyncio
async def test_server_sends_chunked(event_loop: asyncio.AbstractEventLoop) -> None:
    connection = MockConnection(event_loop, framework=chunked_response_framework)
    await connection.send(h11.Request(method="GET", target="/", headers=BASIC_HEADERS))
    await connection.send(h11.EndOfMessage())
    await connection.transport.closed.wait()
    events = connection.get_events()
    response, *data, end = events
    assert isinstance(response, h11.Response)
    assert all(isinstance(datum, h11.Data) for datum in data)
    assert b"".join(datum.data for datum in data) == b"chunked data"
    assert isinstance(end, h11.EndOfMessage)


def test_max_incomplete_size() -> None:
    transport = MockTransport()
    config = Config()
    config.h11_max_incomplete_size = 5
    server = H11Server(Mock(), Mock(), config, transport)  # type: ignore
    server.data_received(b"GET / HTTP/1.1\r\nHost: hypercorn\r\n")  # Longer than 5 bytes
    assert transport.data.startswith(b"HTTP/1.1 400")


@pytest.mark.asyncio
async def test_initial_keep_alive_timeout(event_loop: asyncio.AbstractEventLoop) -> None:
    config = Config()
    config.keep_alive_timeout = 0.01
    server = H11Server(echo_framework, event_loop, config, Mock())
    await asyncio.sleep(2 * config.keep_alive_timeout)
    server.transport.close.assert_called()  # type: ignore


@pytest.mark.asyncio
async def test_post_response_keep_alive_timeout(event_loop: asyncio.AbstractEventLoop) -> None:
    config = Config()
    config.keep_alive_timeout = 0.01
    transport = MockTransport()
    server = H11Server(echo_framework, event_loop, config, transport)  # type: ignore
    server.pause_writing()
    server.data_received(b"GET / HTTP/1.1\r\nHost: hypercorn\r\n\r\n")
    await asyncio.sleep(2 * config.keep_alive_timeout)
    assert not transport.closed.is_set()
    server.resume_writing()
    await asyncio.sleep(2 * config.keep_alive_timeout)
    assert transport.closed.is_set()


@pytest.mark.asyncio
async def test_connection_error(event_loop: asyncio.AbstractEventLoop) -> None:
    # Key is that this works without any Exception being raised,
    # e.g. when trying to write to a errored connection.
    connection = MockConnection(event_loop)
    connection.server.pause_writing()
    await connection.send(h11.Request(method="GET", target="/", headers=BASIC_HEADERS))
    connection.server.connection_lost(Exception())
    connection.server.resume_writing()
    await connection.send(h11.EndOfMessage())
    await connection.transport.closed.wait()
