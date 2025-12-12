import sys
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class RequestLog:
    """Simulates logged request data."""

    request_id: int
    path: str
    payload: str


def calculate_memory_usage(logs: Iterable[RequestLog]) -> int:
    """Return approximate memory usage of logs in bytes."""
    return sys.getsizeof(logs) + sum(
        sys.getsizeof(log)
        + sys.getsizeof(log.request_id)
        + sys.getsizeof(log.path)
        + sys.getsizeof(log.payload)
        for log in logs
    )


def calculate_memory_usage_in_megabytes(logs: Iterable[RequestLog]) -> float:
    """Return approximate memory usage of logs in MB."""
    return calculate_memory_usage(logs) / (1024 * 1024)


class LeakyRequestLogger:
    """A logger that leaks memory by keeping all logs forever.

    This simulates a common mistake: accumulating data without cleanup.
    """

    def __init__(self) -> None:
        self._logs: list[RequestLog] = []

    def log(self, request_id: int, path: str, payload: str) -> None:
        """Log a request - but never clean up!"""
        self._logs.append(RequestLog(request_id, path, payload))

    def get_memory_usage(self) -> int:
        """Return approximate memory usage of logs in bytes."""
        return calculate_memory_usage(self._logs)

    @property
    def log_count(self) -> int:
        return len(self._logs)

    @property
    def memory_usage(self) -> float:
        return calculate_memory_usage_in_megabytes(self._logs)


class BoundedRequestLogger:
    """A logger that keeps memory stable by rotating logs."""

    def __init__(self, max_size: int = 1000) -> None:
        self._logs: deque[RequestLog] = deque(maxlen=max_size)

    def log(self, request_id: int, path: str, payload: str) -> None:
        """Log a request and rotates logs if required."""
        self._logs.append(RequestLog(request_id, path, payload))

    def get_memory_usage(self) -> int:
        """Return approximate memory usage of logs in bytes."""
        return calculate_memory_usage(self._logs)

    @property
    def log_count(self) -> int:
        return len(self._logs)

    @property
    def memory_usage(self) -> float:
        return calculate_memory_usage_in_megabytes(self._logs)


# Global singletons - lives forever in a long-running process!
leaky_logger = LeakyRequestLogger()
bounded_logger = BoundedRequestLogger()


def simulate_requests(count: int, payload_size: int = 1000) -> None:
    """Simulate incoming HTTP requests."""
    for i in range(count):
        path = f"/api/users/{i}"
        payload = "x" * payload_size  # Simulate request body

        # Each request logs data that is never cleaned up
        leaky_logger.log(i, path, payload)
        # Each request logs rotating data
        bounded_logger.log(i, path, payload)


if __name__ == "__main__":
    print("Simulating long-running process with memory leak...")

    for batch in range(1, 6):
        simulate_requests(count=10_000, payload_size=1000)
        print(f"\nAfter batch {batch}:")
        print(f"- Leaky logger: {leaky_logger.log_count:,} logs, ~{leaky_logger.memory_usage: .1f}MB")
        print(f"- Bounded logger: {bounded_logger.log_count:,} logs, ~{bounded_logger.memory_usage: .1f}MB")
