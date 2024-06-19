import random
import matplotlib.pyplot as plt

# Create a list of 366 random prices
test_prices = []

start_price = random.randint(0,100)

for item in range(0,366):
    start_price += random.randint(-5,5)
    test_prices.append(start_price)

days = list(range(len(test_prices)))

# Find the midpoint
midpoint = len(test_prices) // 2

# Slice into two halves
left_half = test_prices[:midpoint]
right_half = test_prices[midpoint:]

# Find local minima and maxima in each half
left_min_idx = left_half.index(min(left_half))
left_max_idx = left_half.index(max(left_half))

right_min_idx = right_half.index(min(right_half)) + midpoint
right_max_idx = right_half.index(max(right_half)) + midpoint

# Initialize variables for best buy and sell days and maximum difference
buy_day = sell_day = 0
max_diff = 0

# Check profits within the left half only
left_diff = left_half[left_max_idx] - left_half[left_min_idx]
if left_min_idx < left_max_idx and left_diff > max_diff:
    buy_day = left_min_idx
    sell_day = left_max_idx
    max_diff = left_diff

# Check profits within the right half only
right_diff = right_half[right_max_idx - midpoint] - right_half[right_min_idx - midpoint]
if right_min_idx < right_max_idx and right_diff > max_diff:
    buy_day = right_min_idx
    sell_day = right_max_idx
    max_diff = right_diff

# Check profits across both halves
total_diff = right_half[right_max_idx - midpoint] - left_half[left_min_idx]
if left_min_idx < right_max_idx and total_diff > max_diff:
    buy_day = left_min_idx
    sell_day = right_max_idx
    max_diff = total_diff

# Output results
print(f"Best day to buy is day {buy_day}, and best day to sell is day {sell_day}.")
print(f"Max profit that can be achieved is {max_diff}.")

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
