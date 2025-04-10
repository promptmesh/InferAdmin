import asyncio
import functools
import concurrent.futures
from typing import Callable, Any, TypeVar, cast, Optional
from inferadmin.common.logging import logger

T = TypeVar('T')

# Thread pools will be initialized in init_thread_pools()
_io_executor = None
_cpu_executor = None


def init_thread_pools(io_pool_size: int = 10, cpu_pool_size: int = 0):
    """
    Initialize the thread pools with configurable sizes.
    
    Args:
        io_pool_size: Number of threads for IO operations
        cpu_pool_size: Number of threads for CPU operations (0 = CPU count - 1)
    """
    global _io_executor, _cpu_executor
    
    # Calculate actual CPU thread count if not specified
    actual_cpu_pool_size = cpu_pool_size
    if actual_cpu_pool_size <= 0:
        actual_cpu_pool_size = max(1, concurrent.futures.cpu_count() - 1)
    
    # Create thread pools
    _io_executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=io_pool_size,
        thread_name_prefix="inferadmin-io-"
    )
    logger.info(f"IO thread pool initialized with {io_pool_size} workers")
    
    _cpu_executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=actual_cpu_pool_size,
        thread_name_prefix="inferadmin-cpu-"
    )
    logger.info(f"CPU thread pool initialized with {actual_cpu_pool_size} workers")


def get_io_executor():
    """Get the IO thread pool executor, initializing it if necessary."""
    global _io_executor
    if _io_executor is None:
        init_thread_pools()
    return _io_executor


def get_cpu_executor():
    """Get the CPU thread pool executor, initializing it if necessary."""
    global _cpu_executor
    if _cpu_executor is None:
        init_thread_pools()
    return _cpu_executor


def to_async(func: Callable[..., T], executor: Optional[concurrent.futures.Executor] = None) -> Callable[..., asyncio.Future[T]]:
    """
    Decorator that converts a synchronous function to an asynchronous one.
    It runs the synchronous function in the specified executor (thread pool)
    to prevent it from blocking the event loop.
    
    Args:
        func: The synchronous function to convert
        executor: Optional custom executor to use. If None, uses the default thread pool.
            For IO-bound operations, get_io_executor() is recommended.
            For CPU-bound operations, get_cpu_executor() is recommended.
    
    Example usage:
    
    @to_async
    def cpu_bound_task(x, y):
        # Some CPU-intensive or blocking I/O operation
        return x + y
        
    async def my_handler():
        result = await cpu_bound_task(40, 2)
        return {"result": result}
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor, 
            functools.partial(func, *args, **kwargs)
        )
    return cast(Callable[..., asyncio.Future[T]], wrapper)


def to_async_io(func: Callable[..., T]) -> Callable[..., asyncio.Future[T]]:
    """
    Decorator specifically for IO-bound operations.
    Uses a thread pool optimized for IO operations.
    
    Example usage:
    
    @to_async_io
    def download_large_file(url):
        # IO-bound operation
        return requests.get(url).content
    """
    return to_async(func, get_io_executor())


def to_async_cpu(func: Callable[..., T]) -> Callable[..., asyncio.Future[T]]:
    """
    Decorator specifically for CPU-bound operations.
    Uses a thread pool optimized for CPU operations.
    
    Example usage:
    
    @to_async_cpu
    def process_large_dataset(data):
        # CPU-intensive computation
        return numpy.process(data)
    """
    return to_async(func, get_cpu_executor())