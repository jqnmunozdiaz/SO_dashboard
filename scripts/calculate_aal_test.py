"""
Script to calculate Average Annual Loss (AAL) from discrete return periods and losses.
"""

import pandas as pd
import numpy as np

# Input data from user
data = {
    'Loss': [
        1898654054.8,
        1286319706.7,
        765851926.0,
        515773930.8,
        276514733.8,
        110663364.5,
        55341267.4,
        27272006.4,
        11230214.0
    ],
    'RP': [5000, 2500, 1000, 500, 250, 100, 50, 25, 10]
}

# Load into DataFrame and compute Annual Exceedance Probability (p)
df = pd.DataFrame(data)
df['p'] = 1.0 / df['RP']

# Sort by Loss ascending (which makes p descending) for clear interval integration
df = df.sort_values(by='Loss', ascending=True).reset_index(drop=True)

print("=" * 60)
# Exceedance Probability curve coordinates
print("                   EXCEEDANCE PROBABILITY CURVE COORDINATES")
print("-" * 60)
print(df.to_string(index=False, formatters={
    'Loss': lambda x: f"${x:,.2f}",
    'RP': lambda x: f"{int(x)} yrs",
    'p': lambda x: f"{x:.4f}"
}))
print("=" * 60)
print("\n")

# --- METHOD A: Trapezoidal integration of p(L) over Loss intervals ---
# This computes the area under the EP curve using Loss on the horizontal axis:
# Area = Sum_{i} (p_i + p_{i+1})/2 * (L_{i+1} - L_i)
aal_loss_integration = 0.0
for i in range(len(df) - 1):
    l1, l2 = df.loc[i, 'Loss'], df.loc[i+1, 'Loss']
    p1, p2 = df.loc[i, 'p'], df.loc[i+1, 'p']
    aal_loss_integration += 0.5 * (p1 + p2) * (l2 - l1)


# --- METHOD B: Trapezoidal integration of L(p) over Probability intervals ---
# This computes the area under the EP curve using Exceedance Probability on the horizontal axis:
# Area = Sum_{i} (L_i + L_{i+1})/2 * (p_i - p_{i+1})
aal_prob_integration = 0.0
for i in range(len(df) - 1):
    l1, l2 = df.loc[i, 'Loss'], df.loc[i+1, 'Loss']
    p1, p2 = df.loc[i, 'p'], df.loc[i+1, 'p']
    # p1 > p2 since the data is sorted by Loss ascending
    aal_prob_integration += 0.5 * (l1 + l2) * (p1 - p2)


# --- METHOD C: Catastrophe Modeling Approach (with Boundary Conditions) ---
# Standard catastrophe risk models (like GIRI) assume that frequent events below a certain
# return period (e.g. 1 year return period or p = 1.0) yield zero loss.
# We add a boundary point: Loss = 0 at p = 1.0.
df_boundary = df.copy()
df_boundary = pd.concat([
    pd.DataFrame({'Loss': [0.0], 'RP': [1.0], 'p': [1.0]}),
    df_boundary
]).reset_index(drop=True)

aal_cat_model = 0.0
for i in range(len(df_boundary) - 1):
    l1, l2 = df_boundary.loc[i, 'Loss'], df_boundary.loc[i+1, 'Loss']
    p1, p2 = df_boundary.loc[i, 'p'], df_boundary.loc[i+1, 'p']
    aal_cat_model += 0.5 * (p1 + p2) * (l2 - l1)


# Print final calculations
print("=" * 60)
print("                    AAL CALCULATION RESULTS")
print("-" * 60)
print(f"Method A (Integration over Loss Intervals):    ${aal_loss_integration:,.2f}")
print(f"Method B (Integration over Prob Intervals):    ${aal_prob_integration:,.2f}")
print(f"Method C (With boundary Loss=0 at p=1.0):       ${aal_cat_model:,.2f}")
print("=" * 60)
print("\n")

print("NOTE ON RESULTS:")
print("- Method A and Method B calculate the area of the polygon formed directly by the data points.")
print("- Method C reflects the standard approach in hazard management, where losses are assumed")
print("  to interpolate to $0 at a 1-year return period (AEP = 1.0).")
