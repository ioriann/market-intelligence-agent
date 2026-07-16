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

fractional_price_data = pd.DataFrame({
    "Date": [pd.Timestamp("2026-03-27")],
    "O": [971.5],
    "H": [980.25],
    "L": [960.1],
    "C": [975.33],
})

moving_averages = pd.DataFrame({
    "Date": [pd.Timestamp("2026-03-27")],
    "MA": [102.5],
    "C": [105],
}).set_index("Date")

# データ1件だけでもレポートの見出し（会社名・銘柄コード）が正しく作られるかを確認する
def test_create_stock_report():
    report = create_stock_report(company_info, stock_data)
    assert "# テスト株式会社 (1234)" in report


# 複数日のデータを渡したとき、「作成日」に一番古い日付ではなく最新日が使われるかを確認する
def test_create_stock_report_uses_latest_date_as_created_date():
    report = create_stock_report(company_info, multi_day_data)
    assert "作成日: 2026-03-27" in report


# 期間サマリー（最高値・最安値・騰落率）の計算式そのものが正しいかを確認する
def test_create_stock_report_summary_reflects_period_high_low_and_change_rate():
    report = create_stock_report(company_info, multi_day_data)
    # 期間最高値=1200, 期間最安値=950
    assert "期間最高値(過去15日間): 1,200円" in report
    assert "期間最安値(過去15日間): 950円" in report
    # 騰落率 = (900 - 1050) / 1050 * 100 = -14.29%
    assert "騰落率: -14.29%" in report


# 4桁以上の価格がカンマ区切り＋「円」表記でテーブルに出力されるかを確認する
def test_create_stock_report_formats_prices_with_comma_and_yen():
    report = create_stock_report(company_info, multi_day_data)
    assert "| 1,000円 | 1,100円 | 950円 | 1,050円 |" in report


# 株価に小数が含まれる場合、四捨五入で丸めずそのまま表示するかを確認する
# （調整後株価など、株価が整数円になるとは限らないケースがあるため）
def test_create_stock_report_does_not_round_fractional_prices():
    report = create_stock_report(company_info, fractional_price_data)
    assert "| 971.5円 | 980.25円 | 960.1円 | 975.33円 |" in report


# 企業情報が取得できず「(不明)」のときも、例外を起こさずレポートを生成できるかを確認する
def test_create_stock_report_missing_company_info_falls_back():
    incomplete_info = {"code": "9999", "name": "(不明)", "market": "(不明)", "sector": "(不明)"}
    report = create_stock_report(incomplete_info, stock_data)
    assert "# (不明) (9999)" in report
    assert "- 市場: (不明)" in report


# ニュースが渡されたとき、タイトル・リンク・日時がMarkdownリンク形式で欄に出るかを確認する
def test_create_stock_report_includes_news_section_when_news_present():
    news = [
        {"title": "テスト社が新製品を発表", "link": "https://example.com/1", "published": "Mon, 29 Jun 2026 13:00:00 GMT"},
    ]
    report = create_stock_report(company_info, stock_data, news)
    assert "## 関連ニュース" in report
    assert "- [テスト社が新製品を発表](https://example.com/1) （Mon, 29 Jun 2026 13:00:00 GMT）" in report


# ニュースが空/未指定のとき、関連ニュース欄自体が出ないことを確認する
def test_create_stock_report_omits_news_section_when_no_news():
    report = create_stock_report(company_info, stock_data)
    assert "## 関連ニュース" not in report

    report_with_empty_list = create_stock_report(company_info, stock_data, news=[])
    assert "## 関連ニュース" not in report_with_empty_list

def test_create_stock_report_moving_averages_section_includes_ma_values():
    report = create_stock_report(company_info, stock_data, moving_averages=moving_averages, moving_average_window=25)
    assert "## MA25(過去1日間)" in report
    assert "| 日付 | 終値 | 移動平均 |" in report
    assert "| 2026-03-27 | 105.0円 | 102.50円 |" in report

# MAがNaNの行（rolling計算の先頭window-1日分）はテーブルに出力しない
def test_create_stock_report_moving_averages_excludes_nan_rows():
    moving_averages_with_nan = pd.DataFrame({
        "Date": [pd.Timestamp("2026-03-26"), pd.Timestamp("2026-03-27")],
        "MA": [float("nan"), 102.5],
        "C": [104, 105],
    }).set_index("Date")

    report = create_stock_report(company_info, stock_data, moving_averages=moving_averages_with_nan, moving_average_window=25)
    assert "## MA25(過去1日間)" in report
    assert "2026-03-26" not in report
    assert "| 2026-03-27 | 105.0円 | 102.50円 |" in report

# MAセクションの冒頭に「MA最新値・終値との位置関係・乖離率」のサマリーが出ることを確認する
def test_create_stock_report_moving_averages_summary_shows_position_and_deviation():
    ma_with_dr = pd.DataFrame({
        "Date": [pd.Timestamp("2026-03-27")],
        "C": [105.0],
        "MA": [100.0],
        "DR": [5.0],  # (105 - 100) / 100 × 100
    }).set_index("Date")

    report = create_stock_report(company_info, stock_data, moving_averages=ma_with_dr, moving_average_window=25)

    assert "- MA25最新値: 100.00円" in report
    assert "- 終値とMA25の位置関係: 終値がMA25の上" in report
    assert "- 乖離率: +5.00%" in report

# save_stock_report() が reports/ に正しいファイル名・内容でファイルを書き出すかを確認する
# （本番のreports/を汚さないよう、tmp_pathで作った一時ディレクトリに移動してから実行する）
def test_save_stock_report_writes_expected_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "reports").mkdir()

    report = create_stock_report(company_info, stock_data)
    save_stock_report(report, company_info["code"], stock_data)

    saved_file = tmp_path / "reports" / "1234_20260327.md"
    assert saved_file.exists()
    assert saved_file.read_text(encoding="utf-8") == report