from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from constants import messages as msg
from pages.base_page import BasePage


class TicketListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._panel = page.locator("#panel_tickets")
        self._search_input = self._panel.get_by_placeholder("件名または担当者で検索")
        self._search_button = self._panel.get_by_role("button", name="検索", exact=True)
        self._per_page = self._panel.get_by_label("表示件数")
        self._table_body = page.locator("#ticket_tbody")
        self._ticket_rows = self._table_body.locator("tr[data-id]")
        self._print_preview_btn = self._panel.get_by_role(
            "button", name="印刷プレビューを開く（新しいウィンドウ）"
        )
        # BEM .tooltip-wrap under #th_created — avoid asserting 作成日 header innerText (sort icon).
        self._created_header_help = page.locator("#th_created").locator(".tooltip-wrap")

    def search(self, keyword: str) -> None:
        self.fill(self._search_input, keyword)
        self.click(self._search_button)

    def expect_empty_search_message(self) -> None:
        self.expect_text(self._table_body, msg.TICKET_SEARCH_EMPTY)

    def set_per_page(self, value: str) -> None:
        self._per_page.select_option(value)

    def count_visible_ticket_rows(self) -> int:
        return self._ticket_rows.count()

    def expect_ticket_row_count(self, expected: int) -> None:
        expect(self._ticket_rows).to_have_count(expected)

    def row_by_index(self, index: int = 0) -> Locator:
        return self._ticket_rows.nth(index)

    def delete_button_in_row(self, row: Locator) -> Locator:
        return row.get_by_role("button", name="削除")

    def detail_button_in_row(self, row: Locator) -> Locator:
        return row.get_by_role("button", name="詳細")

    def delete_first_ticket_with_confirm(self) -> str:
        row = self.row_by_index(0)
        ticket_id = row.get_attribute("data-id") or ""
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.delete_button_in_row(row))
        return ticket_id

    def expect_toast_deleted(self) -> None:
        container = self.page.locator("#toast_container")
        self.expect_visible(container.get_by_text(msg.TICKET_DELETE_TOAST))

    def expect_ticket_id_not_in_table(self, ticket_id: str) -> None:
        expect(self._table_body.locator(f'tr[data-id="{ticket_id}"]')).to_have_count(0)

    def open_detail_on_first_row(self) -> None:
        row = self.row_by_index(0)
        self.click(self.detail_button_in_row(row))

    def open_print_preview_popup(self):
        with self.page.expect_popup() as popup_info:
            self.click(self._print_preview_btn)
        return popup_info.value

    def hover_created_date_help(self) -> None:
        self._created_header_help.hover()

    def expect_created_date_tooltip(self) -> None:
        tooltip = self._created_header_help.locator(".tooltip-content")
        self.expect_visible(tooltip)
        self.expect_text(tooltip, msg.CREATED_DATE_TOOLTIP)

    def expect_ticket_toolbar_visible(self) -> None:
        self.expect_visible(self._panel.get_by_role("button", name="新規チケット作成"))
        self.expect_visible(self._search_input)
