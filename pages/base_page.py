from __future__ import annotations

import random
import string
from typing import Pattern

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import By


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # --- locator resolution (locators live in constants/locators.py) ---

    def find(self, by: By, within: Locator | None = None) -> Locator:
        return by.resolve(within if within is not None else self.page)

    # --- low-level actions / assertions (no allure step: callers own the step) ---

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

    # --- keyboard helpers ---

    def press_tab_until_focused(self, locator: Locator, max_presses: int = 20) -> int:
        """Press Tab until ``locator`` has focus; return number of presses. Fails if unreachable."""
        for presses in range(1, max_presses + 1):
            self.page.keyboard.press("Tab")
            if locator.evaluate("el => el === document.activeElement"):
                return presses
        raise AssertionError(f"Element not reachable with Tab within {max_presses} presses")

    # --- browser navigation ---

    def history_length(self) -> int:
        return self.page.evaluate("window.history.length")

    @allure.step("Assert browser history length is {expected}")
    def expect_history_length(self, expected: int) -> None:
        actual = self.history_length()
        assert actual == expected, f"history.length: expected {expected}, got {actual}"

    @allure.step("Press browser Back")
    def go_back(self) -> None:
        self.page.go_back()

    @allure.step("Press browser Forward")
    def go_forward(self) -> None:
        self.page.go_forward()

    @allure.step("Reload page")
    def reload(self) -> None:
        self.page.reload()

    @allure.step("Assert current URL is not '{url}'")
    def expect_url_not(self, url: str) -> None:
        assert self.page.url != url, f"URL should not be {url}"

    @allure.step("Resize viewport to {width}x{height}")
    def set_viewport(self, width: int, height: int) -> None:
        self.page.set_viewport_size({"width": width, "height": height})

    @staticmethod
    def random_alphanumeric(length: int) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(random.choice(alphabet) for _ in range(length))

    @staticmethod
    def random_string(length: int) -> str:
        return "".join(random.choice(string.ascii_letters) for _ in range(length))
