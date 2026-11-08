from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page

from constants import messages as msg
from constants.locators import NotificationLocators as L
from pages.base_page import BasePage


class NotificationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._panel = self.find(L.PANEL)
        self._search_input = self.find(L.SEARCH_INPUT, within=self._panel)
        self._search_button = self.find(L.SEARCH_BUTTON, within=self._panel)
        self._toolbar_create = self.find(L.TOOLBAR_CREATE_BUTTON, within=self._panel)
        self._empty_state_create = self.find(L.EMPTY_STATE_CREATE_BUTTON, within=self._panel)
        self._table_body = self.find(L.TABLE_BODY)
        self._modal = self.find(L.MODAL)
        self._modal_title = self.find(L.MODAL_TITLE, within=self._modal)

    @allure.step("Search notifications with keyword '{keyword}'")
    def search(self, keyword: str) -> None:
        self.fill(self._search_input, keyword)
        self.click(self._search_button)

    @allure.step("Click '＋通知を作成する' under the empty search message")
    def click_empty_state_create(self) -> None:
        self.click(self._empty_state_create)

    @allure.step("Click toolbar create button")
    def click_toolbar_create(self) -> None:
        self.click(self._toolbar_create)

    @allure.step("Assert notification create modal is open")
    def expect_create_modal_open(self) -> None:
        self.expect_visible(self._modal_title)

    @allure.step("Assert empty notification search message for '{keyword}'")
    def expect_empty_search_message(self, keyword: str) -> None:
        self.expect_text(self._table_body, msg.NOTIFICATION_SEARCH_EMPTY_PREFIX)
        self.expect_text(self._table_body, keyword)

    def _row_with_title(self, title: str) -> Locator:
        return self.find(L.ROWS, within=self._table_body).filter(has_text=title)

    @allure.step("Ensure notification '{title}' exists (get-or-create)")
    def ensure_notification_exists(self, title: str, content: str, notif_type: str = "お知らせ") -> None:
        """Get-or-create: search by title; create via empty-state button if missing."""
        self.search(title)
        if self._row_with_title(title).count() > 0:
            return
        self.click_empty_state_create()
        self.expect_create_modal_open()
        self.fill(self.find(L.MODAL_TITLE_INPUT, within=self._modal), title)
        self.find(L.MODAL_TYPE_SELECT, within=self._modal).select_option(notif_type)
        self.fill(self.find(L.MODAL_CONTENT_INPUT, within=self._modal), content)
        self.click(self.find(L.MODAL_SUBMIT_BUTTON, within=self._modal))
