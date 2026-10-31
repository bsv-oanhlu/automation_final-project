"""Sheet Testcases_Oanh — class/method order matches Excel row order (# column).

1. GD01_001 → 2. Others_01 → 3. GD02.1-01 → 4. GD03.3-01 → 5. GD02.4-01
→ 6. GD02.3-001 → 7. GD03.1-01 → 8. GD02.8-01 → 9. GD02.1-07 → 10. GD03.3-02
→ 11. GD02.5-001 → 12. GD02.6-01 → 13. GD02.7-04 → (smoke login, not on sheet)
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest

from helpers import description_md
from pages.account_page import AccountPage
from pages.header_page import HeaderPage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage
from pages.ticket_detail_page import TicketDetailPage
from pages.ticket_list_page import TicketListPage


# --- 1. GD01_001 ---


@description_md(
    """
### ブラウザ・環境差異
**Case ID:** GD01_001
"""
)
class Testブラウザ環境差異:
    @description_md(
        """
**Case ID:** GD01_001

**大項目:** ブラウザ・環境差異  
**小項目:** ブラウザの戻る・進む操作による状態確認  

**前提条件:** 複数画面を遷移済み  

**テスト手順:**
1. ブラウザの戻るボタンを押下する
2. 必要に応じて進むボタンを押下する
3. 各画面の状態を確認する

**期待する結果:** ブラウザ履歴に従って正しく画面遷移し、ログイン状態や入力状態が仕様どおりに処理される  

**Automation note:** Tab nội bộ không ghi browser history → skip có lý do.
"""
    )
    @allure.title("ブラウザ環境差異_001 [GD01_001]: 戻る操作で画面遷移")
    def test_navigation_browser_back_forward_not_supported_by_spa_tabs(self):
        with allure.step("[GD01_001] Skip — panel tabs do not update browser history on this HTML app"):
            pytest.skip(
                "GD01_001: Chuyển tab チケット/通知/統計/設定 chỉ đổi class CSS, "
                "không ghi browser history nên không assert back/forward theo spec sheet."
            )

        with allure.step("[PASSED] GD01_001: N/A — skipped"):
            pass


# --- 2. Others_01 ---


@description_md(
    """
### UI・表示
**Case ID:** Others_01
"""
)
class TestUI表示:
    @description_md(
        """
**Case ID:** Others_01

**大項目:** UI・表示  
**小項目:** 異なる画面サイズでのレイアウト確認  

**前提条件:** チケット一覧画面を表示中  

**テスト手順:**
1. 異なる解像度・アスペクト比の実端末または実ブラウザで画面を表示する
2. ヘッダー、テーブル、ボタン、ダイアログ等を確認する

**期待する結果:** 重要なUI要素が画面外にはみ出さず、重なりや表示崩れが発生しない  

**Automation note:** Smoke tự động tại viewport 375×812; không thay full manual matrix thiết bị thật.
"""
    )
    @allure.title("UI表示_001 [Others_01]: 狭い画面で主要要素表示")
    def test_responsive_narrow_viewport_keeps_ticket_controls_visible(
        self, access_to_home_screen
    ):
        page = access_to_home_screen
        header = HeaderPage(page)
        tickets = TicketListPage(page)

        with allure.step("[Others_01] Resize viewport to mobile width"):
            page.set_viewport_size({"width": 375, "height": 812})

        with allure.step("Assert header and ticket toolbar remain visible"):
            header.expect_app_header_visible()
            tickets.expect_ticket_toolbar_visible()

        with allure.step("[PASSED] Others_01: Core ticket UI visible at narrow viewport"):
            pass


# --- 3. GD02.1-01 ---


@description_md(
    """
### 通知一覧
**Case ID:** GD02.1-01
"""
)
class Test通知一覧:
    @description_md(
        """
**Case ID:** GD02.1-01

**大項目:** OS・環境依存  
**小項目:** 検索結果0件→作成導線（get-or-create）  

**前提条件:** 通知一覧画面を表示中  

**テスト手順:**
1. 存在しないキーワードで検索する
2. 「検索条件に一致する通知が見つかりません」の下にある「＋通知を作成する」ボタンを押下する

**期待する結果:** 通知作成モーダルが開く（ツールバーの作成ボタンと同じ動作）
"""
    )
    @allure.title("通知一覧_001 [GD02.1-01]: 検索0件から通知作成モーダル")
    def test_notification_empty_search_create_opens_modal(
        self, access_to_home_screen, header
    ):
        notifications = NotificationPage(access_to_home_screen)

        with allure.step("[GD02.1-01] Open notifications tab"):
            header.open_tab_notifications()

        with allure.step("Search non-existent keyword"):
            keyword = "notify-missing-keyword-xyz"
            notifications.search(keyword)
            notifications.expect_empty_search_message(keyword)

        with allure.step("Click empty-state create button"):
            notifications.click_empty_state_create()

        with allure.step("Assert notification create modal is open"):
            notifications.expect_create_modal_open()

        with allure.step("[PASSED] GD02.1-01: Empty search create opens notification modal"):
            pass


# --- 4. GD03.3-01 ---


@description_md(
    """
