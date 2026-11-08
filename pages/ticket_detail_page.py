from __future__ import annotations

from pathlib import Path

import allure
from playwright.sync_api import Page

from constants import messages as msg
from constants.locators import By
from constants.locators import TicketDetailLocators as L
from pages.base_page import BasePage


class TicketDetailPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._dialog = self.find(L.DIALOG)
        self._dialog_title = self.find(L.TITLE)
        self._file_input = self.find(L.FILE_INPUT)
        self._file_preview = self.find(L.FILE_PREVIEW)

    @allure.step("Assert ticket detail dialog is open")
    def expect_open(self) -> None:
        self.expect_visible(self._dialog_title)

    @allure.step("Upload file {file_path}")
    def upload_file(self, file_path: Path) -> None:
        self._file_input.set_input_files(str(file_path))

    @allure.step("Assert unsupported file type error is displayed")
    def expect_file_type_error(self) -> None:
        self.expect_visible(self.find(By.text(msg.FILE_TYPE_ERROR), within=self._dialog))

    @allure.step("Assert file preview is hidden")
    def expect_preview_hidden(self) -> None:
        self.expect_hidden(self._file_preview)
