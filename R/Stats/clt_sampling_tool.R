# Population parameters
mu <- 75
sigma <- 17
n <- 90

# Generate a sample
set.seed(10000)
sample <- rnorm(n, mean = mu, sd = sigma)

# Calculate sample statistics
sample_mean <- mean(sample)
sample_sd <- sd(sample)

# Central Limit Theorem
se <- sigma / sqrt(n)

# Calculate probabilities
value <- 80
prob <- 1-pnorm(value, mean = mu, sd = se)
print(prob)
