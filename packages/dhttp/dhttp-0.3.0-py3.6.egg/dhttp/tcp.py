import socket
import itertools
import socket as socketlib
import random
import collections
import unittest
import io
import inspect
import queue
import atexit
import trio



class DequeBytesIO(io.IOBase):
    def __init__(self, data = None, cursor = 0):
        if data is None:
            self._buffer = collections.deque()

        else:
            self._buffer = collections.deque([data])

        self.cursor = max(0, min(len(self), cursor))

    def ensure_bytes(self, data, string_mode=None):
        if isinstance(data, bytes):
            return data

        elif isinstance(data, str):
            return data.encode('utf-8')

        elif string_mode == 'str':
            return str(data).encode('utf-8')

        elif string_mode == 'repr':
            return repr(data).encode('utf-8')

        else:
            raise TypeError("A bytes or byte-encodable value is required, not " + type(data).__name__ + "!")

    def index_at(self, position):
        remaining = position

        for index in range(len(self._buffer)):
            p = len(self._buffer[index])

            if p > remaining:
                return (index, remaining)

            else:
                remaining -= p

        return (index + 1, remaining)

    def buffer(self):
        return io.BytesIO(sum(self._buffer))

    def _get(self, ind):
        if ind < len(self._buffer):
            return self._buffer[ind]

        return b''

    def cap_position(self, pos):
        if pos < 0:
            pos = len(self) - pos

        return min(pos, len(self))

    def slice(self, start_pos = 0, end_pos = None):
        if end_pos is None:
            end_pos = len(self)

        start_pos = self.cap_position(start_pos)
        end_pos = self.cap_position(end_pos)

        if start_pos == end_pos:
            return None

        start = self.index_at(start_pos)
        end = self.index_at(end_pos)

        if start[0] == end[0]:
            return self._get(start[0])[start[1]:end[1]]
        
        else:
            res = b''

            if abs(start[0] - end[0]) > 1:
                for index in range(start[0] + 1, end[0]):
                    res += self._get(index)

            return self._get(start[0])[start[1]:] + res + self._get(end[0])[:end[1]]

    def __len__(self):
        return sum(len(x) for x in self._buffer)

    def remaining(self):
        return len(self) - self.cursor

    def cap_seek(self):
        self.seek(self.cursor) # automatically caps to content limits

    def truncate_right(self, amount = None):
        if amount is None:
            amount = self.cursor

        elif amount < 0:
            amount = len(self) - amount

        (tind, tpos) = self.index_at(amount)

        self._buffer = collections.deque(itertools.islice(self._buffer, tind))
        self.cap_seek()

        if len(self._buffer) > 0:
            self._buffer[-1] = self._buffer[-1][:tpos]

    def truncate(self, amount = None):
        self.truncate_left(amount)

    def truncate_left(self, amount = None):
        if amount is None:
            amount = self.cursor
        
        elif amount < 0:
            amount = len(self) - amount

        (tind, tpos) = self.index_at(amount)

        self._buffer = collections.deque(itertools.islice(self._buffer, tind, None))
        self.seek_toward(-amount)

        if len(self._buffer) > 0:
            self._buffer[0] = self._buffer[0][tpos:]

    def __str__(self, encoding='utf-8'):
        return sum(self._buffer).decode(encoding)
    
    def __bytes__(self):
        return sum(self._buffer)

    def write(self, data, seek = False):
        self._buffer.append(self.ensure_bytes(data))

        if seek:
            self.cursor += len(data)

    def write_left(self, data):
        self._buffer.appendleft(self.ensure_bytes(data))
        self.cursor += len(data)

    async def read_least(self, queue, size = None, pos = None, seek = True):
        if pos is None:
            pos = self.cursor

        if size is None:
            size = len(self) - pos

        wait_cursor = pos

        await trio.sleep(0.1)

        while True:
            d = self.slice(wait_cursor, pos + size)

            if d != b'':
                queue.put(d)
                wait_cursor += len(d)

            if seek:
                self.cursor = wait_cursor

            if wait_cursor >= pos + size:
                break
                
            await trio.sleep(0.05)

        queue.put(None)

    def read_all(self):
        res = b''
        
        for data in self._buffer:
            res += data
        
        return res

    def read(self, size = None, pos = None, seek = True):
        if pos is None:
            pos = self.cursor

        pos = self.cap_position(pos)

        if size is None:
            size = len(self) - pos
        
        data = self.slice(pos, pos + size)

        if data is None:
            return None

        if seek:
            self.seek_toward(len(data))
        
        return data

    def seek(self, at):
        self.cursor = self.cap_position(at)

    def seek_toward(self, at):
        return self.seek(at + self.cursor)

    def tell(self):
        return self.cursor


