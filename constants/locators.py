"""All locators of the exercise site, one class per screen / UI area.

Page objects (pages/*.py) only contain actions and assertions; when the UI changes,
update this file only.

Locator priority (automation_rules.md):
    role → placeholder → text → label → CSS (#id, BEM class) → XPath (last resort, comment why)

Each locator is a ``By`` spec, resolved in BasePage.find() with Playwright's get_by_* API:

    self.find(LoginLocators.SUBMIT_BUTTON)                       # from page root
    self.find(TicketListLocators.SEARCH_BUTTON, within=panel)    # scoped to a container
"""

from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Locator, Page


@dataclass(frozen=True)
class By:
    strategy: str
    value: str
    name: str | None = None
    exact: bool | None = None

    # --- factories (in priority order) ---

    @classmethod
    def role(cls, role: str, name: str | None = None, exact: bool | None = None) -> "By":
        return cls("role", role, name, exact)

    @classmethod
    def placeholder(cls, text: str, exact: bool | None = None) -> "By":
        return cls("placeholder", text, exact=exact)

    @classmethod
    def text(cls, text: str, exact: bool | None = None) -> "By":
        return cls("text", text, exact=exact)

    @classmethod
    def label(cls, text: str, exact: bool | None = None) -> "By":
        return cls("label", text, exact=exact)

    @classmethod
    def css(cls, selector: str) -> "By":
        return cls("css", selector)

    def resolve(self, root: Page | Locator) -> Locator:
        if self.strategy == "role":
            return root.get_by_role(self.value, name=self.name, exact=self.exact)  # type: ignore[arg-type]
        if self.strategy == "placeholder":
            return root.get_by_placeholder(self.value, exact=self.exact)
        if self.strategy == "text":
            return root.get_by_text(self.value, exact=self.exact)
        if self.strategy == "label":
            return root.get_by_label(self.value, exact=self.exact)
        if self.strategy == "css":
            return root.locator(self.value)
        raise ValueError(f"Unknown locator strategy: {self.strategy}")


class CommonLocators:
    MAIN = By.role("main")
    TOAST_CONTAINER = By.css("#toast_container")


class LoginLocators:
    HEADING = By.role("heading", name="ログイン")
    ID_INPUT = By.label("ID")
    PASSWORD_INPUT = By.label("パスワード")
    SUBMIT_BUTTON = By.role("button", name="ログイン")


class HeaderLocators:
    APP_HEADER = By.css("#app_header")
    # #nav_tabs: tab labels are <li> (no role / tabindex) → scope by id, then text.
    NAV_TABS = By.css("#nav_tabs")
    LOGO = By.text("🎫 サポートチケット管理", exact=True)  # within APP_HEADER
    USER_MENU_WRAP = By.css("#user_menu_wrap")
    USER_MENU_BUTTON = By.role("button")  # within USER_MENU_WRAP
    USER_MENU_CONTENT = By.css("#user_menu_content")
    LOGOUT_BUTTON = By.role("button", name="ログアウト")  # within USER_MENU_CONTENT

    @staticmethod
    def nav_tab(name: str) -> By:
        """チケット一覧 / 通知 / 統計 / 設定 — within NAV_TABS."""
        return By.text(name, exact=True)


class TicketListLocators:
    # #panel_tickets: scope — 検索 / 作成 buttons also exist on the notification panel.
    PANEL = By.css("#panel_tickets")
    NEW_TICKET_BUTTON = By.role("button", name="新規チケット作成")
    SEARCH_INPUT = By.placeholder("件名または担当者で検索")
    SEARCH_BUTTON = By.role("button", name="検索", exact=True)
    PER_PAGE_SELECT = By.label("表示件数")
    PRINT_PREVIEW_BUTTON = By.role("button", name="印刷プレビューを開く（新しいウィンドウ）")
    TABLE_BODY = By.css("#ticket_tbody")
    ROWS = By.css("tr[data-id]")  # within TABLE_BODY
    ROW_DELETE_BUTTON = By.role("button", name="削除")  # within a row
    ROW_DETAIL_BUTTON = By.role("button", name="詳細")  # within a row
    # BEM .tooltip-wrap under #th_created — do not assert 作成日 innerText (has sort icon).
    CREATED_HELP_ICON = By.css("#th_created .tooltip-wrap")
    TOOLTIP_CONTENT = By.css(".tooltip-content")  # within CREATED_HELP_ICON

    @staticmethod
    def row_by_id(ticket_id: str) -> By:
        return By.css(f'tr[data-id="{ticket_id}"]')


class NotificationLocators:
    # #panel_notifications: scope — duplicate 検索 / 作成 buttons on ticket panel.
    PANEL = By.css("#panel_notifications")
    SEARCH_INPUT = By.placeholder("タイトルまたは内容で検索")
    SEARCH_BUTTON = By.role("button", name="検索", exact=True)
    TOOLBAR_CREATE_BUTTON = By.role("button", name="通知を作成する")
    EMPTY_STATE_CREATE_BUTTON = By.role("button", name="＋通知を作成する")
    TABLE_BODY = By.css("#notification_tbody")
    ROWS = By.css("tr[data-id]")  # within TABLE_BODY
    MODAL = By.css("#notification_modal")
    MODAL_TITLE = By.role("heading", name="通知を作成")  # within MODAL
    MODAL_TITLE_INPUT = By.label("タイトル", exact=False)
    MODAL_TYPE_SELECT = By.label("種別", exact=False)
    MODAL_CONTENT_INPUT = By.label("内容", exact=False)
    MODAL_SUBMIT_BUTTON = By.role("button", name="作成する")


class SettingsLocators:
    PANEL = By.css("#panel_settings")
    SIGNATURE_INPUT = By.label("署名", exact=False)


class TicketDetailLocators:
    DIALOG = By.role("dialog", name="チケット詳細")
    TITLE = By.role("heading", name="チケット詳細")
    # Hidden file input — no OS dialog; set_input_files only (role/label not applicable).
    FILE_INPUT = By.css("#detail_file_input")
    FILE_PREVIEW = By.css("#detail_file_preview")
