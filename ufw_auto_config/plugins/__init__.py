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

from .openai import openai
from .censys import censys
from .user_config import user_config
from .ahrefs import ahrefs


def configure():
    openai()
    censys()
    ahrefs()

    # User config last
    # Other plugins use deny
    # If allows are before, it will not apply the deny
    user_config()
