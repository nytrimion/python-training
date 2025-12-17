"""
Exercise 01: Sync vs Async comparison.

This module demonstrates the difference between synchronous
and asynchronous execution for I/O-bound operations.
"""

import asyncio
import time


def simulate_fetch_sync(url: str, delay: float = 0.5) -> dict:
    """Simulate a synchronous HTTP fetch with blocking sleep."""
    print(f"[SYNC] Fetching {url}...")
    time.sleep(delay)
    return {"url": url, "status": 200}


async def simulate_fetch_async(url: str, delay: float = 0.5) -> dict:
    """Simulate an asynchronous HTTP fetch with non-blocking sleep."""
    print(f"[ASYNC] Fetching {url}...")
    await asyncio.sleep(delay)
    return {"url": url, "status": 200}


# --- SYNC VERSION (provided) ---

def fetch_all_sync(urls: list[str]) -> list[dict]:
    """Fetch all URLs sequentially (blocking)."""
    results = []
    for url in urls:
        result = simulate_fetch_sync(url)
        results.append(result)
    return results


# --- ASYNC VERSION ---

async def fetch_all_async(urls: list[str]) -> list[dict]:
    """Fetch all URLs concurrently (non-blocking)."""
    return await asyncio.gather(*[simulate_fetch_async(url) for url in urls])


# --- BENCHMARK ---

def benchmark() -> None:
    """Compare execution times of sync vs async approaches."""
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/posts",
        "https://api.example.com/comments",
        "https://api.example.com/albums",
        "https://api.example.com/photos",
    ]

    print_header("SYNC VERSION", with_line_feed=False)
    start = time.perf_counter()
    sync_results = fetch_all_sync(urls)
    sync_duration = time.perf_counter() - start
    print(f"Results: {len(sync_results)} fetched")
    print(f"Duration: {sync_duration:.2f}s")

    print_header("ASYNC VERSION")
    start = time.perf_counter()
    async_results = asyncio.run(fetch_all_async(urls))
    async_duration = time.perf_counter() - start
    print(f"Results: {len(async_results)} fetched")
    print(f"Duration: {async_duration:.2f}s")

    print_header(f"Speedup: {sync_duration / async_duration:.1f}x faster with async")


def print_header(label: str, border: str = "=" * 50, with_line_feed: bool = True) -> None:
    """Print a header with given label."""
    if with_line_feed:
        print()
    print(border, label, border, sep="\n")


if __name__ == "__main__":
    benchmark()
