"""Sheet Testcases_Oanh — class/method order matches Excel row order (# column).

1. GD01_001 → 2. Others_01 → 3. GD02.1-01 → 4. GD03.3-01 → 5. GD02.4-01
→ 6. GD02.3-001 → 7. GD03.1-01 → 8. GD02.8-01 → 9. GD02.1-07 → 10. GD03.3-02
→ 11. GD02.5-001 → 12. GD02.6-01 → 13. GD02.7-04 → (smoke login, not on sheet)

Allure report language policy:
- @description_md / @allure.title : Japanese (same as the test sheet)
- Steps                           : English, declared with @allure.step in pages/*.py
  (tests only call page methods — no `with allure.step` here)
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest

from config import BASE_URL
from helpers import description_md
from pages.account_keyboard_page import AccountKeyboardPage
from pages.account_page import AccountPage
from pages.header_page import HeaderPage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage
from pages.ticket_detail_page import TicketDetailPage
from pages.ticket_list_page import TicketListPage

NO_MATCH_TICKET_KEYWORD = "zzzz-no-ticket-keyword-99999"


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

**自動化メモ:** タブ切替はブラウザ履歴に追加されない（SPA内のCSSクラス切替のみ）。
戻る→進むでページが再読み込みされ、メモリ上のログイン状態は破棄されるためログイン画面が表示されることを確認する。
"""
    )
    @allure.title("ブラウザ環境差異_001 [GD01_001]: 戻る・進む操作で画面遷移")
    def test_navigation_back_forward_reloads_app_to_login_screen(self, access_to_home_screen):
        page = access_to_home_screen
        header = HeaderPage(page)
        account = AccountPage(page)

        history_before = header.history_length()
        header.open_tab_notifications()
        header.open_tab_settings()
        header.expect_tab_active("設定")
        header.expect_history_length(history_before)

        header.go_back()
        header.expect_url_not(BASE_URL)

        header.go_forward()
        account.expect_login_screen()


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

**自動化メモ:** ビューポート 375×812 でのスモーク確認。実機マトリクスの手動確認は別途実施。
"""
    )
    @allure.title("UI表示_001 [Others_01]: 狭い画面で主要要素表示")
    def test_responsive_narrow_viewport_keeps_ticket_controls_visible(
        self, access_to_home_screen
    ):
        header = HeaderPage(access_to_home_screen)
        tickets = TicketListPage(access_to_home_screen)

        header.set_viewport(375, 812)
        header.expect_app_header_visible()
        tickets.expect_ticket_toolbar_visible()


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
        keyword = "notify-missing-keyword-xyz"

        header.open_tab_notifications()
        notifications.search(keyword)
        notifications.expect_empty_search_message(keyword)
        notifications.click_empty_state_create()
        notifications.expect_create_modal_open()


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

        popup = tickets.open_print_preview_popup()
        tickets.expect_print_preview_content(popup)


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

        tickets.set_per_page("25")
        tickets.expect_ticket_row_count(12)


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

        header.open_tab_settings()
        settings.fill_signature_attempt("あ" * 120)
        settings.expect_signature_value_length(100)
        settings.expect_counter("100/100文字")


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

        ticket_id = tickets.delete_first_ticket_with_confirm()
        tickets.expect_ticket_id_not_in_table(ticket_id)
        tickets.expect_toast_deleted()


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

        tickets.search(NO_MATCH_TICKET_KEYWORD)
        tickets.expect_empty_search_message()

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
    def test_header_click_outside_closes_user_menu(self, header):
        header.open_user_menu()
        header.expect_user_menu_open()
        header.click_outside_user_menu()
        header.expect_user_menu_closed()


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

**自動化メモ:** 同一ブラウザコンテキストで2タブ（A/B）を開き、両方でログインする。
本アプリはサーバーセッションを持たずタブごとにメモリ上で状態を保持するため、
Aでのログアウト後もBは操作可能であり、Bを再読み込みすると再ログインが要求されることを確認する。
"""
    )
    @allure.title("認証セッション_001 [GD03.3-02]: 別タブログアウト影響")
    def test_session_logout_in_tab_a_requires_relogin_in_tab_b_after_reload(
        self, access_to_home_screen
    ):
        tab_a = access_to_home_screen
        tab_b = tab_a.context.new_page()
        account_a = AccountPage(tab_a)
        account_b = AccountPage(tab_b)
        tickets_b = TicketListPage(tab_b)

        account_b.open()
        account_b.login_as_admin()
        account_b.expect_main_app_visible()

        HeaderPage(tab_a).logout()
        account_a.expect_login_screen()

        tickets_b.search(NO_MATCH_TICKET_KEYWORD)
        tickets_b.expect_empty_search_message()

        account_b.reload()
        account_b.expect_login_screen()