### 別ウィンドウで開く
**Case ID:** GD03.3-01
"""
)
class Test別ウィンドウで開く:
    @description_md(
        """
**Case ID:** GD03.3-01

**大項目:** OS・環境依存  
**小項目:** 別ウィンドウで開く  

**前提条件:** チケット一覧画面を表示中  

**テスト手順:**
1. 「印刷プレビューを開く（新しいウィンドウ）」ボタンを押下する

**期待する結果:** 新しいポップアップウィンドウが開き、印刷プレビュー内容（対象チケット数）が表示される
"""
    )
    @allure.title("チケット一覧_001 [GD03.3-01]: 印刷プレビュー新規ウィンドウ")
    def test_ticket_print_preview_opens_popup_with_count(self, access_to_home_screen):
        tickets = TicketListPage(access_to_home_screen)

        with allure.step("[GD03.3-01] Open print preview in new window"):
            popup = tickets.open_print_preview_popup()

        with allure.step("Assert preview content"):
            popup.wait_for_load_state()
            assert "印刷プレビュー" in popup.content()
            assert "対象チケット数" in popup.content()

        with allure.step("[PASSED] GD03.3-01: Print preview popup displays ticket count"):
            pass


# --- 5. GD02.4-01 ---


@description_md(
    """
### 表示件数変更
**Case ID:** GD02.4-01
"""
)
class Test表示件数変更:
    @description_md(
        """
**Case ID:** GD02.4-01

**大項目:** OS・環境依存  
**小項目:** 表示件数変更  

**前提条件:** チケット一覧画面を表示中  

**テスト手順:**
1. 「表示件数」プルダウンで25を選択する

**期待する結果:** 12件全てが1ページに表示される
"""
    )
    @allure.title("チケット一覧_002 [GD02.4-01]: 表示件数25で全件1ページ表示")
    def test_ticket_per_page_25_shows_all_twelve_rows(self, access_to_home_screen):
        tickets = TicketListPage(access_to_home_screen)

        with allure.step("[GD02.4-01] Select 25 items per page"):
            tickets.set_per_page("25")

        with allure.step("Assert 12 ticket rows are visible"):
            tickets.expect_ticket_row_count(12)

        with allure.step("[PASSED] GD02.4-01: All admin seed tickets appear on one page"):
            pass


# --- 6. GD02.3-001 ---


@description_md(
    """
### 設定
**Case ID:** GD02.3-001
"""
)
class Test設定:
    @description_md(
        """
**Case ID:** GD02.3-001

**大項目:** OS・環境依存  
**小項目:** 文字数カウンター  

**前提条件:** 設定画面を表示中  

**テスト手順:**
1. 署名欄に100文字を超えるテキストを入力しようとする

**期待する結果:** 最大100文字までしか入力できず、カウンター表示が「100/100文字」で止まる
"""
    )
    @allure.title("設定_001 [GD02.3-001]: 署名100文字カウンター上限")
    def test_settings_signature_counter_stops_at_100(self, access_to_home_screen, header):
        settings = SettingsPage(access_to_home_screen)
        over_limit = "あ" * 120

        with allure.step("[GD02.3-001] Open settings tab"):
            header.open_tab_settings()

        with allure.step("Attempt to type more than 100 characters"):
            settings.fill_signature_attempt(over_limit)

        with allure.step("Assert value length and counter"):
            settings.expect_signature_value_length(100)
            settings.expect_counter("100/100文字")

        with allure.step("[PASSED] GD02.3-001: Signature counter enforces 100 character limit"):
            pass


# --- 7. GD03.1-01 ---


@description_md(
    """
### チケット削除
**Case ID:** GD03.1-01
"""
)
class Testチケット削除:
    @description_md(
        """
**Case ID:** GD03.1-01

**大項目:** OS・環境依存  
**小項目:** チケット削除（確認ダイアログ→OK）  

**前提条件:** チケット一覧画面を表示中  

**テスト手順:**
1. 任意の行の「削除」ボタンを押下する
2. 確認ダイアログ（confirm）で「OK」を押下する

