"""
This program is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation,
either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import subprocess
import logging
from typing import Literal

logger = logging.getLogger(__name__)


def _exec(args: tuple[str], *, stdin=b""):
    logger.info("$ ufw %s ; stdin=%s", " ".join(args), stdin)
    output = subprocess.run(["/usr/sbin/ufw", *args], capture_output=True, input=stdin)
    logger.info("-> %s", output)
    output.check_returncode()
    return output


def add_rule(
    type: Literal["allow"] | Literal["deny"],
    *,
    port: int = None,
    ip_range: str = None,
    comment: str = None,
):
    if type not in ("allow", "deny"):
        raise ValueError(f"Unknown directivy {type}")

    args = ()

    if port is not None:
        args += (str(port),)

    if ip_range is not None:
        args += ("from", ip_range)

    if not args:
        raise ValueError("Invalid arguments. Must specify port or ip range.")

    if comment is not None:
        args += ("comment", comment)

    _exec((type, *args))


def allow(*, port: int = None, ip_range: str = None, comment: str = None):
    add_rule("allow", port=port, ip_range=ip_range, comment=comment)


def deny(*, port: int = None, ip_range: str = None, comment: str = None):
    add_rule("deny", port=port, ip_range=ip_range, comment=comment)


def enable():
    # Always allow ssh as a fail-safe
    logger.debug("Enabling SSH as a fail-safe.")
    allow(port=22, comment="SSH")

    logger.debug("Enabling UFW.")
    _exec(("enable",), stdin=b"y\n")


def reset():
    _exec(("reset",), stdin=b"y\n")


def status():
    return _exec(("status",)).stdout.decode("utf8")
