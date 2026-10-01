# Test the connection to the APC PDU
# Can be run with
# cd fastcs-apc-pdu
# uv sync
# uv run python tests/test_connection.py

import asyncio

from fastcs_apc_pdu.connection import APCPDUConnection


async def test():
    connection = APCPDUConnection(
        host="172.23.91.223",
        port=23,
        username="apc",
        password="b21staff",
    )

    await connection.connect()
    print("Connected and logged in")

    response = await connection.send_query("?")
    print("APC response:")
    print(response)


asyncio.run(test())
