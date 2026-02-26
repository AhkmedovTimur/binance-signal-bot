def calculate_ma(prices: list[float], window: int) -> float:
    if len(prices) < window:
        raise ValueError(f"Not enough data for window {window}")
    return sum(prices[-window:]) / window

def calculate_ema(prices: list[float], window: int) -> float:
	if len(prices) < window:
		raise ValueError(f"Not enough data for window {window}")
	ema = calculate_ma(prices[:window], window)
	k = 2 / (window + 1)
	for price in prices[window:]:
		ema = price * k + ema * (1 - k)
	return ema

def get_signal(prices: list[float], indicator: str = "ma") -> str:
	if indicator == "ma":
		short = calculate_ma(prices, window=7)
		long = calculate_ma(prices, window=50)
	elif indicator == "ema":
		short = calculate_ema(prices, window=7)
		long = calculate_ema(prices, window=50)
	else:
		raise ValueError("Unsupported indicator")
	
	label = indicator.upper()

	diff_percent = ((short - long) / long) * 100

	threshold = 0.5
 
	if diff_percent > threshold:
		direction = "UP 📈"
	elif diff_percent < -threshold:
		direction = "DOWN 📉"
	else:
		direction = "SIDEWAYS ➖"
  
	return (
		f"{direction}\n"
    f"{label}-short(7): {short:.2f}\n"
    f"{label}-long(50): {long:.2f}\n"
    f"Difference: {diff_percent:.2f}%"
	)