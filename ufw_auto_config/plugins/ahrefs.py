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

from ..ip_range_api import import_from_api

# https://docs.ahrefs.com/docs/api/public/operations/list-crawler-ip-ranges
api_url = "https://api.ahrefs.com/v3/public/crawler-ip-ranges"


def ahrefs():
    import_from_api(name="AhrefsBot", url=api_url)
