"""Asynchronous helpers for concurrency control."""

import asyncio
from typing import Awaitable, Iterable, List, TypeVar, Callable

T = TypeVar("T")

async def rate_limited_gather(
    coros: Iterable[Callable[[], Awaitable[T]]],
    limit: int = 5,
    retries: int = 3,
) -> List[T]:
    """Run coroutines with a concurrency limit and basic exponential backoff."""

    semaphore = asyncio.Semaphore(limit)

    async def run_with_sem(coro_factory: Callable[[], Awaitable[T]]) -> T:
        delay = 1.0
        for attempt in range(retries):
            async with semaphore:
                try:
                    return await coro_factory()
                except Exception:
                    if attempt == retries - 1:
                        raise
            await asyncio.sleep(delay)
            delay *= 2
        raise RuntimeError("Unreachable")

    return await asyncio.gather(*(run_with_sem(c) for c in coros))