**期待する結果:** 該当行が一覧から削除され、トースト通知「チケットを削除しました。」が表示される
"""
    )
    @allure.title("チケット一覧_003 [GD03.1-01]: チケット削除とトースト通知")
    def test_ticket_delete_confirm_removes_row_and_toast(self, access_to_home_screen):
        tickets = TicketListPage(access_to_home_screen)

        with allure.step("[GD03.1-01] Delete first ticket and accept confirm dialog"):
            ticket_id = tickets.delete_first_ticket_with_confirm()

        with allure.step("Assert row removed and toast shown"):
            tickets.expect_ticket_id_not_in_table(ticket_id)
            tickets.expect_toast_deleted()

        with allure.step("[PASSED] GD03.1-01: Ticket delete flow completes with toast"):
            pass


# --- 8. GD02.8-01 & 9. GD02.1-07 (same 大項目, consecutive rows) ---


@description_md(
    """
### ログイン画面
**Case ID:** GD02.8-01, GD02.1-07 (sheet row order)
"""
)
class Testログイン画面:
    @description_md(
        """
**Case ID:** GD02.8-01

**大項目:** ログイン画面  
**小項目:** 検索結果0件  

**前提条件:** チケット一覧画面を表示中  

**テスト手順:**
1. 検索欄に存在しないキーワードを入力する
2. 「検索」ボタンを押下する

**期待する結果:** 「該当するチケットがありません」というメッセージが表示される
"""
    )
    @allure.title("チケット一覧_004 [GD02.8-01]: 検索結果0件メッセージ表示")
    def test_ticket_search_no_match_shows_empty_message(self, access_to_home_screen):
        tickets = TicketListPage(access_to_home_screen)

        with allure.step("[GD02.8-01] Search with non-existent keyword"):
            tickets.search("zzzz-no-ticket-keyword-99999")

        with allure.step("Assert empty search message"):
            tickets.expect_empty_search_message()

        with allure.step("[PASSED] GD02.8-01: Empty ticket search message is shown"):
            pass

    @description_md(
        """
**Case ID:** GD02.1-07

**大項目:** ログイン画面  
**小項目:** ユーザーメニューを閉じる  

**前提条件:** ユーザーメニューを表示中  

**テスト手順:**
1. メニュー外の任意の場所を押下する

**期待する結果:** ユーザーメニューが閉じる
"""
    )
    @allure.title("ヘッダー_001 [GD02.1-07]: ユーザーメニュー外クリックで閉じる")
    def test_header_click_outside_closes_user_menu(self, access_to_home_screen):
        header = HeaderPage(access_to_home_screen)

        with allure.step("[GD02.1-07] Open user menu"):
            header.open_user_menu()
            header.expect_user_menu_open()

        with allure.step("Click outside menu"):
            header.click_outside_user_menu()

        with allure.step("Assert menu is closed"):
            header.expect_user_menu_closed()

        with allure.step("[PASSED] GD02.1-07: User menu closes on outside click"):
            pass


# --- 10. GD03.3-02 ---


@description_md(
    """
### 認証・セッション
**Case ID:** GD03.3-02
"""
)
class Test認証セッション:
    @description_md(
        """
**Case ID:** GD03.3-02

**大項目:** 認証・セッション  
**小項目:** 別タブ・別ブラウザでのログアウト影響  

**前提条件:** 同一アカウントで複数のブラウザまたはタブからログインしている  

**テスト手順:**
1. ブラウザAでログアウトする
2. ブラウザBでログイン後の画面を操作する

**期待する結果:** 仕様に従ってセッション無効化が反映され、必要に応じて再ログインを要求される  

**Automation note:** App in-memory theo tab → skip cho đến khi có spec rõ.
"""
    )
    @allure.title("認証セッション_001 [GD03.3-02]: 別タブログアウト影響")
    def test_session_cross_tab_logout_not_specified(self):
        with allure.step("[GD03.3-02] Skip — no shared server session contract in bai_tap HTML"):
            pytest.skip(
                "GD03.3-02: Trang bài tập lưu trạng thái in-memory theo từng tab, "
                "sheet không mô tả hành vi đồng bộ logout giữa browser A/B."
            )

        with allure.step("[PASSED] GD03.3-02: N/A — skipped"):
            pass


# --- 11. GD02.5-001 ---


@description_md(
    """
### デフォルトアカウント
**Case ID:** GD02.5-001 (guest / guest123)
"""
)
class Testデフォルトアカウント:
    @pytest.mark.guest
    @description_md(
        """
**Case ID:** GD02.5-001

**大項目:** デフォルトアカウント（guestユーザー）  
**小項目:** ツールチップ表示  

**前提条件:** チケット一覧画面を表示中（tài khoản **guest** / **guest123**）  

