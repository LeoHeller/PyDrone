import asyncio
from typing import Optional


# noinspection PyAttributeOutsideInit
class MyProtocol(asyncio.Protocol):
    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"Connection lost! {exc}")

    def connection_made(self, transport) -> None:
        self.transport = transport

    def data_received(self, data):
        print(data)
        self.transport.write(data)

    def send(self, data):
        self.transport.write(data)


async def main(host, port):
    inp = ""
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(MyProtocol, host, port)
    protocol.send(b"hello world!")
    while inp != "quit":
        inp = input("> ")
        protocol.send(bytes(inp, encoding="utf-8"))


asyncio.run(main('127.0.0.1', 5000))

