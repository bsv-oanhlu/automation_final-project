from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Page

from config import GUEST_PASSWORD, GUEST_USER
from pages.account_page import AccountPage
from pages.header_page import HeaderPage


@pytest.fixture
def access_to_login_screen(page: Page) -> Page:
    account = AccountPage(page)
    account.open()
    return page


@pytest.fixture
def access_to_home_screen(access_to_login_screen: Page) -> Page:
    account = AccountPage(access_to_login_screen)
    account.login_as_admin()
    account.expect_main_app_visible()
    return access_to_login_screen


@pytest.fixture
def access_to_home_screen_guest(access_to_login_screen: Page) -> Page:
    account = AccountPage(access_to_login_screen)
    account.login(GUEST_USER, GUEST_PASSWORD)
    account.expect_main_app_visible()
    return access_to_login_screen


@pytest.fixture
def header(access_to_home_screen: Page) -> HeaderPage:
    return HeaderPage(access_to_home_screen)


@pytest.fixture
def sample_exe_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.exe"
    path.write_bytes(b"MZ" + b"\x00" * 1022)
    return path

