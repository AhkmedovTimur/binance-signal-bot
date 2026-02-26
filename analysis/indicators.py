def calculate_ma(prices: list[float], window: int) -> float:
    if len(prices) < window:
        raise ValueError(f"Not enough data for window {window}")
    return sum(prices[-window:]) / window

def get_signal(prices: list[float]) -> str:
	ma_short = calculate_ma(prices, window=7)
	ma_long = calculate_ma(prices, window=50)

	diff_percent = ((ma_short - ma_long) / ma_long) * 100

	threshold = 0.5
 
	if diff_percent > threshold:
		direction = "UP 📈"
	elif diff_percent < -threshold:
		direction = "DOWN 📉"
	else:
		direction = "SIDEWAYS ➖"
  
	return (
		f"{direction}\n"
    f"MA-short(7): {ma_short:.2f}\n"
    f"MA-long(50): {ma_long:.2f}\n"
    f"Difference: {diff_percent:.2f}%"
	)
