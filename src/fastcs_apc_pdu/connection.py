import asyncio

PROMPT: bytes = b"apc>"
USER_PROMPT: bytes = b"User Name"
PASSWORD_PROMPT: bytes = b"Password"


class APCPDUConnection:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        await self._read_until(USER_PROMPT)
        await self._write_line(self.username)
        await self._read_until(PASSWORD_PROMPT)
        await self._write_line(self.password)
        await self._read_until(PROMPT)

    async def send_query(self, command: str) -> str:
        await self._write_line(command)
        return await self._read_until(PROMPT)

    async def _write_line(self, text: str) -> None:
        assert self._writer is not None
        self._writer.write(f"{text}\r\n".encode())
        await self._writer.drain()

    async def _read_until(self, marker: bytes) -> str:
        assert self._reader is not None
        data = await self._reader.readuntil(marker)
        return data.decode(errors="replace")
