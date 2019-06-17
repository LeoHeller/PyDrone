import asyncio
from typing import Optional

# noinspection PyAttributeOutsideInit
class MyServerProtocol(asyncio.Protocol):
    def connection_lost(self, exc: Optional[Exception]) -> None:
        print(f"Connection lost! {exc}")

    def connection_made(self, transport) -> None:
        self.transport = transport

    def data_received(self, data):
        print(data)
        self.transport.write(data)


async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(MyServerProtocol, host, port)
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
