from src.indicators import calculate_moving_averages
import pandas as pd

# テスト用データ
stock_data = pd.DataFrame({
    "Date": [
        pd.Timestamp("2026-03-25"),
        pd.Timestamp("2026-03-26"),
        pd.Timestamp("2026-03-27"),
        pd.Timestamp("2026-03-28"),
        pd.Timestamp("2026-03-29"),
     ],
    "O": [1000, 1050, 1100, 1150, 1200],
    "H": [1100, 1150, 1200, 1250, 1300],
    "L": [950, 1000, 1050, 1100, 1150],
    "C": [1050, 1100, 900, 1150, 1200],
})

# calculate_moving_averages()の計算が合っているかのテスト
def test_calculate_moving_averages_is_correct_algorithm():
    # 移動平均を計算
    moving_averages = calculate_moving_averages(stock_data, window=3)

    # 計算結果の検証
    expected_moving_averages = pd.DataFrame(
        {
            "C": [1050, 1100, 900, 1150, 1200],
            "MA": [
                float("NaN"),
                float("NaN"),
                (1050 + 1100 + 900) / 3,
                (1100 + 900 + 1150) / 3,
                (900 + 1150 + 1200) / 3,
            ],
        },
        index=pd.Index(stock_data["Date"], name="Date"),
    )

    pd.testing.assert_frame_equal(moving_averages, expected_moving_averages, check_exact=False)