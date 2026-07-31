import asyncio
import time

import pytest

from lead_harvester.ingestion.rate_limiter import DomainRateLimiter


@pytest.mark.asyncio
async def test_wait_enforces_minimum_delay_between_requests_to_same_domain():
    limiter = DomainRateLimiter(delay_seconds=0.1)
    start = time.monotonic()
    await limiter.wait("https://example.com/a")
    await limiter.wait("https://example.com/b")
    elapsed = time.monotonic() - start
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_wait_does_not_delay_across_different_domains():
    limiter = DomainRateLimiter(delay_seconds=1.0)
    start = time.monotonic()
    await asyncio.gather(
        limiter.wait("https://a.example.com/"),
        limiter.wait("https://b.example.com/"),
    )
    elapsed = time.monotonic() - start
    assert elapsed < 0.5


@pytest.mark.asyncio
async def test_domain_matching_is_case_insensitive_and_ignores_path():
    limiter = DomainRateLimiter(delay_seconds=0.1)
    start = time.monotonic()
    await limiter.wait("https://Example.com/a")
    await limiter.wait("https://example.COM/b")
    elapsed = time.monotonic() - start
    assert elapsed >= 0.1


def test_negative_delay_is_clamped_to_zero():
    limiter = DomainRateLimiter(delay_seconds=-5.0)
    assert limiter.delay_seconds == 0.0
