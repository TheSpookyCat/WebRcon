import asyncio
import json
import websockets

from .exceptions import InvalidServer, ConnectionClosed
from .utils import maybe_await


# noinspection SpellCheckingInspection
class RconConnector:
    # noinspection PyTypeChecker
    def __init__(self, host, port, password, message_callback=None, console_callback=None):
        self.uri = f'ws://{host}:{port}/{password}'
        self.ws: websockets.WebSocketClientProtocol = None
        self._loop = None
        self._ws_kwargs = {}
        self._counter = 1
        self._process_task: asyncio.Future = None
        self._bucket = {}
        self._closed = True
        if message_callback and not callable(message_callback):
            raise TypeError('Expected type `function` for `message_callback`, got type `{0}`'.format(
                type(message_callback)))
        elif message_callback:
            self._bucket[-1] = message_callback
        if console_callback and not callable(console_callback):
            raise TypeError('Expected type `function` for `console_callback`, got type `{0}`'.format(
                type(console_callback)))
        elif console_callback:
            self._bucket[0] = console_callback

    async def start(self, loop, **kwargs):
        self._loop = loop
        try:
            self.ws = await websockets.connect(self.uri, **kwargs)
            self._ws_kwargs = kwargs
            self._closed = False
            if self._process_task:
                self._process_task.cancel()
            self._process_task = self._loop.create_task(self.receive_data())
        except websockets.WebSocketProtocolError:
            raise InvalidServer

    async def close(self):
        self._closed = True
        await self.ws.close(reason='Client requested shutdown of WS connection.')

    async def command(self, command, callback):
        if not callable(callback):
            raise TypeError('Expected type `function` for `message_callback`, got type `{0}`'.format(
                type(callback)))
        if self._closed:
            raise ConnectionClosed
        self._bucket[self._counter] = callback
        data = json.dumps(dict(Message=command, Identifier=self._counter, Name="WebRcon"))
        self._counter += 1
        retry_counter = 0
        sent = False
        while not sent:
            try:
                await self.ws.send(data)
                sent = True
            except websockets.ConnectionClosed:
                await asyncio.sleep((retry_counter + 1) * 5)
                retry_counter += 1
                await self.start(self._loop, **self._ws_kwargs)
            except (websockets.WebSocketProtocolError, websockets.InvalidHandshake):
                await asyncio.sleep((retry_counter + 1) * 5)
                retry_counter += 1
            if retry_counter >= 5:
                # Could not reconnect / send the data
                return False
        return True

    async def receive_data(self):
        # noinspection DuplicatedCode
        closed_counter = 0
        while not self._closed:
            data = {}
            try:
                resp = await self.ws.recv()
                data = json.loads(resp)
            except websockets.ConnectionClosed:
                closed_counter += 1
                if closed_counter >= 3:
                    await self.start(self._loop, **self._ws_kwargs)
            except json.JSONDecodeError:
                # Invalid response, ignore
                pass

            identifier = data.get('Identifier')
            if identifier == -1 and self._bucket.get(-1):
                await maybe_await(self._bucket[-1], data)
            elif identifier == 0 and self._bucket.get(0):
                await maybe_await(self._bucket[0], data)
            elif identifier in self._bucket:
                await maybe_await(self._bucket[identifier], data)
                del self._bucket[identifier]
