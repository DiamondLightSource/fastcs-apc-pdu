import asyncio

# Prompts
USERNAME_PROMPT: bytes = b"User Name"
PASSWORD_PROMPT: bytes = b"Password"
PROMPT: bytes = b"apc>"

# Telnet commands
IAC: int = 0xFF
WILL: int = 0xFB
WONT: int = 0xFC
DO: int = 0xFD
DONT: int = 0xFE
# Eg
# IAC WILL ECHO = b"\xFF\xFB\x01"
# IAC WONT ECHO = b"\xFF\xFC\x01"
# IAC IAC = b"\xFF\xFF" means a literal 0xFF in the data stream, not a command


class APCPDUConnection:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    """
    Connects to the APC PDU via Telnet, logs in, gets to the apc prompt.
    """

    async def connect(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        await self._read_until(USERNAME_PROMPT)
        await self._write_line(self.username)
        await self._read_until(PASSWORD_PROMPT)
        await self._write_line(self.password)
        await self._read_until(PROMPT)

    """
    Sends a command to the APC PDU and returns the response as a string.
    """

    async def send_command(self, command: str, check_success: bool = True) -> str:
        await self._write_line(command)
        response = await self._read_until(PROMPT)
        if check_success:
            self.check_success(response)
        return response

    """
    Checks if the response indicates success. Raises ValueError if not.
    """

    def check_success(self, response: str) -> None:
        if "E000: Success" not in response:
            raise ValueError(f"APC command failed: {response!r}")

    """
    Writes a line + carriage return, newline to the connection.
    """

    async def _write_line(self, text: str) -> None:
        assert self._writer is not None
        self._writer.write(f"{text}\r\n".encode())
        await self._writer.drain()

    """
    Reads from the connection until the end marker.
    If get a Telnet command (IAC sequence) then process.
    If not a Telnet command, regard as data, return as string.
    """

    async def _read_until(self, end_marker: bytes) -> str:
        assert self._reader is not None

        data = bytearray()

        while end_marker not in data:
            byte = await self._reader.readexactly(1)

            if byte[0] == IAC:
                data.extend(await self._handle_telnet_command())
            else:
                data.extend(byte)

        return bytes(data).decode(errors="replace")

    async def _handle_telnet_command(self) -> bytes:
        assert self._reader is not None
        assert self._writer is not None

        command = (await self._reader.readexactly(1))[0]

        if command == IAC:
            # IAC IAC is actually not a command but a literal 0xFF in application data.
            return bytes([IAC])

        if command in (WILL, WONT, DO, DONT):
            # Eg, IAC WILL ECHO = b"\xFF\xFB\x01"
            option = (await self._reader.readexactly(1))[0]

            # If device says it WILL do something, eg, IAC WILL ECHO, we say DONT do it.
            if command == WILL:
                self._writer.write(bytes([IAC, DONT, option]))
                await self._writer.drain()

            # If device says DO something, we say WONT do it.
            elif command == DO:
                self._writer.write(bytes([IAC, WONT, option]))
                await self._writer.drain()

            # Ignore WONT and DONT commands, no response needed.

        # Ignore other one-byte Telnet commands

        return b""
