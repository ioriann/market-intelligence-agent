from src.report import create_stock_report, save_stock_report
import pandas as pd

# テスト用データ
company_info = {
    "code": "1234",
    "name": "テスト株式会社",
    "market": "東証1部",
    "sector": "情報通信"
}

stock_data = pd.DataFrame({
    "Date": [pd.Timestamp("2026-03-27")],
    "O": [100],
    "H": [110],
    "L": [90],
    "C": [105],
})

multi_day_data = pd.DataFrame({
    "Date": [
        pd.Timestamp("2026-03-25"),
        pd.Timestamp("2026-03-26"),
        pd.Timestamp("2026-03-27"),
    ],
    "O": [1000, 1050, 1100],
    "H": [1100, 1150, 1200],
    "L": [950, 1000, 1050],
    "C": [1050, 1100, 900],
})


def test_create_stock_report():
    report = create_stock_report(company_info, stock_data)
    assert "# テスト株式会社 (1234)" in report


def test_create_stock_report_uses_latest_date_as_created_date():
    report = create_stock_report(company_info, multi_day_data)
    assert "作成日: 2026-03-27" in report


def test_create_stock_report_summary_reflects_period_high_low_and_change_rate():
    report = create_stock_report(company_info, multi_day_data)
    # 期間最高値=1200, 期間最安値=950
    assert "期間最高値: 1,200円" in report
    assert "期間最安値: 950円" in report
    # 騰落率 = (900 - 1050) / 1050 * 100 = -14.29%
    assert "騰落率: -14.29%" in report


def test_create_stock_report_formats_prices_with_comma_and_yen():
    report = create_stock_report(company_info, multi_day_data)
    assert "| 1,000円 | 1,100円 | 950円 | 1,050円 |" in report


def test_create_stock_report_missing_company_info_falls_back():
    incomplete_info = {"code": "9999", "name": "(不明)", "market": "(不明)", "sector": "(不明)"}
    report = create_stock_report(incomplete_info, stock_data)
    assert "# (不明) (9999)" in report
    assert "- 市場: (不明)" in report


def test_save_stock_report_writes_expected_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "reports").mkdir()

    report = create_stock_report(company_info, stock_data)
    save_stock_report(report, company_info["code"], stock_data)

    saved_file = tmp_path / "reports" / "1234_20260327.md"
    assert saved_file.exists()
    assert saved_file.read_text(encoding="utf-8") == report
