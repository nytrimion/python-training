"""Generators demonstration: data processing pipeline."""

from collections.abc import Generator, Iterable
from dataclasses import dataclass


@dataclass
class LogEntry:
    """Parsed log entry."""
    timestamp: str
    level: str
    message: str


# Simulated raw log data (imagine this comes from a 10GB file)
RAW_LOGS = [
    "2024-01-15T10:00:00|INFO|Application started",
    "2024-01-15T10:00:01|DEBUG|Loading configuration",
    "2024-01-15T10:00:02|INFO|Connected to database",
    "2024-01-15T10:00:03|WARNING|High memory usage detected",
    "2024-01-15T10:00:04|ERROR|Failed to process request",
    "2024-01-15T10:00:05|INFO|Request completed",
    "2024-01-15T10:00:06|DEBUG|Cache hit for user 123",
    "2024-01-15T10:00:07|ERROR|Connection timeout",
    "2024-01-15T10:00:08|INFO|Retrying connection",
    "2024-01-15T10:00:09|INFO|Connection restored",
]


def parse_logs(lines: Iterable[str]) -> Generator[LogEntry, None, None]:
    """Parse raw log lines into LogEntry objects.

    Each line format: "timestamp|level|message"
    Yield a LogEntry for each line.
    """
    for line in lines:
        fields = line.split("|")
        yield LogEntry(
            timestamp=fields[0],
            level=fields[1],
            message=fields[2],
        )


def filter_by_level(
        entries: Iterable[LogEntry],
        levels: set[str]
) -> Generator[LogEntry, None, None]:
    """Filter log entries by level.

    Only yield entries whose level is in the levels set.
    """
    for entry in entries:
        if entry.level in levels:
            yield entry


def extract_messages(entries: Iterable[LogEntry]) -> Generator[str, None, None]:
    """Extract just the message from each log entry."""
    for entry in entries:
        yield entry.message


if __name__ == "__main__":
    print("=== Generator Pipeline Demo ===\n")

    # Pipeline: parse -> filter -> extract
    # Nothing executes until we iterate!

    parsed = parse_logs(RAW_LOGS)
    errors_only = filter_by_level(parsed, {"ERROR", "WARNING"})
    messages = extract_messages(errors_only)

    print("Error and warning messages:")
    for msg in messages:
        print(f"  - {msg}")

    print("\n=== Memory efficiency demo ===")
    print("Processing 'infinite' data stream...")


    # This generator could yield forever - but we only take 5
    def infinite_numbers() -> Generator[int, None, None]:
        n = 0
        while True:
            yield n
            n += 1


    # Take only first 5 - no infinite loop!
    from itertools import islice

    first_five = list(islice(infinite_numbers(), 5))
    print(f"First 5 numbers: {first_five}")
