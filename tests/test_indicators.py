from src.indicators import calculate_moving_averages, add_ma_deviation_rate
import pandas as pd
import pytest

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


# 乖離率 = (終値 - MA) / MA × 100 が手計算どおりになるかのテスト
def test_add_ma_deviation_rate_is_correct_formula():
    ma_df = pd.DataFrame({
        "C": [105.0, 95.0],
        "MA": [100.0, 100.0],
    })

    result = add_ma_deviation_rate(ma_df)

    assert result["DR"].tolist() == pytest.approx([5.0, -5.0])
    # 引数で渡した元のDataFrameには列を足さない（副作用なし）ことも確認する
    assert "DR" not in ma_df.columns