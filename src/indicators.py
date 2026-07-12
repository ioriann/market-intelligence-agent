def calculate_moving_averages(stock_data, window=25):
    moving_averages = stock_data[["Date", "C"]].copy()
    moving_averages["MA"] = stock_data["C"].rolling(window=window).mean()
    moving_averages = moving_averages.set_index("Date")
    return moving_averages