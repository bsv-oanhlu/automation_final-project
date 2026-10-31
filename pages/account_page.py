"""Login screen — do not modify this module's public API."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from config import ADMIN_PASSWORD, ADMIN_USER, BASE_URL
from pages.base_page import BasePage


class AccountPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._heading = page.get_by_role("heading", name="ログイン")
        self._login_id = page.get_by_label("ID")
        self._login_password = page.get_by_label("パスワード")
        self._login_button = page.get_by_role("button", name="ログイン")

    def open(self) -> None:
        self.page.goto(BASE_URL)
        self.expect_visible(self._heading)

    def login(self, user_id: str, password: str) -> None:
        self.fill(self._login_id, user_id)
        self.fill(self._login_password, password)
        self.click(self._login_button)

    def login_as_admin(self) -> None:
        self.login(ADMIN_USER, ADMIN_PASSWORD)

    def login_as_guest(self) -> None:
        from config import GUEST_PASSWORD, GUEST_USER

        self.login(GUEST_USER, GUEST_PASSWORD)

    def expect_login_screen(self) -> None:
        self.expect_visible(self._heading)

    def expect_main_app_visible(self) -> None:
        expect(self.page.get_by_role("main")).to_be_visible()
