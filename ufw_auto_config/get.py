from schema import Schema
import requests
from pathlib import Path
import json
from time import time
from datetime import timedelta
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

cache_dir = Path(__file__).parent.parent / ".cache"
cache_max_age = timedelta(hours=1)

filename_safe_characters = (" ", ".", "_", "-")


"""
Caches results to .cache/
Use cache to:
- Not get rate limited.
- Be able to handle remote server going down
- If remote file format changes use cache
"""


def _to_filename_safe(raw: str) -> str:
    return "".join(
        c if c.isalnum() or c in filename_safe_characters else "_" for c in raw
    )


@dataclass
class CacheResult:
    age: timedelta
    body: str


def read_cache(filename: str) -> CacheResult | None:
    """
    Return cache result even if it already expired
    """

    cache_path = cache_dir / filename

    try:
        with cache_path.open("r") as f:
            result = json.load(f)
            age = time() - result["cacheTime"]
            return CacheResult(body=result["body"], age=timedelta(seconds=age))
    except:
        cache_path.unlink(missing_ok=True)

    return None


def write_cache(filename: str, body: str):
    cache_dir.mkdir(exist_ok=True)
    cache_path = cache_dir / filename

    with cache_path.open("w") as f:
        json.dump(
            {
                "cacheTime": int(time()),
                "body": body,
            },
            f,
        )


def get(url: str, schema: Schema):
    """
    Try these in order
    1. Return cache if it is not too old
    2. Get URL and return that if it matches schema
    3. Return cache even if it is too old

    Let all exceptions bubble
    """

    logger.debug("get(url: %s)", url)
    filename = _to_filename_safe(url)

    cache_result = read_cache(filename)

    if cache_result is not None and cache_result.age < cache_max_age:
        logger.debug("Cache-hit %s", url)
        try:
            return schema.validate(cache_result.body)
        except:
            pass

    try:
        logger.debug("Downloading %s", url)
        response = requests.get(url)
        response.raise_for_status()

        body = response.text

        result = schema.validate(body)
        write_cache(filename, body)
        return result
    except:
        import traceback

        logger.error(traceback.print_exc())

        # Doesn't matter that cache is too old
        # Use expired cache if server is temporarily down
        # Use expired cache until dev can fix schema or issue
        if cache_result is not None:
            return schema.validate(cache_result.body)

        raise
