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

from schema import Schema, Optional, Or, And, Use
from yaml import load, SafeLoader
from pathlib import Path
from dataclasses import dataclass

from .. import ufw


@dataclass
class RuleSet:
    port: list[int]
    ip: list[str]


@dataclass
class Config:
    allow: RuleSet
    deny: RuleSet


config_schema = Schema(
    And(
        {
            Optional(Or("allow", "deny")): And(
                {
                    Optional("port"): [int],
                    Optional("ip"): [str],
                },
                Use(
                    lambda rule: RuleSet(
                        port=rule.get("port", []),
                        ip=rule.get("ip", []),
                    )
                ),
            )
        },
        Use(
            lambda config: Config(
                allow=config.get("allow", RuleSet([], [])),
                deny=config.get("deny", RuleSet([], [])),
            )
        ),
    )
)


def _load_config() -> Config:
    config_path = Path(__file__).parent.parent.parent / "config.yml"

    with config_path.open("r") as f:
        config = load(f, Loader=SafeLoader)

        return config_schema.validate(config)


def user_config():
    config = _load_config()

    comment = "User config.yml"

    for port in config.deny.port:
        ufw.deny(port=port, comment=comment)

    for ip in config.deny.ip:
        ufw.deny(ip_range=ip, comment=comment)

    for port in config.allow.port:
        ufw.allow(port=port, comment=comment)

    for ip in config.allow.ip:
        ufw.allow(ip_range=ip, comment=comment)
