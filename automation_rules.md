# Automation rules (đọc trước khi code)

Nguồn: sheet **Rules** + quy ước dự án `automation_final-project`.

## Môi trường

| Mục | Giá trị |
| --- | --- |
| URL | https://bsv-nhungnguyen.github.io/bai_tap_17082026.html |
| Tài khoản 1 (có data) | `admin` / `admin123` |
| Tài khoản 2 (guest, không data) | `guest` / `guest123` |

- Nhóm case **デフォルトアカウント（guestユーザー）** bắt buộc dùng guest.
- Xem cột **前提条件** trong sheet testcase để chọn account.

## Locator strategy (ưu tiên)

1. `get_by_role` + tên hiển thị  
2. `get_by_placeholder` / `get_by_label`  
3. `get_by_text`  
4. CSS `#id` hoặc class BEM (`.btn-detail`, `.row-checkbox`)  
5. **XPath** — chỉ khi hết cách, **ghi chú lý do** trong code  

Trang không có `data-testid`.

## POM structure rules

- **Page Object** = một màn hình hoặc vùng UI (dialog/drawer), không gom logic test vào POM.
- Locator khai báo trong `__init__`; action method tên động từ (`search`, `open_detail_on_first_row`).
- Nút trùng chữ (**詳細**, **削除**, **前へ**, **次へ**): **scope theo row/container** (`row.get_by_role(...)`).
- Checkbox: `check()` / `click()` trực tiếp lên `input`, không click `.cb-box`.
- File upload: `set_input_files` trên input ẩn, không mở dialog OS.
- **`pages/account_page.py`**: login only — **không sửa** API public.

## Locator discovery process

1. Mở trang thật (hoặc `_page.html` đã tải) → xác định vùng UI.  
2. Thử `get_by_role` / `placeholder` / `label` trên Playwright codegen hoặc snapshot.  
3. Nếu trùng locator → thu hẹp bằng `#panel_*`, `tr[data-id]`, `#notification_tbody`.  
4. Ghi locator dùng chung vào `constants/locators.py` nếu ≥2 page dùng lại.  

## Bẫy (sheet Rules)

1. **Bảng / nút**: scope row; checkbox opacity 0.  
2. **File / async**: input file ẩn; cột 作成日 có icon sort — không assert `innerText` thô; tab **統計** cần bấm **再集計する**.  
3. **State**: đổi filter → bỏ chọn checkbox; pagination **ẩn** (không disable) khi ≤1 trang; mỗi login reset data theo account.  
4. **通知 get-or-create**: search → không thấy → **＋通知を作成する** dưới message empty → modal; gom vào helper kiểu `ensure_notification_exists`.

## Quy ước test

| Mục | Quy tắc |
| --- | --- |
| Tên method | `test_<subject>_<condition>_<expected>` |
| `@allure.title` | `<khu_vực>_<NNN>: <mô tả>` (NNN zero-pad 3 chữ số) |
| Test class | `Test` + tên khu vực tiếng Nhật |
| Kết thúc test | `with allure.step("[PASSED] ..."): pass` |
| Mô tả Allure | `@description_md` (từ `helpers`) ở **class và method** — không dùng `@allure.description` trực tiếp |
| Severity | **Không** dùng `@allure.severity` |
| Độc lập | Không phụ thuộc thứ tự chạy hay state test khác |
| Spec chưa rõ | `pytest.skip(...)` + lý do cụ thể, không đoán hành vi |

## Cấu trúc thư mục

```
automation_final-project/
├── automation_rules.md
├── conftest.py
├── helpers.py
├── config.py
├── constants/
│   ├── locators.py
│   └── messages.py
├── pages/
│   ├── base_page.py
│   ├── account_page.py      # KHÔNG sửa
│   ├── header_page.py
│   ├── ticket_list_page.py
│   ├── notification_page.py
│   ├── settings_page.py
│   └── ticket_detail_page.py
├── tests/
│   └── test_testcase.py      # Toàn bộ testcase sheet Testcases_Oanh
├── .env.example
├── requirements.txt
└── pytest.ini
```

## Chạy test

```bash
cd automation_final-project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env   # tùy chọn
pytest
pytest --alluredir=allure-results
```
