from fastcs.attributes import AttributeIO, AttributeIORef, AttrR
from fastcs.controllers import Controller
from fastcs.datatypes import Bool
from fastcs.util import ONCE

from fastcs_apc_pdu.connection import APCPDUConnection
from fastcs_apc_pdu.protocol import APCPDUProtocol

# Hardcoded for testing only - replace with real config/env vars later.
HOST = "172.23.91.223"
PORT = 23
USERNAME = "apc"
PASSWORD = "b21staff"
OUTLET = 1

protocol = APCPDUProtocol()


class OutletStatusIORef(AttributeIORef):
    def __init__(self, connection: APCPDUConnection, outlet: int) -> None:
        super().__init__(update_period=ONCE)
        self.connection = connection
        self.outlet = outlet


class OutletStatusIO(AttributeIO[bool, OutletStatusIORef]):
    async def update(self, attr: AttrR[bool, OutletStatusIORef]) -> None:
        response = await attr.io_ref.connection.send_query(
            protocol.get_outlet_status(attr.io_ref.outlet)
        )
        await attr.update(protocol.read_outlet_status(response))


class APCPDUController(Controller):
    def __init__(self) -> None:
        self.conn = APCPDUConnection(
            host=HOST, port=PORT, username=USERNAME, password=PASSWORD
        )
        super().__init__(ios=[OutletStatusIO()])

        self.outlet_1_state = AttrR(
            Bool(),
            io_ref=OutletStatusIORef(self.conn, OUTLET),
            description="State of outlet 1",
        )

    async def connect(self) -> None:
        await self.conn.connect()
        await super().connect()
