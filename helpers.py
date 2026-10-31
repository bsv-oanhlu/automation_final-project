"""Shared helpers for Allure reporting."""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

import allure

F = TypeVar("F", bound=Callable[..., Any])


def description_md(markdown: str) -> Callable[[F], F]:
    """Apply an Allure description from markdown text (class or test method)."""

    def decorator(target: F) -> F:
        return allure.description(markdown)(target)  # type: ignore[return-value]

    return decorator
