import re

_OUTLET_STATUS_RE = re.compile(
    r"^\s*[1-8]:\s*Outlet\s+[1-8]:\s*(On|Off)(\*)?",
    re.MULTILINE,
)
_LOAD_CURRENT_RE = re.compile(r"^\d+:\s*([\d.]+)\s*A", re.MULTILINE)


class APCPDUProtocol:
    # Outlet status
    def command_outlet_status(self, outlet: str) -> str:
        """Command to get the status of a specific outlet."""
        return f"olStatus {outlet}"

    def parse_outlet_status(self, response: str) -> tuple[str, bool]:
        """Parse the response to get the status of outlet.
        the boolean indicates whether the outlet is pending (True) or not (False)."""
        match = _OUTLET_STATUS_RE.search(response)
        if match is None:
            raise ValueError(f"Invalid response format: {response!r}")
        return match.group(1), match.group(2) == "*"

    # Commands to control outlets
    def command_outlet_cancel(self, outlet: str) -> str:
        """Command to cancel pending commandson an outlet."""
        return f"olCancelCmd {outlet}"

    def command_outlet_on(self, outlet: str) -> str:
        """Command to turn on an outlet."""
        return f"olOn {outlet}"

    def command_outlet_off(self, outlet: str) -> str:
        """Command to turn off an outlet."""
        return f"olOff {outlet}"

    def command_outlet_reboot(self, outlet: str) -> str:
        """Command to reboot an outlet."""
        return f"olReboot {outlet}"

    def command_outlet_delay_on(self, outlet: str) -> str:
        """Command to turn on an outlet after a delay."""
        return f"olDlyOn {outlet}"

    def command_outlet_delay_off(self, outlet: str) -> str:
        """Command to turn off an outlet after a delay."""
        return f"olOff {outlet}"

    def command_outlet_delay_reboot(self, outlet: str) -> str:
        """Command to reboot an outlet after a delay."""
        return f"olDlyReboot {outlet}"

    # Commands to configure outlets
    def command_get_outlet_name(self, outlet: int) -> str:
        """Command to get the name of a specific outlet."""
        return f"olName {outlet}"

    def command_set_outlet_name(self, outlet: int, name: str) -> str:
        """Command to set the name of a specific outlet."""
        return f"olName {outlet} {name}"

    def command_get_outlet_on_delay(self, outlet: int) -> str:
        """Command to get the power-on delay of a specific outlet."""
        return f"olOnDelay {outlet}"

    def command_set_outlet_on_delay(self, outlet: int, delay: int) -> str:
        """Command to set the power-on delay of a specific outlet."""
        return f"olOnDelay {outlet} {delay}"

    def command_get_outlet_off_delay(self, outlet: int) -> str:
        """Command to get the power-off delay of a specific outlet."""
        return f"olOffDelay {outlet}"

    def command_set_outlet_off_delay(self, outlet: int, delay: int) -> str:
        """Command to set the power-off delay of a specific outlet."""
        return f"olOffDelay {outlet} {delay}"

    def command_get_outlet_reboot_time(self, outlet: int) -> str:
        """Command to get the reboot time of a specific outlet."""
        return f"olRbootTime {outlet}"

    def command_set_outlet_reboot_time(self, outlet: int, time: int) -> str:
        """Command to set the reboot time of a specific outlet."""
        return f"olRbootTime {outlet} {time}"

    # Load current
    def command_load_current(self) -> str:
        """Command to get the load current."""
        return "phReading all current"

    def parse_load_current(self, response: str) -> float:
        """Parse the response to get the load current."""
        match = _LOAD_CURRENT_RE.search(response)
        if match is None:
            raise ValueError(f"Invalid response format: {response!r}")
        return float(match.group(1))
