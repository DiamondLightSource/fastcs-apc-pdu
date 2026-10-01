import re

_OUTLET_STATUS_RE = re.compile(r"^\s*[1-8]:\s*Outlet\s+[1-8]:\s*(On|Off)", re.MULTILINE)
_LOAD_CURRENT_RE = re.compile(r"^\d+:\s*([\d.]+)\s*A", re.MULTILINE)


class APCPDUProtocol:
    def command_outlet_on(self, outlet: int) -> str:
        """Command to turn on an outlet."""
        return f"olOn {outlet}"

    def command_outlet_off(self, outlet: int) -> str:
        """Command to turn off an outlet."""
        return f"olOff {outlet}"

    def command_outlet_status(self, outlet: int) -> str:
        """Command to get the status of a specific outlet."""
        return f"olStatus {outlet}"

    def parse_outlet_status(self, response: str) -> str:
        """Parse the response to get the status of outlet."""
        match = _OUTLET_STATUS_RE.search(response)
        if match is None:
            raise ValueError("Invalid response format: {response!r}")
        return match.group(1)

    def command_load_current(self) -> str:
        """Command to get the load current."""
        return "phReading all current"

    def parse_load_current(self, response: str) -> float:
        """Parse the response to get the load current."""
        match = _LOAD_CURRENT_RE.search(response)
        if match is None:
            raise ValueError("Invalid response format: {response!r}")
        return float(match.group(1))