class AsyncTCPClient(object):
    def __init__(self, host = None):
        self.socket = socket.socket(socketlib.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)

        self.host = host
        self._read_buffer = DequeBytesIO()
        self._write_buffer = DequeBytesIO()

    async def loop(self):
        while True:
            sleep_amount = 0.02

            try:
                data = self.socket.recv(1024)

            except socket.error:
                sleep_amount = 0.1

            self._read_buffer.write(data)
            
            self._write_buffer.poll()

            trio.sleep(sleep_amount)

    async def connect(self, host = None):
        host = host or self.host

        if host is None:
            raise ValueError('AsyncTCPClient: Both the default host (given on construction) and connect.host are None.')

        else:
            self.socket.connect(host)
            await self.loop()

class AsyncTCPServer(object):
    class Client(object):
        def __init__(self, server, socket, addr):
            self.server = server
            self.address = addr
            self.socket = socket

            self.out_buffer = DequeBytesIO()
            self.in_buffer = DequeBytesIO()

            self._pending_close = False
            self.closed = False

            self._receivers = set()

        def verify_close(self):
            if self.closed:
                raise TCPClientError("The client socket was already closed!")

        def receiver(self, func):
            self._receivers.add(func)
            return func

        def write(self, data):
            self.verify_close()
            self.out_buffer.write(data)

        def close(self):
            self._pending_close = True

        def _close(self):
            self.socket.close()
            self.closed = True

        def poll(self):
            data = self.read()
            self.truncate_left()

            return data

        def read(self, data):
            data = self.in_buffer.read()
            self.in_buffer.truncate_left()

            return data

        async def receive(self, data):
            if data == b'':
                self._close()

            else:
                self.in_buffer.write(data)

                async with trio.open_nursery() as nursery:
                    for f in self._receivers | self.server._receivers:
                        if inspect.iscoroutinefunction(f):
                            nursery.start_soon(f, self, data)

                        else:
                            f(self, data)

    def __init__(self):
        self._on_accept = set()
        self._receivers = set()

        self.running = False

    def stop(self):
        self.running = False

    def receiver(self, func):
        self._receivers.add(func)
        return func

    def on_accept(self, func):
        self._on_accept.add(func)

        return func

    async def serve(self, client):
        pass

    def _wrap_client(self, socket, addr):
        client = AsyncTCPServer.Client(self, socket, addr)

        return client

    async def _accept(self, socket, addr):
        client = self._wrap_client(socket, addr)

        async with trio.open_nursery() as nursery:
            nursery.start_soon(self._run_client, client)
            nursery.start_soon(self.serve, client)

            rest = set()

            for f in self._on_accept:
                if inspect.iscoroutinefunction(f):
                    nursery.start_soon(f, client)

                else:
                    rest.add(f)

            for f in rest:
                f(client)

    async def _run_client(self, client):
        client.socket.setblocking(False)

        while (not client.closed) and self.running:
            sleep_amount = 0.05

            try:
                if not client._pending_close:
                    data = client.socket.recv(1024)
                    if data == '': break

                else:
                    sleep_amount = 0.075

                await client.receive(data)

                if client.closed:
                    break

            except socketlib.error:
                sleep_amount = 0.2
            
            if client.out_buffer.remaining() > 0:
                data = client.out_buffer.read(1024)
                sent = client.socket.send(data)

                client.out_buffer.seek_toward(sent - len(data))
                client.out_buffer.truncate_left()

            else:
                if client._pending_close:
                    client._close()

                sleep_amount *= 1.5

            await trio.sleep(sleep_amount)

        if not client.closed:
            client._close()
        
    async def run(self, port, host='127.0.0.1'):
        self.running = True

        async with trio.open_nursery() as nursery:
            listen_socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
            listen_socket.bind((host, port))

            listen_socket.listen(5)

            listen_socket.setblocking(False)

            _run = True

            @atexit.register
            def _at_exit():
                if _run:
                    self.running = False
                    listen_socket.close()
            
            while self.running:
                try:
                    (socket, addr) = listen_socket.accept()
                    nursery.start_soon(self._accept, socket, addr)

                    sleep_amount = 0.1

                except socketlib.error:
                    sleep_amount = 0.25

                await trio.sleep(sleep_amount)

            _run = False
            listen_socket.close()

    def run_forever(self, port, host='127.0.0.1'):
        trio.run(self.run, port, host)


