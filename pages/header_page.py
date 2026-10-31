from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class HeaderPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # #nav_tabs: scope — tab labels are <li>, not buttons (role not applicable).
        self._nav_tabs = page.locator("#nav_tabs")
        self._app_header = page.locator("#app_header")
        self._user_menu_wrap = page.locator("#user_menu_wrap")
        self._user_menu_content = page.locator("#user_menu_content")
        self._logo = self._app_header.get_by_text("🎫 サポートチケット管理", exact=True)

    def open_tab_tickets(self) -> None:
        self.click(self._nav_tabs.get_by_text("チケット一覧", exact=True))

    def open_tab_notifications(self) -> None:
        self.click(self._nav_tabs.get_by_text("通知", exact=True))

    def open_tab_stats(self) -> None:
        self.click(self._nav_tabs.get_by_text("統計", exact=True))

    def open_tab_settings(self) -> None:
        self.click(self._nav_tabs.get_by_text("設定", exact=True))

    def open_user_menu(self) -> None:
        self.click(self._user_menu_wrap.get_by_role("button"))

    def expect_user_menu_open(self) -> None:
        self.expect_visible(self._user_menu_content)

    def expect_user_menu_closed(self) -> None:
        self.expect_hidden(self._user_menu_content)

    def click_outside_user_menu(self) -> None:
        self.click(self._logo)

    def logout(self) -> None:
        self.open_user_menu()
        self.click(self._user_menu_content.get_by_role("button", name="ログアウト"))

    def expect_logged_in_header(self) -> None:
        self.expect_visible(self._user_menu_wrap.get_by_role("button"))

    def expect_app_header_visible(self) -> None:
        self.expect_visible(self._logo)
