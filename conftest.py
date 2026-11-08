from __future__ import annotations

from pathlib import Path

import allure
import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from config import GUEST_PASSWORD, GUEST_USER
from pages.account_page import AccountPage
from pages.header_page import HeaderPage


# ---------------------------------------------------------------------------
# Evidence: screenshot every test, video only when the test fails
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, tmp_path_factory):
    """Record video for every context; only failed tests keep it (see _attach_evidence)."""
    return {
        **browser_context_args,
        "record_video_dir": str(tmp_path_factory.mktemp("videos")),
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Attach evidence to the Allure test result right after the test body (or a failed setup)."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" or (report.when == "setup" and report.failed):
        _attach_evidence(item, failed=report.failed)


def _attach_evidence(item: pytest.Item, failed: bool) -> None:
    """Screenshot for every test; video only when the test failed."""
    page: Page | None = getattr(item, "funcargs", {}).get("page")
    if page is None or page.is_closed():
        return

    name = "screenshot_on_failure" if failed else "screenshot_end_of_test"
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except PlaywrightError:
        pass

    video = page.video
    if video is None:
        return
    page.close()  # the video file is finalized only when the page is closed
    if failed:
        allure.attach.file(
            video.path(),
            name="video_on_failure",
            attachment_type=allure.attachment_type.WEBM,
        )
    else:
        video.delete()


# ---------------------------------------------------------------------------
# Screen fixtures
# ---------------------------------------------------------------------------


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
