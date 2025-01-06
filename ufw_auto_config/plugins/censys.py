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


from .. import ufw
from pathlib import Path

# https://about.censys.io
# https://support.censys.io/hc/en-us/articles/360043177092-Opt-Out-of-Data-Collection
ranges_path = Path(__file__).parent / 'censys_scanning_ranges.txt'

def censys():
    with ranges_path.open('r') as f:
        for ip_range in f:
            if ip_range := ip_range.strip():
                ufw.deny(ip_range=ip_range, comment="censys.io")
