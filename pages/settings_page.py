from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._panel = page.locator("#panel_settings")
        self._signature = self._panel.get_by_label("署名", exact=False)

    def fill_signature_attempt(self, text: str) -> None:
        self.fill(self._signature, text)

    def expect_signature_value_length(self, max_len: int) -> None:
        value = self._signature.input_value()
        assert len(value) <= max_len

    def expect_counter(self, expected: str) -> None:
        expect(self._panel.get_by_text(expected, exact=True)).to_be_visible()
