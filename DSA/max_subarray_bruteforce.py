import random
import matplotlib.pyplot as plt

# Create a list of 366 random prices
test_prices = []

# Generate random prices
start_price = random.randint(0, 100)
for item in range(366):
    start_price += random.randint(-5, 5)
    test_prices.append(start_price)

days = list(range(len(test_prices)))

# Initialize variables to track the maximum difference and days to buy/sell
max_diff = 0
buy = sell = 0

# Outer loop: Iterates from the first day to the second-last day
for day_one in range(len(test_prices) - 1):
    # Inner loop: Iterates from the next day after day_one to the last day
    for day_two in range(day_one + 1, len(test_prices)):
        # Calculate the price difference between selling on day_two and buying on day_one
        diff = test_prices[day_two] - test_prices[day_one]

        # If the difference is greater than the current maximum difference, update the values
        if diff > max_diff:
            max_diff = diff
            buy = day_one
            sell = day_two

# Output results
print(f"Best day to buy is day {buy}, and best day to sell is day {sell}.")
print(f"Max profit that can be achieved is {max_diff}.")

# Plot the prices and mark the buy and sell days
plt.figure(figsize=(10, 5))
plt.plot(days, test_prices, label='Price', color='blue', marker='o', markersize=3)
plt.axvline(x=buy, color='green', linestyle='--', label='Buy Day')
plt.axvline(x=sell, color='red', linestyle='--', label='Sell Day')

# Add labels and title
plt.xlabel('Day')
plt.ylabel('Price')
plt.title('Price Movement Over Time')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()
