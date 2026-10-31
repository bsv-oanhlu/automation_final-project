from __future__ import annotations

from playwright.sync_api import Page, expect

from constants import messages as msg
from pages.base_page import BasePage


class NotificationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # #panel_notifications: scope — duplicate 検索 / 作成 buttons on ticket panel.
        self._panel = page.locator("#panel_notifications")
        self._search_input = self._panel.get_by_placeholder("タイトルまたは内容で検索")
        self._search_button = self._panel.get_by_role("button", name="検索", exact=True)
        self._toolbar_create = self._panel.get_by_role("button", name="通知を作成する")
        self._modal = page.locator("#notification_modal")
        self._modal_title = self._modal.get_by_role("heading", name="通知を作成")
        self._table_body = page.locator("#notification_tbody")

    def search(self, keyword: str) -> None:
        self.fill(self._search_input, keyword)
        self.click(self._search_button)

    def click_empty_state_create(self) -> None:
        self.click(self._panel.get_by_role("button", name="＋通知を作成する"))

    def click_toolbar_create(self) -> None:
        self.click(self._toolbar_create)

    def expect_create_modal_open(self) -> None:
        self.expect_visible(self._modal_title)

    def expect_empty_search_message(self, keyword: str) -> None:
        self.expect_text(self._table_body, msg.NOTIFICATION_SEARCH_EMPTY_PREFIX)
        self.expect_text(self._table_body, keyword)

    def _row_with_title(self, title: str):
        return self._table_body.locator("tr[data-id]").filter(has_text=title)

    def ensure_notification_exists(self, title: str, content: str, notif_type: str = "お知らせ") -> None:
        """Get-or-create: search by title; create via empty-state button if missing."""
        self.search(title)
        if self._row_with_title(title).count() > 0:
            return
        self.click_empty_state_create()
        self.expect_create_modal_open()
        self.fill(self._modal.get_by_label("タイトル", exact=False), title)
        self._modal.get_by_label("種別", exact=False).select_option(notif_type)
        self.fill(self._modal.get_by_label("内容", exact=False), content)
        self.click(self._modal.get_by_role("button", name="作成する"))
