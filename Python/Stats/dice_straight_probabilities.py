#Finds the probability of getting a straight run of an exact length with a given number of dice
#Example - Find the probability of rolling a small straight (run of 4) with five, six-sided dice
#Total rolls: 7776
#Total valid combinations: 960
#Probability: 0.12345679012345678327

from itertools import permutations, product

#Generates all possible outcomes for a given number of dice with specified sides
def generate_rolls(num_dice, num_sides=6):
    return [roll for roll in product(range(1, num_sides + 1), repeat=num_dice)]

#Generates all unique permutations for consecutive number sets of specified length
def generate_consecutive_sets(run_length, num_sides=6):
    sets = [list(range(i, i + run_length)) for i in range(1, num_sides - run_length + 2)]
    permutations_list = [set(permutations(s)) for s in sets]
    return [item for sublist in permutations_list for item in sublist]

#Checks if a roll contains exactly the required run length of consecutive numbers
def contains_run(roll, runs, min_run, max_run=None):
    if max_run and any(all(item in roll for item in max_set) for max_set in generate_consecutive_sets(max_run)):
        return False  # Contains longer consecutive run, exclude
    return any(all(item in roll for item in run) for run in runs)

#Calculates the probability of rolling exactly the specified run length of consecutive numbers
def calculate_probability(num_dice, run_length, num_sides=6):
    rolls = generate_rolls(num_dice, num_sides)
    runs = generate_consecutive_sets(run_length, num_sides)
    max_run = run_length + 1 if run_length < num_sides else None
    valid_rolls = [roll for roll in rolls if contains_run(roll, runs, run_length, max_run)]
    total_rolls = len(rolls)
    valid_roll_count = len(valid_rolls)
    probability = valid_roll_count / total_rolls
    return probability, valid_rolls, total_rolls

#Example usage: 5 dice, looking for exactly 4 consecutive numbers
probability, valid_rolls, total_rolls = calculate_probability(5, 4)
print(valid_rolls)
print(f"Total rolls: {total_rolls}")
print(f"Total valid combinations: {len(valid_rolls)}")
print(f"Probability: {probability:.20f}")
