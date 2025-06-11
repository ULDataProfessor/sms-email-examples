"""Collects pipeline execution metrics."""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from typing import List


@dataclass
class Result:
    customer_id: str
    success: bool
    latency: float
    error: str | None = None


@dataclass
class Report:
    results: List[Result] = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.results.append(result)

    def summary(self) -> str:
        total = len(self.results)
        succeeded = sum(1 for r in self.results if r.success)
        failed = total - succeeded
        latencies = [r.latency for r in self.results]
        avg_latency = statistics.mean(latencies) if latencies else 0.0
        return (
            f"Total: {total}\n"
            f"Succeeded: {succeeded}\n"
            f"Failed: {failed}\n"
            f"Average latency: {avg_latency:.2f}s"
        )

