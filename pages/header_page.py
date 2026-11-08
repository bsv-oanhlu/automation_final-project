from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import HeaderLocators as L
from pages.base_page import BasePage


class HeaderPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._nav_tabs = self.find(L.NAV_TABS)
        self._app_header = self.find(L.APP_HEADER)
        self._user_menu_wrap = self.find(L.USER_MENU_WRAP)
        self._user_menu_button = self.find(L.USER_MENU_BUTTON, within=self._user_menu_wrap)
        self._user_menu_content = self.find(L.USER_MENU_CONTENT)
        self._logout_button = self.find(L.LOGOUT_BUTTON, within=self._user_menu_content)
        self._logo = self.find(L.LOGO, within=self._app_header)

    # --- nav tabs ---

    def nav_tab(self, name: str) -> Locator:
        return self.find(L.nav_tab(name), within=self._nav_tabs)

    @allure.step("Open tab '{name}'")
    def open_tab(self, name: str) -> None:
        self.click(self.nav_tab(name))

    def open_tab_tickets(self) -> None:
        self.open_tab("チケット一覧")

    def open_tab_notifications(self) -> None:
        self.open_tab("通知")

    def open_tab_stats(self) -> None:
        self.open_tab("統計")

    def open_tab_settings(self) -> None:
        self.open_tab("設定")

    @allure.step("Assert tab '{name}' is active")
    def expect_tab_active(self, name: str) -> None:
        expect(self.nav_tab(name)).to_have_class(re.compile(r"nav-tab--active"))

    @allure.step("Press Tab until nav tab '{name}' is focused")
    def focus_nav_tab_with_keyboard(self, name: str, max_presses: int = 40) -> None:
        self.press_tab_until_focused(self.nav_tab(name), max_presses=max_presses)

    @allure.step("Press Enter")
    def press_enter(self) -> None:
        self.page.keyboard.press("Enter")

    # --- user menu ---

    @allure.step("Open user menu")
    def open_user_menu(self) -> None:
        self.click(self._user_menu_button)

    @allure.step("Assert user menu is open")
    def expect_user_menu_open(self) -> None:
        self.expect_visible(self._user_menu_content)

    @allure.step("Assert user menu is closed")
    def expect_user_menu_closed(self) -> None:
        self.expect_hidden(self._user_menu_content)

    @allure.step("Click outside the user menu (logo)")
    def click_outside_user_menu(self) -> None:
        self.click(self._logo)

    @allure.step("Logout from user menu")
    def logout(self) -> None:
        self.click(self._user_menu_button)
        self.click(self._logout_button)

    @allure.step("Assert logged-in header is displayed")
    def expect_logged_in_header(self) -> None:
        self.expect_visible(self._user_menu_button)

    @allure.step("Assert app header is displayed")
    def expect_app_header_visible(self) -> None:
        self.expect_visible(self._logo)