**テスト手順:**
1. 「作成日」列見出し横のヘルプアイコン（?）にカーソルを合わせる

**期待する結果:** 「チケットが作成された日付を表示します」という説明テキストが表示される
"""
    )
    @allure.title("デフォルトアカウント_001 [GD02.5-001]: 作成日ツールチップ表示")
    def test_guest_created_date_tooltip_shows_help_text(self, access_to_home_screen_guest):
        tickets = TicketListPage(access_to_home_screen_guest)

        with allure.step("[GD02.5-001] Hover 作成日 help icon"):
            tickets.hover_created_date_help()

        with allure.step("Assert tooltip text"):
            tickets.expect_created_date_tooltip()

        with allure.step("[PASSED] GD02.5-001: Created date tooltip is visible for guest user"):
            pass


# --- 12. GD02.6-01 ---


@description_md(
    """
### アクセシビリティ
**Case ID:** GD02.6-01
"""
)
class Testアクセシビリティ:
    @description_md(
        """
**Case ID:** GD02.6-01

**大項目:** アクセシビリティ  
**小項目:** キーボードのみでの主要操作確認  

**前提条件:** ログイン済み・チケット一覧画面を表示中  

**テスト手順:**
1. マウスを使用せず、Tab・Shift+Tab・Enter・Space等で主要操作を行う
2. フォーカス位置を確認する

**期待する結果:** 主要な操作要素へ適切な順序でフォーカスが移動し、キーボードだけで操作できる  

**Automation note:** Cần ma trận thủ công; sheet không liệt kê thứ tự focus → skip.
"""
    )
    @allure.title("アクセシビリティ_001 [GD02.6-01]: キーボードのみ操作")
    def test_accessibility_full_keyboard_path_not_automated(self):
        with allure.step("[GD02.6-01] Skip — testcase requires comprehensive manual keyboard matrix"):
            pytest.skip(
                "GD02.6-01: Cần ma trận Tab/Enter/Space trên toàn màn hình; "
                "sheet không liệt kê thứ tự focus mong đợi để assert tự động."
            )

        with allure.step("[PASSED] GD02.6-01: N/A — skipped"):
            pass


# --- 13. GD02.7-04 ---


@description_md(
    """
### チケット詳細ダイアログ
**Case ID:** GD02.7-04
"""
)
class Testチケット詳細ダイアログ:
    @description_md(
        """
**Case ID:** GD02.7-04

**大項目:** チケット詳細ダイアログ  
**小項目:** ファイルアップロード（拡張子エラー）  

**前提条件:** 詳細ダイアログを表示中  

**テスト手順:**
1. ドロップゾーンに.exeファイルをアップロードする

**期待する結果:** 「対応していないファイル形式です。」というエラーが表示され、プレビューされない  

**備考 (sheet):** File tạo trong code: sample.exe (~1KB). Kiểm tra vùng preview bị ẩn.
"""
    )
    @allure.title("チケット詳細_001 [GD02.7-04]: exeアップロード形式エラー")
    def test_ticket_detail_upload_exe_shows_type_error(
        self, access_to_home_screen, sample_exe_file: Path
    ):
        tickets = TicketListPage(access_to_home_screen)
        detail = TicketDetailPage(access_to_home_screen)

        with allure.step("[GD02.7-04] Open detail dialog on first ticket"):
            tickets.open_detail_on_first_row()
            detail.expect_open()

        with allure.step("Upload unsupported .exe via hidden file input"):
            detail.upload_file(sample_exe_file)

        with allure.step("Assert error message and no preview"):
            detail.expect_file_type_error()
            detail.expect_preview_hidden()

        with allure.step("[PASSED] GD02.7-04: Exe upload rejected with type error"):
            pass


# --- Smoke login (not listed on Testcases_Oanh sheet) ---


@description_md(
    """
### ログイン
Smoke đăng nhập admin (không có ID trên sheet; chạy cuối danh sách).
"""
)
class Testログイン:
    @description_md(
        """
**Case ID:** *(smoke — không liệt kê trong Testcases_Oanh)*

**Mục đích:** Xác nhận tài khoản admin (`admin` / `admin123`) vào được màn chính.

**Automation:** Mở URL → login → `#main_section` hiển thị.
"""
    )
    @allure.title("ログイン_001 [smoke]: 管理者アカウントでログイン成功")
    def test_login_admin_valid_credentials_shows_home(self, access_to_login_screen):
        account = AccountPage(access_to_login_screen)

        with allure.step("Login with admin account"):
            account.login_as_admin()

        with allure.step("Assert main section is visible"):
            account.expect_main_app_visible()

        with allure.step("[PASSED] Admin login reaches home screen"):
            pass
