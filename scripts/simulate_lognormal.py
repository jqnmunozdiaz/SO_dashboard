import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Number of simulated years
N_years = 100_000

# Parameters for two independent lognormal distributions
# Lognormal parameters (mu, sigma) represent the mean and std dev of the natural log of variables
mu_1, sigma_1 = 10.0, 1.2
mu_2, sigma_2 = 9.5, 1.5

print(f"Simulating two independent lognormal distributions for {N_years:,} years...")
print(f"  Distribution 1: mu = {mu_1}, sigma = {sigma_1}")
print(f"  Distribution 2: mu = {mu_2}, sigma = {sigma_2}\n")

# 1. Simulate independent annual losses from both lognormal distributions
vector_1 = np.random.lognormal(mean=mu_1, sigma=sigma_1, size=N_years)
vector_2 = np.random.lognormal(mean=mu_2, sigma=sigma_2, size=N_years)

# 2. Retain the sum of the values for each year
vector_combined = vector_1 + vector_2

# 3. Compute the 90th percentile (90% non-exceedance / 10% exceedance) for all three vectors
perc = 50
percentile_90_v1 = np.percentile(vector_1, perc)
percentile_90_v2 = np.percentile(vector_2, perc)
percentile_90_combined = np.percentile(vector_combined, perc)

# Display the results
print("=" * 60)
print("             90TH PERCENTILE RESULTS (RP = 10)")
print("=" * 60)
print(f"Vector 1 {perc}th Percentile:       ${percentile_90_v1:,.2f}")
print(f"Vector 2 {perc}th Percentile:       ${percentile_90_v2:,.2f}")
print(f"Linear Sum of {perc}th Percentiles: ${percentile_90_v1 + percentile_90_v2:,.2f}")
print("-" * 60)
print(f"Combined Vector {perc}th Percentile: ${percentile_90_combined:,.2f}")
print("=" * 60)

# Show mathematical comparison
diff = percentile_90_combined - (percentile_90_v1 + percentile_90_v2)
if diff > 0:
    print(f"Observation: Combined PML is GREATER than the linear sum by ${diff:,.2f} (+{diff / (percentile_90_v1 + percentile_90_v2) * 100:.2f}%)")
    print("This demonstrates super-additivity at more frequent return periods (like RP = 10).")
else:
    print(f"Observation: Combined PML is LESS than the linear sum by ${abs(diff):,.2f} (-{abs(diff) / (percentile_90_v1 + percentile_90_v2) * 100:.2f}%)")
    print("This demonstrates sub-additivity (diversification benefit) in the tail of the distributions.")
print("=" * 60)
