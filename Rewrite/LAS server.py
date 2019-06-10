import asyncio
from typing import Optional

global protocol
# noinspection PyAttributeOutsideInit
class MyProtocol(asyncio.Protocol):
    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"Connection lost! {exc}")

    def connection_made(self, transport) -> None:
        self.transport = transport
        protocol = self

    def data_received(self, data):
        print(data)
        self.transport.write(data)


async def main(host, port):
    protocol = None
    loop = asyncio.get_running_loop()
    server = await loop.create_server(MyProtocol, host, port)

    await server.start_serving()
    inp = ""
    while inp != "quit":
        inp = input("> ")
        protocol.send(bytes(inp, encoding="utf-8"))

asyncio.run(main('127.0.0.1', 5000))

