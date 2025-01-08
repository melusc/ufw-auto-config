from schema import Schema, And, Use, Optional
import json
from dataclasses import dataclass
import logging
from ipaddress import IPv4Network, IPv6Network

from .get import get
from . import ufw

logger = logging.getLogger(__name__)


@dataclass
class IpNetwork:
    ipv4: IPv4Network | None
    ipv6: IPv6Network | None


def _validate_ipv4(ipv4_cidr: str):
    network = IPv4Network(ipv4_cidr)
    # OpenAI has /22
    assert network.prefixlen >= 20 and network.is_global
    return network


def _validate_ipv6(ipv6_cidr: str):
    network = IPv6Network(ipv6_cidr)
    # censys has /80
    assert network.prefixlen >= 72 and network.is_global
    return network


_ip_range_schema = Schema(
    And(
        str,
        Use(json.loads),
        {
            "creationTime": str,
            "prefixes": [
                And(
                    {
                        Optional("ipv4Prefix"): And(
                            str,
                            Use(_validate_ipv4),
                        ),
                        Optional("ipv6Prefix"): And(
                            str,
                            Use(_validate_ipv6),
                        ),
                    },
                    Use(
                        lambda prefix: IpNetwork(
                            ipv4=prefix.get("ipv4Prefix"), ipv6=prefix.get("ipv6Prefix")
                        )
                    ),
                )
            ],
        },
    ),
)


def import_from_api(*, name: str, url: str):
    try:
        response = get(url, _ip_range_schema)
        logger.debug("name=%s, url=%s", name, url)
        prefixes: list[IpNetwork] = response["prefixes"]

        for prefix in prefixes:
            if prefix.ipv4 is not None:
                ufw.deny(ip_range=str(prefix.ipv4), comment=name)
            if prefix.ipv6 is not None:
                ufw.deny(ip_range=str(prefix.ipv6), comment=name)

    except:
        import traceback

        logger.error("name=%s, trace: %s", name, traceback.format_exc())

        # Ignore error, continue as normal
        # If json is different or remote is down,
        # we cannot do anything about it
