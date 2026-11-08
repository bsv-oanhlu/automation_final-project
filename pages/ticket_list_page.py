from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page, expect

from constants import messages as msg
from constants.locators import CommonLocators
from constants.locators import TicketListLocators as L
from pages.base_page import BasePage


class TicketListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._panel = self.find(L.PANEL)
        self._new_ticket_button = self.find(L.NEW_TICKET_BUTTON, within=self._panel)
        self._search_input = self.find(L.SEARCH_INPUT, within=self._panel)
        self._search_button = self.find(L.SEARCH_BUTTON, within=self._panel)
        self._per_page = self.find(L.PER_PAGE_SELECT, within=self._panel)
        self._print_preview_btn = self.find(L.PRINT_PREVIEW_BUTTON, within=self._panel)
        self._table_body = self.find(L.TABLE_BODY)
        self._ticket_rows = self.find(L.ROWS, within=self._table_body)
        self._created_header_help = self.find(L.CREATED_HELP_ICON)
        self._toast_container = self.find(CommonLocators.TOAST_CONTAINER)

    # --- search ---

    @allure.step("Search tickets with keyword '{keyword}'")
    def search(self, keyword: str) -> None:
        self.fill(self._search_input, keyword)
        self.click(self._search_button)

    @allure.step("Search tickets with keyword '{keyword}' using keyboard only (Tab / type / Enter)")
    def search_with_keyboard(self, keyword: str) -> None:
        self.press_tab_until_focused(self._search_input)
        self.page.keyboard.type(keyword)
        self.press_tab_until_focused(self._search_button, max_presses=1)
        self.page.keyboard.press("Enter")

    @allure.step("Assert empty ticket search message is displayed")
    def expect_empty_search_message(self) -> None:
        self.expect_text(self._table_body, msg.TICKET_SEARCH_EMPTY)

    # --- paging ---

    @allure.step("Select {value} items per page")
    def set_per_page(self, value: str) -> None:
        self._per_page.select_option(value)

    def count_visible_ticket_rows(self) -> int:
        return self._ticket_rows.count()

    @allure.step("Assert {expected} ticket rows are displayed")
    def expect_ticket_row_count(self, expected: int) -> None:
        expect(self._ticket_rows).to_have_count(expected)

    # --- rows ---

    def row_by_index(self, index: int = 0) -> Locator:
        return self._ticket_rows.nth(index)

    def delete_button_in_row(self, row: Locator) -> Locator:
        return self.find(L.ROW_DELETE_BUTTON, within=row)

    def detail_button_in_row(self, row: Locator) -> Locator:
        return self.find(L.ROW_DETAIL_BUTTON, within=row)

    @allure.step("Delete first ticket and accept the confirm dialog")
    def delete_first_ticket_with_confirm(self) -> str:
        row = self.row_by_index(0)
        ticket_id = row.get_attribute("data-id") or ""
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.delete_button_in_row(row))
        return ticket_id

    @allure.step("Assert toast 'ticket deleted' is displayed")
    def expect_toast_deleted(self) -> None:
        self.expect_visible(self._toast_container.get_by_text(msg.TICKET_DELETE_TOAST))

    @allure.step("Assert ticket '{ticket_id}' is removed from the table")
    def expect_ticket_id_not_in_table(self, ticket_id: str) -> None:
        expect(self.find(L.row_by_id(ticket_id), within=self._table_body)).to_have_count(0)

    @allure.step("Open detail dialog of the first ticket")
    def open_detail_on_first_row(self) -> None:
        self.click(self.detail_button_in_row(self.row_by_index(0)))

    # --- print preview ---

    @allure.step("Open print preview in a new window")
    def open_print_preview_popup(self) -> Page:
        with self.page.expect_popup() as popup_info:
            self.click(self._print_preview_btn)
        return popup_info.value

    @allure.step("Assert print preview shows title and ticket count")
    def expect_print_preview_content(self, popup: Page) -> None:
        popup.wait_for_load_state()
        content = popup.content()
        assert "印刷プレビュー" in content
        assert "対象チケット数" in content

    # --- tooltip ---

    @allure.step("Hover the help icon of column 作成日")
    def hover_created_date_help(self) -> None:
        self._created_header_help.hover()

    @allure.step("Assert 作成日 tooltip text is displayed")
    def expect_created_date_tooltip(self) -> None:
        tooltip = self.find(L.TOOLTIP_CONTENT, within=self._created_header_help)
        self.expect_visible(tooltip)
        self.expect_text(tooltip, msg.CREATED_DATE_TOOLTIP)

    @allure.step("Assert ticket toolbar (create button, search box) is displayed")
    def expect_ticket_toolbar_visible(self) -> None:
        self.expect_visible(self._new_ticket_button)
        self.expect_visible(self._search_input)
