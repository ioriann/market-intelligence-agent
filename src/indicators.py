def calculate_moving_averages(stock_data, window=25):
    moving_averages = stock_data[["Date", "C"]].copy()
    moving_averages["MA"] = stock_data["C"].rolling(window=window).mean()
    moving_averages = moving_averages.set_index("Date")
    return moving_averages


def add_ma_deviation_rate(moving_averages):
    # 乖離率(%) = (終値 - 移動平均) ÷ 移動平均 × 100
    # MAがNaNの行は乖離率もNaNになる（pandasが自動で伝播させる）
    moving_averages = moving_averages.copy()
    moving_averages["DR"] = (moving_averages["C"] - moving_averages["MA"]) / moving_averages["MA"] * 100
    return moving_averages