"""GIL demonstration: CPU-bound vs I/O-bound behavior."""

import multiprocessing
import threading
import time


def cpu_bound_task(name: str, iterations: int = 50_000_000) -> None:
    """Simulate CPU-intensive work."""
    print(f"[{name}] Starting CPU work...")
    start = time.perf_counter()

    total = 0
    for i in range(iterations):
        total += i * i

    elapsed = time.perf_counter() - start
    print(f"[{name}] Done in {elapsed:.2f}s")


def run_cpu_sequential() -> float:
    """Run two CPU tasks sequentially."""
    start = time.perf_counter()
    cpu_bound_task("Task-1")
    cpu_bound_task("Task-2")
    return time.perf_counter() - start


def run_cpu_threaded() -> float:
    """Run two CPU tasks in parallel threads."""
    start = time.perf_counter()

    t1 = threading.Thread(target=cpu_bound_task, args=("Thread-1",))
    t2 = threading.Thread(target=cpu_bound_task, args=("Thread-2",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return time.perf_counter() - start


def run_cpu_multiprocess() -> float:
    """Run two CPU tasks in parallel processes."""
    start = time.perf_counter()

    p1 = multiprocessing.Process(target=cpu_bound_task, args=("Process-1",))
    p2 = multiprocessing.Process(target=cpu_bound_task, args=("Process-2",))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    return time.perf_counter() - start


def io_bound_task(name: str, duration: float = 2.0) -> None:
    """Simulate I/O-bound work (network, database, file system)."""
    print(f"[{name}] Starting I/O work...")
    start = time.perf_counter()

    time.sleep(duration)

    elapsed = time.perf_counter() - start
    print(f"[{name}] Done in {elapsed:.2f}s")


def run_io_sequential() -> float:
    """Run two I/O tasks sequentially."""
    start = time.perf_counter()
    io_bound_task("Task-1")
    io_bound_task("Task-2")
    return time.perf_counter() - start


def run_io_threaded() -> float:
    """Run two I/O tasks in parallel threads."""
    start = time.perf_counter()

    t1 = threading.Thread(target=io_bound_task, args=("Thread-1",))
    t2 = threading.Thread(target=io_bound_task, args=("Thread-2",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return time.perf_counter() - start


if __name__ == "__main__":
    print("=" * 50)
    print("CPU-BOUND: SEQUENTIAL")
    print("=" * 50)
    seq_time = run_cpu_sequential()
    print(f"Total sequential time: {seq_time:.2f}s\n")

    print("=" * 50)
    print("CPU-BOUND: THREADED")
    print("=" * 50)
    thread_time = run_cpu_threaded()
    print(f"Total threaded time: {thread_time:.2f}s\n")

    print("=" * 50)
    print("CPU-BOUND: MULTIPROCESS")
    print("=" * 50)
    multiprocess_time = run_cpu_multiprocess()
    print(f"Total multiprocess time: {multiprocess_time:.2f}s\n")

    print("=" * 50)
    print("I/O-BOUND: SEQUENTIAL")
    print("=" * 50)
    io_seq_time = run_io_sequential()
    print(f"Total I/O sequential time: {io_seq_time:.2f}s\n")

    print("=" * 50)
    print("I/O-BOUND: THREADED")
    print("=" * 50)
    io_thread_time = run_io_threaded()
    print(f"Total I/O threaded time: {io_thread_time:.2f}s\n")

    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"CPU-bound: "
          f"sequential={seq_time:.2f}s, "
          f"threaded={thread_time:.2f}s, "
          f"multiprocess={multiprocess_time:.2f}s")
    print(f"I/O-bound: "
          f"sequential={io_seq_time:.2f}s, "
          f"threaded={io_thread_time:.2f}s")
