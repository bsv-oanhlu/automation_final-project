# automation_final-project

Automation testing practice (Python + Playwright + pytest + Allure) for the support ticket exercise page.

## Project layout

Automation code is at the **repository root**. Read [`automation_rules.md`](automation_rules.md) before changing tests or page objects.

## Environment (from sheet Rules)

| Item | Value |
| --- | --- |
| **URL** | https://bsv-nhungnguyen.github.io/bai_tap_17082026.html |
| **Admin** (seed data) | `admin` / `admin123` |
| **Guest** (empty default) | `guest` / `guest123` |

Use the **前提条件** column in the Excel sheet **Testcases_Oanh** to pick the account. Guest-only cases must use `guest`.

## Coding rules (summary)

### Locator priority

`get_by_role` → `get_by_placeholder` → `get_by_text` → `get_by_label` → CSS (`#id`, BEM class) → XPath (last resort, comment why).

No `data-testid` on the exercise site.

### Naming & Allure

- Methods: `test_<subject>_<condition>_<expected>`
- Title: `@allure.title("<khu_vực>_<NNN>: <mô tả>")` with 3-digit `NNN`
- Class: `Test` + Japanese area name (e.g. `Testチケット一覧`)
- End each test with `with allure.step("[PASSED] ..."): pass`
- Use `@description_md` from `helpers` on **class and method** (not raw `@allure.description`)
- Do **not** use `@allure.severity`
- Tests must be independent; unclear specs → `pytest.skip("...")` with a concrete reason

### POM & traps

- Scope duplicate buttons (詳細/削除/前へ/次へ) to rows/containers
- Checkbox: interact with `<input>`, not `.cb-box`
- Hidden file inputs: `set_input_files`
- Stats tab: click **再集計する** before asserting numbers
- Notifications: `ensure_notification_exists` get-or-create pattern
- Do **not** modify `pages/account_page.py` public API

## Quick start

```bash
cd automation_final-project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

## Testcases covered (sheet Testcases_Oanh)

| ID | Module | Status |
| --- | --- | --- |
| GD01_001 | Browser back/forward | Skipped (tabs don’t push history) |
| Others_01 | Responsive layout | Automated smoke (375px) |
| GD02.1-01 | Notification empty → create | Automated |
| GD03.3-01 | Print preview window | Automated |
| GD02.4-01 | Per-page 25 | Automated |
| GD02.3-001 | Signature 100 chars | Automated |
| GD03.1-01 | Delete ticket + toast | Automated |
| GD02.8-01 | Ticket search empty | Automated |
| GD02.1-07 | Close user menu | Automated |
| GD03.3-02 | Cross-tab logout | Skipped (no server session spec) |
| GD02.5-001 | Created-date tooltip (guest) | Automated |
| GD02.6-01 | Keyboard-only | Skipped (manual matrix) |
| GD02.7-04 | Upload .exe error | Automated |
| — | Login smoke | `tests/test_testcase.py` |
