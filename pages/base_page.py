from __future__ import annotations

import random
import string
from typing import Pattern

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def click(self, locator: Locator) -> None:
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.fill(value)

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_hidden(self, locator: Locator) -> None:
        expect(locator).to_be_hidden()

    def expect_text(self, locator: Locator, text: str | Pattern[str]) -> None:
        expect(locator).to_contain_text(text)

    @staticmethod
    def random_alphanumeric(length: int) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(random.choice(alphabet) for _ in range(length))

    @staticmethod
    def random_string(length: int) -> str:
        return "".join(random.choice(string.ascii_letters) for _ in range(length))
