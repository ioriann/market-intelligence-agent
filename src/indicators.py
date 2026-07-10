def calculate_moving_averages(stock_data, window=25):
    moving_averages = stock_data["C"].rolling(window=window).mean()
    return moving_averages