# --- 11. GD02.5-001 ---


@description_md(
    """
### デフォルトアカウント
**Case ID:** GD02.5-001 (guest)
"""
)
class Testデフォルトアカウント:
    @pytest.mark.guest
    @description_md(
        """
**Case ID:** GD02.5-001

**大項目:** デフォルトアカウント（guestユーザー）
**小項目:** ツールチップ表示

**前提条件:** チケット一覧画面を表示中（guestアカウント: .env の GUEST_USER）

**テスト手順:**
1. 「作成日」列見出し横のヘルプアイコン（?）にカーソルを合わせる

**期待する結果:** 「チケットが作成された日付を表示します」という説明テキストが表示される
"""
    )
    @allure.title("デフォルトアカウント_001 [GD02.5-001]: 作成日ツールチップ表示")
    def test_guest_created_date_tooltip_shows_help_text(self, access_to_home_screen_guest):
        tickets = TicketListPage(access_to_home_screen_guest)

        tickets.hover_created_date_help()
        tickets.expect_created_date_tooltip()


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

**自動化メモ:** マウスを使わず Tab / Enter のみでログイン → チケット検索を実施する。
ナビゲーションタブはキーボードで到達できないため、別テスト（アクセシビリティ_002）で xfail として記録する。
"""
    )
    @allure.title("アクセシビリティ_001 [GD02.6-01]: キーボードのみでログイン・検索")
    def test_accessibility_keyboard_only_login_and_search(self, access_to_login_screen):
        account = AccountKeyboardPage(access_to_login_screen)
        tickets = TicketListPage(access_to_login_screen)

        account.login_as_admin_with_keyboard()
        account.expect_main_app_visible()
        tickets.search_with_keyboard(NO_MATCH_TICKET_KEYWORD)
        tickets.expect_empty_search_message()

    @description_md(
        """
**Case ID:** GD02.6-01

**大項目:** アクセシビリティ
**小項目:** ナビゲーションタブへのキーボードフォーカス

**期待する結果:** Tabキーでナビゲーションタブ（通知）にフォーカスでき、Enterで切り替えられる

**既知の不具合:** タブが `<li>` で tabindex / role が無いため、キーボードで到達できない。
"""
    )
    @allure.title("アクセシビリティ_002 [GD02.6-01]: ナビゲーションタブのキーボード操作")
    @pytest.mark.xfail(
        strict=True,
        reason="Known defect: nav tabs are <li> without tabindex — not reachable by Tab",
    )
    def test_accessibility_nav_tabs_reachable_by_keyboard(self, header):
        header.focus_nav_tab_with_keyboard("通知")
        header.press_enter()
        header.expect_tab_active("通知")


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

**備考:** テストコード内で sample.exe（約1KB）を生成。プレビュー領域が非表示であることを確認する。
"""
    )
    @allure.title("チケット詳細_001 [GD02.7-04]: exeアップロード形式エラー")
    def test_ticket_detail_upload_exe_shows_type_error(
        self, access_to_home_screen, sample_exe_file: Path
    ):
        tickets = TicketListPage(access_to_home_screen)
        detail = TicketDetailPage(access_to_home_screen)

        tickets.open_detail_on_first_row()
        detail.expect_open()
        detail.upload_file(sample_exe_file)
        detail.expect_file_type_error()
        detail.expect_preview_hidden()


# --- Smoke login (not listed on Testcases_Oanh sheet) ---


@description_md(
    """
### ログイン
管理者アカウントでのログインスモーク（シート外のケース）
"""
)
class Testログイン:
    @description_md(
        """
**Case ID:** *(スモーク — Testcases_Oanh シート外)*

**目的:** 管理者アカウント（.env の ADMIN_USER）でメイン画面に遷移できることを確認する。

**手順:** URLを開く → ログイン → メイン画面が表示される
"""
    )
    @allure.title("ログイン_001 [smoke]: 管理者アカウントでログイン成功")
    def test_login_admin_valid_credentials_shows_home(self, access_to_login_screen):
        account = AccountPage(access_to_login_screen)

        account.login_as_admin()
        account.expect_main_app_visible()
