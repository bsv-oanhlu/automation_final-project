from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect

from constants import messages as msg
from pages.base_page import BasePage


class TicketDetailPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._dialog = page.get_by_role("dialog", name="チケット詳細")
        self._dialog_title = page.get_by_role("heading", name="チケット詳細")
        # Hidden file input — no OS dialog; set_input_files only (#id after role/label N/A).
        self._file_input = page.locator("#detail_file_input")

    def expect_open(self) -> None:
        self.expect_visible(self._dialog_title)

    def upload_file(self, file_path: Path) -> None:
        self._file_input.set_input_files(str(file_path))

    def expect_file_type_error(self) -> None:
        self.expect_visible(self._dialog.get_by_text(msg.FILE_TYPE_ERROR))

    def expect_preview_hidden(self) -> None:
        expect(self.page.locator("#detail_file_preview")).to_be_hidden()
