"""HTTP log analyzer using idiomatic Python patterns."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from statistics import mean


@dataclass
class HttpLog:
    """Represents a single HTTP request log entry."""

    timestamp: str
    method: str  # GET, POST, PUT, DELETE
    path: str
    status_code: int
    response_time_ms: int
    user_id: int | None


# Sample data for testing
SAMPLE_LOGS: list[HttpLog] = [
    HttpLog("2024-01-15T10:00:00", "GET", "/api/users", 200, 45, 1),
    HttpLog("2024-01-15T10:00:01", "POST", "/api/users", 201, 120, 1),
    HttpLog("2024-01-15T10:00:02", "GET", "/api/products", 200, 30, 2),
    HttpLog("2024-01-15T10:00:03", "GET", "/api/users/1", 404, 15, None),
    HttpLog("2024-01-15T10:00:04", "DELETE", "/api/products/5", 500, 200, 3),
    HttpLog("2024-01-15T10:00:05", "GET", "/api/users", 200, 50, 2),
    HttpLog("2024-01-15T10:00:06", "PUT", "/api/users/1", 200, 80, 1),
    HttpLog("2024-01-15T10:00:07", "GET", "/api/products", 200, 35, None),
    HttpLog("2024-01-15T10:00:08", "POST", "/api/orders", 201, 150, 2),
    HttpLog("2024-01-15T10:00:09", "GET", "/api/orders", 503, 5000, 1),
]


# TODO(human): Implement the following functions using comprehensions


def get_failed_requests(logs: Iterable[HttpLog]) -> list[HttpLog]:
    """Return all requests with status code >= 400.

    Use a list comprehension.
    """
    return [log for log in logs if log.status_code >= 400]


def get_average_response_time(logs: Iterable[HttpLog]) -> float:
    """Calculate average response time in milliseconds.

        Use a generator expression with sum() and count.
        Hint: You'll need to convert to list first to get both sum and
    count,
        or iterate twice, or use a different approach.
    """
    return mean(log.response_time_ms for log in logs)


def count_requests_by_method(logs: Iterable[HttpLog]) -> dict[str, int]:
    """Count how many requests per HTTP method.

    Example return: {"GET": 5, "POST": 2, "PUT": 1, "DELETE": 1}

    Hint: This one is tricky with a pure dict comprehension.
    You might need Counter from collections, or a different approach.
    """
    return dict(Counter(log.method for log in logs))


def get_unique_users(logs: Iterable[HttpLog]) -> set[int]:
    """Return set of unique user IDs (excluding None).

    Use a set comprehension.
    """
    return {log.user_id for log in logs if log.user_id is not None}


def group_logs_by_status_category(logs: Iterable[HttpLog]) -> dict[str, list[HttpLog]]:
    """Group logs by status category: "2xx", "4xx", "5xx".

    Example return: {"2xx": [...], "4xx": [...], "5xx": [...]}

    This is harder - a pure comprehension might not be ideal.
    Choose the most readable approach.
    """
    logs_by_status_category: dict[str, list[HttpLog]] = defaultdict(list)

    for log in logs:
        category = f"{log.status_code // 100}xx"
        logs_by_status_category[category].append(log)

    return logs_by_status_category


if __name__ == "__main__":
    print("=== HTTP Log Analysis ===\n")

    failed = get_failed_requests(SAMPLE_LOGS)
    print(f"Failed requests: {len(failed)}")
    for log in failed:
        print(f"  {log.method} {log.path} -> {log.status_code}")

    print(f"\nAverage response time: {get_average_response_time(SAMPLE_LOGS): .1f}ms")

    print(f"\nRequests by method: {count_requests_by_method(SAMPLE_LOGS)}")

    print(f"\nUnique users: {get_unique_users(SAMPLE_LOGS)}")

    print("\nLogs by status category:")
    for category, category_logs in group_logs_by_status_category(SAMPLE_LOGS).items():
        print(f"  {category}: {len(category_logs)} requests")
