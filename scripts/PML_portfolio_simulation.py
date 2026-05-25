"""
PML Portfolio Simulation
Demonstrates the aggregation of PML (Probable Maximum Loss) curves for independent portfolios.
Compares the linear sum of PMLs versus the actual PML of the combined portfolio (illustrating diversification benefit).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set seed for reproducibility
np.random.seed(42)

# Parameters for the lognormal distributions representing annual losses
# Lognormal parameters (mu, sigma) represent the mean and std dev of the natural log of losses
# Portfolio 1 parameters
mu1, sigma1 = 15.0, 1.0
# Portfolio 2 parameters
mu2, sigma2 = 14.5, 1.2

# Number of simulation trials (years)
# High number of trials is required to accurately capture the tail quantiles (e.g. RP = 1000 or 5000)
N = 5_000_000

print(f"Starting simulation with N = {N:,} trials...")

# 1. Simulate independent annual losses
losses_p1 = np.random.lognormal(mean=mu1, sigma=sigma1, size=N)
losses_p2 = np.random.lognormal(mean=mu2, sigma=sigma2, size=N)

# 2. Combine portfolios trial-by-trial (simultaneous sampling)
losses_combined = losses_p1 + losses_p2

# 3. Calculate AAL (Average Annual Loss)
aal_p1 = np.mean(losses_p1)
aal_p2 = np.mean(losses_p2)
aal_sum = aal_p1 + aal_p2
aal_combined = np.mean(losses_combined)

print("\n=== Average Annual Loss (AAL) Comparison ===")
print(f"Portfolio 1 AAL:       ${aal_p1 / 1e6:,.2f} Million")
print(f"Portfolio 2 AAL:       ${aal_p2 / 1e6:,.2f} Million")
print(f"Linear Sum of AALs:    ${aal_sum / 1e6:,.2f} Million")
print(f"Combined Portfolio AAL: ${aal_combined / 1e6:,.2f} Million")
print(f"Difference (Linear Sum vs Combined): ${abs(aal_sum - aal_combined) / 1e6:,.6f} Million (linear addition holds for expected values)")

# 4. Calculate PML for key Return Periods (RP)
# RP values to compute
return_periods = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000]

pmls_p1 = []
pmls_p2 = []
pmls_combined = []

for rp in return_periods:
    # Exceedance probability: p = 1 / RP
    # Percentile: 100 * (1 - p)
    percentile = 100.0 * (1.0 - 1.0 / rp)
    
    pml_1 = np.percentile(losses_p1, percentile)
    pml_2 = np.percentile(losses_p2, percentile)
    pml_comb = np.percentile(losses_combined, percentile)
    
    pmls_p1.append(pml_1)
    pmls_p2.append(pml_2)
    pmls_combined.append(pml_comb)

# 5. Create comparison DataFrame
df_pml = pd.DataFrame({
    'RP (Years)': return_periods,
    'Exceedance Prob (%)': [100.0 / rp for rp in return_periods],
    'PML Portfolio 1 ($M)': [p / 1e6 for p in pmls_p1],
    'PML Portfolio 2 ($M)': [p / 1e6 for p in pmls_p2],
    'Linear Sum ($M)': [(p1 + p2) / 1e6 for p1, p2 in zip(pmls_p1, pmls_p2)],
    'Combined Portfolio ($M)': [p / 1e6 for p in pmls_combined]
})

# Calculate diversification benefit
df_pml['Div. Benefit ($M)'] = df_pml['Linear Sum ($M)'] - df_pml['Combined Portfolio ($M)']
df_pml['Div. Benefit (%)'] = (df_pml['Div. Benefit ($M)'] / df_pml['Linear Sum ($M)']) * 100.0

print("\n=== Probable Maximum Loss (PML) Comparison (in Millions) ===")
print(df_pml.to_string(index=False, formatters={
    'Exceedance Prob (%)': '{:.3f}%'.format,
    'PML Portfolio 1 ($M)': '${:,.2f}M'.format,
    'PML Portfolio 2 ($M)': '${:,.2f}M'.format,
    'Linear Sum ($M)': '${:,.2f}M'.format,
    'Combined Portfolio ($M)': '${:,.2f}M'.format,
    'Div. Benefit ($M)': '${:,.2f}M'.format,
    'Div. Benefit (%)': '{:.2f}%'.format
}))

# 6. Plot the Exceedance curves (Loss vs Return Period)
plt.figure(figsize=(10, 6))

plt.plot(return_periods, [p / 1e6 for p in pmls_p1], marker='o', label='Portfolio 1', color='#1f77b4', linewidth=2)
plt.plot(return_periods, [p / 1e6 for p in pmls_p2], marker='s', label='Portfolio 2', color='#ff7f0e', linewidth=2)
plt.plot(return_periods, [(p1 + p2) / 1e6 for p1, p2 in zip(pmls_p1, pmls_p2)], marker='d', label='Linear Sum (PML1 + PML2)', color='#d62728', linestyle='--', linewidth=2)
plt.plot(return_periods, [p / 1e6 for p in pmls_combined], marker='v', label='Simulated Combined Portfolio (L1 + L2)', color='#2ca02c', linewidth=2.5)

# Style chart
plt.xscale('log')
plt.title('PML Exceedance Curves - Portfolio Aggregation & Diversification Benefit', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Return Period (Years)', fontsize=10)
plt.ylabel('Probable Maximum Loss (Million USD)', fontsize=10)
plt.grid(True, which="both", ls="--", color='#e2e8f0')

# Force nice tick text on log scale
plt.xticks(return_periods, [str(rp) for rp in return_periods])

plt.legend(fontsize=10, loc='upper left')

# Add explanation text box
textstr = '\n'.join((
    r'$\mathbf{Key\ Findings:}$',
    r'$\bullet\ AALs\ add\ up\ perfectly\ linearly\ (Expected\ values)$',
    r'$\bullet\ PMLs\ are\ sub-additive\ (Quantiles)$',
    r'$\bullet\ Combined\ PML\ is\ significantly\ lower\ than\ the\ Linear\ Sum$',
    r'$\bullet\ This\ is\ the\ diversification\ benefit\ for\ independent\ perils$'
))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
plt.gca().text(0.05, 0.45, textstr, transform=plt.gca().transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# Save figure in the artifacts directory
artifacts_dir = 'C:\\Users\\jqnmu\\.gemini\\antigravity-ide\\brain\\304ff205-8479-459d-8895-6da342563fbc'
plot_path = os.path.join(artifacts_dir, 'pml_diversification_simulation.png')
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"\nExceedance curve plot saved successfully to: {plot_path}")