class TCPClientError(BaseException):
    pass


#===


class EchoServerTest(object):
    async def run_serv(self, callback):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.server.run, self.port)
            nursery.start_soon(callback)

    def __init__(self, port = None):
        if port is None:
            port = random.randint(7000, 7999)

        self.port = int(port)
        self.server = AsyncTCPServer()

        @self.server.receiver
        async def receive(client, data):
            client.write(data + data)

        class EchoServerTestCase(unittest.TestCase):
            def test_double_echo(case):
                async def run():
                    async def run_test():
                        cl = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)

                        connected = False
                        while not connected:
                            try:
                                cl.connect(('127.0.0.1', self.port))
                                connected = True

                            except socket.error:
                                await trio.sleep(0.2)

                        cl.sendall(b'MyTest')
                        cl.setblocking(False)

                        data = b''

                        while True:
                            try:
                                nd = cl.recv(1024)

                                if nd == b'':
                                    break

                                else:
                                    data += nd
                                    cl.close()

                                    await trio.sleep(0.1)
                                    break

                            except socketlib.error:
                                await trio.sleep(0.2)

                        case.assertEqual(len(data), 2 * len(b'MyTest'))
                        case.assertEqual(data, b'MyTestMyTest')

                        self.server.stop()

                    async def callback():
                        await run_test()

                    await self.run_serv(callback)

                trio.run(run)

            def test_read_least(case):
                print()
                buf = DequeBytesIO()

                async def put_wait():
                    def write(data):
                        buf.write(data)
                        print(' --> ', data)

                    write(b'A')
                    await trio.sleep(0.3)
                    write(b'BC')
                    await trio.sleep(1.2)
                    write(b'DEF')
                    await trio.sleep(1)
                    write(b'GHI')
                    await trio.sleep(1.5)
                    write(b'JKL')

                async def read_wait():
                    q = queue.Queue()
                    res = b''
                    waits = 0

                    async with trio.open_nursery() as nursery:
                        nursery.start_soon(buf.read_least, q, 8)
                        await trio.sleep(0.1)

                        while True:
                            if not q.empty():
                                data = q.get_nowait()

                                if data is None:
                                    break

                                else:
                                    res += data
                                    waits += 1

                                print(data, res)

                            await trio.sleep(0.25)

                        print()
                        print('-----')
                        print()
                        print('result:', res)
                        print()
                        print('-----')

                        case.assertEqual(len(res), 8)
                        case.assertEqual(res, b'ABCDEFGH')
                        case.assertEqual(waits, 4)

                async def run_test():
                    async with trio.open_nursery() as nursery:
                        nursery.start_soon(read_wait)
                        nursery.start_soon(put_wait)

                trio.run(run_test)

        self.TestCase = EchoServerTestCase

    def run(self):
        unittest.main(self.TestCase())

if __name__ == "__main__":
    EchoServerTest().run()