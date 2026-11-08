# automation_final-project

Automation testing practice (Python + Playwright + pytest + Allure) for the support ticket exercise page.

## Project layout

Automation code is at the **repository root**. Read [`automation_rules.md`](automation_rules.md) before changing tests or page objects.

```
constants/locators.py   # ALL locators (one class per screen)
constants/messages.py   # expected UI messages
pages/                  # page objects: actions + assertions, each with @allure.step
tests/                  # test cases: only call page methods
conftest.py             # fixtures + screenshot / video evidence for Allure
run_test.sh             # run tests + build single-file Allure report
```

## Environment

| Item | Value |
| --- | --- |
| **URL** | https://bsv-nhungnguyen.github.io/bai_tap_17082026.html |
| **Admin** (seed data) | set in `.env` → `ADMIN_USER` / `ADMIN_PASSWORD` |
| **Guest** (empty default) | set in `.env` → `GUEST_USER` / `GUEST_PASSWORD` |

Credentials are **not** stored in the repo. Copy the template and fill in the values from the sheet **Rules** (or ask the test lead):

```bash
cp .env.example .env
```

Use the **前提条件** column in the Excel sheet **Testcases_Oanh** to pick the account. Guest-only cases must use the guest account.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env          # then fill in the credentials
brew install allure           # macOS — needed for the HTML report
./run_test.sh
```

## Running tests — `run_test.sh`

| Command | What it does |
| --- | --- |
| `./run_test.sh` | Run all tests → build report → open it in the browser |
| `./run_test.sh --headed` | Same, with a visible browser (any extra arg is passed to pytest) |
| `./run_test.sh -m guest` | Only tests marked `guest` |
| `./run_test.sh -k GD02` | Filter tests by name |
| `./run_test.sh --no-open` | Build the report but do not open it (CI) |
| `./run_test.sh --no-report` | Run tests only |
| `./run_test.sh --report-only` | Rebuild the report from the existing `allure-results/` |

The script exits with pytest's exit code, so it can be used in CI.

## Allure report

**Option 1 — run the commands manually**

```bash
pytest --alluredir=allure-results --clean-alluredir
allure generate allure-results --clean --single-file -o allure-report
open allure-report/index.html        # Linux: xdg-open allure-report/index.html
```

`--single-file` puts the whole report in one `index.html`: it can be opened directly
(no `allure serve` / web server) and sent to others by mail or chat.

**Option 2 — use the bash script:** `./run_test.sh` (see above).

### Evidence in the report

- **Screenshot**: attached to every test (`screenshot_end_of_test`, or `screenshot_on_failure`).
- **Video**: recorded for every test, attached only when the test fails (`video_on_failure`).

### Report language

- `@description_md` and `@allure.title`: Japanese (same as the test sheet).
- Steps: English, written with `@allure.step` in `pages/*.py`.

`allure-results/`, `allure-report/`, `test-results/` and `.DS_Store` are git-ignored — do not push them.

## Coding rules (summary)

### Locators

- All locators live in [`constants/locators.py`](constants/locators.py) as `By` specs, one class per screen. Page objects get them with `self.find(...)`.
- Priority: `role` → `placeholder` → `text` → `label` → CSS (`#id`, BEM class) → XPath (last resort, comment why).
- No `data-testid` on the exercise site.

### Naming & Allure

- Methods: `test_<subject>_<condition>_<expected>`
- Title: `@allure.title("<khu_vực>_<NNN>: <mô tả>")` with 3-digit `NNN`
- Class: `Test` + Japanese area name (e.g. `Testチケット一覧`)
- Steps: `@allure.step("...")` on page-object methods — **no** `with allure.step` in tests
- Use `@description_md` from `helpers` on **class and method** (not raw `@allure.description`)
- Do **not** use `@allure.severity`
- Tests must be independent; known product defects → `pytest.mark.xfail(strict=True, reason=...)`

### POM & traps

- Scope duplicate buttons (詳細/削除/前へ/次へ) to rows/containers
- Checkbox: interact with `<input>`, not `.cb-box`
- Hidden file inputs: `set_input_files`
- Stats tab: click **再集計する** before asserting numbers
- Notifications: `ensure_notification_exists` get-or-create pattern
- Do **not** change the public API of `pages/account_page.py` (extend it, e.g. `AccountKeyboardPage`)

## Testcases covered (sheet Testcases_Oanh)

| ID | Module | Status |
| --- | --- | --- |
| GD01_001 | Browser back/forward | Automated (tabs add no history; Back→Forward reloads → login required) |
| Others_01 | Responsive layout | Automated smoke (375px) |
| GD02.1-01 | Notification empty → create | Automated |
| GD03.3-01 | Print preview window | Automated |
| GD02.4-01 | Per-page 25 | Automated |
| GD02.3-001 | Signature 100 chars | Automated |
| GD03.1-01 | Delete ticket + toast | Automated |
| GD02.8-01 | Ticket search empty | Automated |
| GD02.1-07 | Close user menu | Automated |
| GD03.3-02 | Cross-tab logout | Automated (logout is per tab; reload requires re-login) |
| GD02.5-001 | Created-date tooltip (guest) | Automated |
| GD02.6-01 | Keyboard-only | Automated (login + search); nav tabs → **xfail: known defect** |
| GD02.7-04 | Upload .exe error | Automated |
| — | Login smoke | `tests/test_testcase.py` |

### Known defects found by automation

| ID | Defect |
| --- | --- |
| GD02.6-01 | Nav tabs (チケット一覧/通知/統計/設定) are `<li>` without `tabindex`/`role` → cannot be reached with Tab |
| GD02.6-01 | Pressing Enter in the password field does not submit the login form (must Tab to the button) |
