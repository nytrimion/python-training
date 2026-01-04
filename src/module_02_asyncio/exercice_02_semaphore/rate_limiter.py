"""
Exercise 02: Rate limiting with Semaphore.

This module demonstrates how to limit concurrent operations
using asyncio.Semaphore to avoid overwhelming external services.
"""

import asyncio
import random
import time
from typing import Any


async def fetch_url(url: str, delay: float = 0.3) -> dict[str, Any]:
    """Simulate fetching a URL with variable delay."""
    actual_delay = delay + random.uniform(0, 0.2)  # 0.3 à 0.5s
    print(f"  -> Starting: {url}")
    await asyncio.sleep(actual_delay)
    print(f"  <- Finished: {url}")
    return {"url": url, "status": 200}


# TODO(human): Implement fetch_with_limit
# This function should:
# - Create an asyncio.Semaphore with max_concurrent slots
# - Define an inner async function that:
#   1. Acquires the semaphore (use 'async with semaphore:')
#   2. Calls fetch_url(url)
#   3. Returns the result
# - Use asyncio.gather() to run all fetches concurrently
#   (but limited by the semaphore)
#
# Expected behavior:
# - With 10 URLs and max_concurrent=3, only 3 fetches run at a time
# - Total time should be ~ceil(10/3) * 0.3s = ~1.2s (not 0.3s or 3s)


async def fetch_with_limit(
        urls: list[str],
        max_concurrent: int = 3,
) -> list[dict[str, Any]]:
    """
    Fetch all URLs with a maximum number of concurrent requests.

    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum number of simultaneous requests

    Returns:
        List of fetch results
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict[str, Any]:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(*(fetch_one(url) for url in urls))


async def demo() -> None:
    """Demonstrate the difference between unlimited and limited concurrency."""
    urls = [f"https://api.example.com/item/{i}" for i in range(10)]

    print_header("UNLIMITED CONCURRENCY (all 10 at once)", with_line_feed=False)
    start = time.perf_counter()
    await asyncio.gather(*[fetch_url(url) for url in urls])
    unlimited_duration = time.perf_counter() - start
    print(f"Duration: {unlimited_duration:.2f}s")

    print_header("LIMITED CONCURRENCY (max 3 at a time)")
    start = time.perf_counter()
    await fetch_with_limit(urls, max_concurrent=3)
    limited_duration = time.perf_counter() - start
    print(f"Duration: {limited_duration:.2f}s")

    print_header(
        f"Unlimited: {unlimited_duration:.2f}s (all parallel)",
        f"Limited:   {limited_duration:.2f}s (batches of 3)",
    )


def print_header(
        *labels: str, border: str = "=" * 60, with_line_feed: bool = True
) -> None:
    """Print a header with given label."""
    if with_line_feed:
        print()
    print(border, *labels, border, sep="\n")


if __name__ == "__main__":
    asyncio.run(demo())
