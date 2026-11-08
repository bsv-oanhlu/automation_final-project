"""Keyboard-only login flow.

Extends AccountPage instead of changing its public API.
"""

from __future__ import annotations

import allure

from config import ADMIN_PASSWORD, ADMIN_USER
from pages.account_page import AccountPage


class AccountKeyboardPage(AccountPage):
    @allure.step("Login as '{user_id}' using keyboard only (Tab / type / Enter)")
    def login_with_keyboard(self, user_id: str, password: str) -> None:
        self.press_tab_until_focused(self._login_id)
        self.page.keyboard.type(user_id)
        self.press_tab_until_focused(self._login_password, max_presses=1)
        self.page.keyboard.type(password)
        self.press_tab_until_focused(self._login_button, max_presses=1)
        self.page.keyboard.press("Enter")

    def login_as_admin_with_keyboard(self) -> None:
        self.login_with_keyboard(ADMIN_USER, ADMIN_PASSWORD)
