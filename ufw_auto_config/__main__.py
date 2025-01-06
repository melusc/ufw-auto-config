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

import logging
import os
from pathlib import Path

from . import ufw, plugins, error

logger = logging.getLogger(__name__)


def configure_logging():
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(filename=log_dir / "ufw-auto-config.log", level=logging.DEBUG)


def assert_root():
    uid = os.getuid()
    if uid != 0:
        raise PermissionError("ufw requires root.")


if __name__ == "__main__":
    configure_logging()

    try:
        assert_root()

        ufw.reset()
        plugins.configure()

        ufw.enable()

        status = ufw.status()
        print(status)
        logger.info(status)
    except error.UserError as e:
        print(f"Error: {e}")
        exit(1)
    except:
        import traceback

        logger.error(traceback.format_exc())
        raise
