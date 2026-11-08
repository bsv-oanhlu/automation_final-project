"""Login screen — do not change this module's public API (method names / signatures)."""

from __future__ import annotations

import allure
from playwright.sync_api import Page

from config import ADMIN_PASSWORD, ADMIN_USER, BASE_URL, GUEST_PASSWORD, GUEST_USER
from constants.locators import CommonLocators, LoginLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._heading = self.find(LoginLocators.HEADING)
        self._login_id = self.find(LoginLocators.ID_INPUT)
        self._login_password = self.find(LoginLocators.PASSWORD_INPUT)
        self._login_button = self.find(LoginLocators.SUBMIT_BUTTON)
        self._main = self.find(CommonLocators.MAIN)

    @allure.step("Open login page")
    def open(self) -> None:
        self.page.goto(BASE_URL)
        self.expect_visible(self._heading)

    @allure.step("Login as '{user_id}'")
    def login(self, user_id: str, password: str) -> None:
        self.fill(self._login_id, user_id)
        self.fill(self._login_password, password)
        self.click(self._login_button)

    def login_as_admin(self) -> None:
        self.login(ADMIN_USER, ADMIN_PASSWORD)

    def login_as_guest(self) -> None:
        self.login(GUEST_USER, GUEST_PASSWORD)

    @allure.step("Assert login screen is displayed")
    def expect_login_screen(self) -> None:
        self.expect_visible(self._heading)

    @allure.step("Assert main screen is displayed")
    def expect_main_app_visible(self) -> None:
        self.expect_visible(self._main)
