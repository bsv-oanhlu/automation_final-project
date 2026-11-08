from __future__ import annotations

import allure
from playwright.sync_api import Page

from constants.locators import By
from constants.locators import SettingsLocators as L
from pages.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._panel = self.find(L.PANEL)
        self._signature = self.find(L.SIGNATURE_INPUT, within=self._panel)

    @allure.step("Type text into 署名 (attempt)")
    def fill_signature_attempt(self, text: str) -> None:
        allure.attach(f"{len(text)} characters", name="input length")
        self.fill(self._signature, text)

    @allure.step("Assert 署名 value length is at most {max_len}")
    def expect_signature_value_length(self, max_len: int) -> None:
        value = self._signature.input_value()
        assert len(value) <= max_len, f"Signature length {len(value)} > {max_len}"

    @allure.step("Assert character counter shows '{expected}'")
    def expect_counter(self, expected: str) -> None:
        self.expect_visible(self.find(By.text(expected, exact=True), within=self._panel))
