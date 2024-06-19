import random
import matplotlib.pyplot as plt

def max_sub_array(prices):
    # Initialize variables
    min_so_far = float('inf')
    min_idx = 0
    max_profit = 0
    buy_day = sell_day = 0

    # Traverse the prices to identify buy and sell days
    for current_day, price in enumerate(prices):
        if price < min_so_far:
            min_so_far = price
            min_idx = current_day
        elif price - min_so_far > max_profit:
            max_profit = price - min_so_far
            buy_day = min_idx
            sell_day = current_day

    return buy_day, sell_day, max_profit

# Create a list of 366 random prices
test_prices = []

start_price = random.randint(0, 100)
for _ in range(366):
    start_price += random.randint(-5, 5)
    test_prices.append(start_price)

days = list(range(len(test_prices)))

# Find the optimal buy and sell days using the function
buy_day, sell_day, max_profit = max_sub_array(test_prices)

# Output results
print(f"Best day to buy is day {buy_day}, and best day to sell is day {sell_day}.")
print(f"Max profit that can be achieved is {max_profit}.")

# Plot the prices and mark the buy and sell days
plt.figure(figsize=(10, 5))
plt.plot(days, test_prices, label='Price', color='blue', marker='o', markersize=3)
plt.axvline(x=buy_day, color='green', linestyle='--', label='Buy Day')
plt.axvline(x=sell_day, color='red', linestyle='--', label='Sell Day')

# Add labels and title
plt.xlabel('Day')
plt.ylabel('Price')
plt.title('Price Movement Over Time')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
