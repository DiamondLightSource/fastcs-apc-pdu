# Test the connection to the APC PDU
# Can be run with
# cd fastcs-apc-pdu
# uv sync
# uv run python tests/test_connection.py

import asyncio

from fastcs_apc_pdu.connection import APCPDUConnection
from fastcs_apc_pdu.protocol import APCPDUProtocol


async def test():
    connection = APCPDUConnection(
        host="172.23.91.223",
        port=23,
        username="apc",
        password="b21staff",
    )

    await connection.connect()
    print("Connected and logged in")

    response = await connection.send_command("?", check_success=False)
    print("? response:")
    print(response)

    protocol = APCPDUProtocol()

    response = await connection.send_command(protocol.get_outlet_status(1))
    print("get_outlet_status(1) response:")
    print(response)


asyncio.run(test())
