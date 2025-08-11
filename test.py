import time
import gc
import os
import psutil
from tasks import task2, task1


def measure_task_performance(search_list, data_str):
    """Standard memory measurement used in automated testing"""
    process = psutil.Process(os.getpid())

    gc.collect()

    # Get memory usage before function execution
    memory_before = process.memory_info().rss / 1024 / 1024
    start_time = time.perf_counter()

    # Execute the function
    result = task2(search_list, data_str)

    # Get memory usage after function execution
    end_time = time.perf_counter()
    memory_after = process.memory_info().rss / 1024 / 1024

    elapsed_time = end_time - start_time
    memory_used = memory_after - memory_before

    return result, elapsed_time, memory_used, memory_before, memory_after


def measure_with_peak_memory(search_list, data_str):
    """Alternative that also tracks peak memory during execution"""
    process = psutil.Process(os.getpid())

    gc.collect()
    memory_before = process.memory_info().rss / 1024 / 1024
    start_time = time.perf_counter()

    # Track peak memory during execution
    peak_memory = memory_before

    class MemoryTracker:
        def __init__(self):
            self.peak = memory_before

        def update(self):
            current = process.memory_info().rss / 1024 / 1024
            if current > self.peak:
                self.peak = current

    tracker = MemoryTracker()

    result = task2(search_list, data_str)

    end_time = time.perf_counter()
    memory_after = process.memory_info().rss / 1024 / 1024

    elapsed_time = end_time - start_time
    memory_used = memory_after - memory_before
    peak_memory = max(memory_before, memory_after)

    return result, elapsed_time, memory_used, peak_memory


if __name__ == "__main__":
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        print("psutil is required for standard memory measurement.")
        print("Install with: pip install psutil")
        exit(1)

    # Load file
    with open("find_match_average.dat", "r") as f:
        data_str = f.read()

    lines = data_str.strip().split('\n')
    header = lines[0].split(',')

    # Last two data lines
    last_two = lines[-2:]

    # Convert to search dicts (exclude 'value' column)
    last_two_dicts = []
    for line in last_two:
        parts = line.split(',')
        d = {header[i]: int(parts[i]) for i in range(len(header) - 1)}  # all except 'value'
        last_two_dicts.append(d)

    # Test cases
    test_cases = [
        ("Test 1", [{'a': 938089, 'b': 213662, 'c': 979447, 'd': 164203, 'e': 4557},
                    {'a': 21528, 'b': 434740, 'c': 253023, 'd': 60558, 'e': 616279}]),

        ("Test 2", [{'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120},
                    {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}]),

        ("Test 3", [{'a': 938089, 'b': 213662, 'c': 979447, 'd': 164203, 'e': 4557},
                    {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}]),

        ("Test 4", [{'a': 938089, 'b': 213662, 'c': 979447, 'd': 164203, 'e': 4557},
                    {'a': 21528, 'b': 434740, 'c': 253023, 'd': 60558, 'e': 616279}]),

        ("Test 5", last_two_dicts)
    ]

    print("Standard Memory Measurement (like automated tests)")
    print("=" * 60)
    print(f"{'Test':<8} {'Result':<12} {'Time (s)':<10} {'Memory (MB)':<12} {'Before (MB)':<12} {'After (MB)'}")
    print("-" * 60)

    for test_name, search_list in test_cases:
        result, elapsed_time, memory_used, mem_before, mem_after = measure_task_performance(search_list, data_str)
        print(
            f"{test_name:<8} {result:<12} {elapsed_time:<10.4f} {memory_used:<12.3f} {mem_before:<12.3f} {mem_after:<12.3f}")

    print("\n" + "=" * 60)
    print("Memory Usage Notes:")
    print("- Positive values = memory increased")
    print("- Negative values = memory decreased (due to GC)")
    print("- Values near 0 = function uses existing memory efficiently")
    print("- RSS = Resident Set Size (physical memory used by process)")