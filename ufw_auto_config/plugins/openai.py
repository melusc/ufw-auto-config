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

from schema import Schema, Use, And, Optional
from dataclasses import dataclass
import json
import logging

from ..get import get
from .. import ufw

logger = logging.getLogger(__name__)

# https://platform.openai.com/docs/bots/
lists = {
    "OAI-SearchBot": "https://openai.com/searchbot.json",
    "ChatGPT-User": "https://openai.com/chatgpt-user.json",
    "GPTBot": "https://openai.com/gptbot.json",
}


@dataclass
class IpRange:
    ipv4: str | None
    ipv6: str | None


schema = Schema(
    And(
        str,
        Use(json.loads),
        {
            "creationTime": str,
            "prefixes": [
                And(
                    {
                        Optional("ipv4Prefix"): str,
                        # Future proofing
                        # Only ipv4Prefix exists right now but
                        # for ipv6 this seems logical
                        Optional("ipv6Prefix"): str,
                    },
                    Use(
                        lambda prefix: IpRange(
                            ipv4=prefix.get("ipv4Prefix"), ipv6=prefix.get("ipv6Prefix")
                        )
                    ),
                )
            ],
        },
    ),
)


def openai():
    for name, url in lists.items():
        try:
            response = get(url, schema)
            logger.debug("name=%s, url=%s", name, url)
            prefixes: list[IpRange] = response["prefixes"]

            for prefix in prefixes:
                if prefix.ipv4 is not None:
                    ufw.deny(ip_range=prefix.ipv4, comment=name)
                if prefix.ipv6 is not None:
                    ufw.deny(ip_range=prefix.ipv6, comment=name)

        except:
            import traceback

            logger.error("name=%s, trace: %s", name, traceback.format_exc())

            # Ignore error, continue as normal
            # If json is different or remote is down,
            # we cannot do anything about it
