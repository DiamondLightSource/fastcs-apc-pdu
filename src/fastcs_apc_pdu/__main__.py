# """Interface for ``python -m fastcs_apc_pdu``."""

# from argparse import ArgumentParser
# from collections.abc import Sequence

# from . import __version__

# __all__ = ["main"]


# def main(args: Sequence[str] | None = None) -> None:
#     """Argument parser for the CLI."""
#     parser = ArgumentParser()
#     parser.add_argument(
#         "-v",
#         "--version",
#         action="version",
#         version=__version__,
#     )
#     parser.parse_args(args)


# if __name__ == "__main__":
#     main()


from fastcs import launch

from fastcs_apc_pdu import __version__
from fastcs_apc_pdu.controller import APCPDUController

launch(APCPDUController, version=__version__)
