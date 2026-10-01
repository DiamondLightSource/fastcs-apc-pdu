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

    response, _ = await connection.send_command("?", check_success=False)
    print("? response:")
    print(response)

    protocol = APCPDUProtocol()

    # Test turning on outlet 1, checking status, turning off outlet 1,
    # checking status again, and checking load current

    response, _ = await connection.send_command(protocol.command_outlet_on(1))
    print("command_outlet_on(1) response:")
    print(response)

    response, parsed = await connection.send_command(
        protocol.command_outlet_status(1), parser=protocol.parse_outlet_status
    )
    print("command_outlet_status(1) response:")
    print(response)
    print(f"command_outlet_status(1) parsed: {parsed}")

    response, _ = await connection.send_command(protocol.command_outlet_off(1))
    print("command_outlet_off(1) response:")
    print(response)

    response, parsed = await connection.send_command(
        protocol.command_outlet_status(1), parser=protocol.parse_outlet_status
    )
    print("command_outlet_status(1) response:")
    print(response)
    print(f"command_outlet_status(1) parsed: {parsed}")

    response, parsed = await connection.send_command(
        protocol.command_load_current(), parser=protocol.parse_load_current
    )
    print("command_load_current() response:")
    print(response)
    print(f"command_load_current() parsed: {parsed}")


asyncio.run(test())
