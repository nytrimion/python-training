"""Decorators demonstration."""

import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from typing import Any


# Benchmark decorator
def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that measures and prints execution time."""

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        value = func(*args, **kwargs)
        print(f"[timer] {func.__name__} took {time.perf_counter() - start:.2f}s")
        return value

    return inner


# Retry pattern
def retry(
        attempts: int, delay: float = 0.5
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    if attempts < 1:
        raise ValueError("[retry] attempts must be >= 1")
    if delay < 0:
        raise ValueError("[retry] Delay must be >= 0")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt >= attempts:
                        raise e
                    print(
                        f"[retry] {func.__name__} failed, attempt {attempt}/{attempts}"
                    )
                    time.sleep(delay)
            raise RuntimeError("[retry] Unreachable: attempts validation failed")

        return inner

    return decorator


# Timer context manager
@contextmanager
def timed_block(label: str) -> Generator[float, None, None]:
    start = time.perf_counter()
    try:
        yield start
    finally:
        duration = time.perf_counter() - start
        print(f"[timed_block] {label} took {duration:.2f}s")


# Test functions
@timer
def slow_operation(duration: float) -> str:
    """Simulate a slow operation."""
    time.sleep(duration)
    return "done"


@timer
def compute_sum(n: int) -> int:
    """Compute sum of numbers from 0 to n."""
    return sum(range(n))


@retry(attempts=3, delay=0.5)
def unreliable_api_call() -> str:
    """Simulate an API that fails randomly."""
    import random

    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("API unavailable")
    return "success"


if __name__ == "__main__":
    result = slow_operation(0.5)
    print(f"Result: {result}\n")

    result = compute_sum(1_000_000)
    print(f"Result: {result}")

    try:
        result = unreliable_api_call()
        print(f"API call: {result}")
    except Exception as e:
        print(f"API call error: {e}")

    with timed_block("data processing"):
        time.sleep(0.3)
        total = sum(range(1_000_000))
    print(f"Total: {total}")
