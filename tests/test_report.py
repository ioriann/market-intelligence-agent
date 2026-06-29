from src.report import create_stock_report
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

def test_create_stock_report():
    report = create_stock_report(company_info, stock_data)
    assert "# テスト株式会社 (1234)" in report

if __name__ == "__main__":
    main()