"""
Script to calculate Combined PML (Probable Maximum Loss) curves for each country.

For each country:
1. Retrieve Earthquake and Flood PML curves (Loss vs. Return Period).
2. Set up the Exceedance Probability (AEP = 1 / RP) curves, including the boundary condition of Loss = 0 at AEP <= 0.5 (RP <= 2).
3. Produce 1,000,000 stochastic catalog samples for Earthquakes and Floods simultaneously (assuming independence).
4. Interpolate losses for each peril in each trial and sum them trial-by-trial to get Combined losses.
5. Compute the Combined PML for each Return Period from the percentiles of the combined losses.
6. Create the "Combined" hazard rows, filling CAP_Stock and GDP from the country values, setting Scaling_Factor to 0, Buildings_Loss to 0, and Total_AAL / Buildings_AAL as the sum of Earthquake and Flood values.
7. Append these "Combined" rows to the original dataset and save to GIRI_Processed_with_Added_PMLs.csv.
"""

import os
import sys
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Set up file paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

processed_dir = os.path.join(project_root, 'data', 'processed', 'GIRI')
input_file_path = os.path.join(processed_dir, 'GIRI_Overall_Loss.csv')
output_file_path = os.path.join(processed_dir, 'GIRI_Overall_Loss_with_Added_PMLs.csv')

df = pd.read_csv(input_file_path)
print(f"Loaded dataset with shape: {df.shape}")

# Define the target Return Periods (stopping at RP 1000 as requested)
return_periods = [10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0]

# List of unique countries
countries = df['iso3cd'].unique()
# countries = ['AGO']
print(f"Found {len(countries)} unique countries in the dataset.")

# Number of stochastic trials
N_trials = 100_000_000
print(f"Generating stochastic catalog with N = {N_trials:,} trials per country...")

combined_rows = []

for country in countries:
    print(country)
    country_df = df[df['iso3cd'] == country]
    
    # 1. Extract Earthquake and Flood data
    df_eq = country_df[country_df['hazard'].str.lower() == 'earthquake'].copy()
    df_fl = country_df[country_df['hazard'].str.lower() == 'flood'].copy()
    
    # Check if we have both hazards, if not, print a message and set empty defaults
    has_eq = len(df_eq) > 0
    has_fl = len(df_fl) > 0
    
    # Set up Earthquake Exceedance Probability Curve (Loss vs. Probability)
    if has_eq:
        eq_rps = df_eq['RP'].values
        eq_losses = df_eq['Loss'].values
        
        # Include boundary condition: Loss = 0 at p <= 0.5 (RP <= 2)
        eq_prob_curve = np.array([1.0 / rp for rp in eq_rps])
        eq_loss_curve = eq_losses.copy()
        
        # Add boundary at RP = 2 (p = 0.5) and RP = 1 (p = 1.0) with loss = 0.0.
        # Since the probability curve must be increasing for np.interp, we will sort both arrays after adding the boundaries.
        eq_prob_curve = np.append(eq_prob_curve, [0.5, 1.0])
        eq_loss_curve = np.append(eq_loss_curve, [0.0, 0.0])
        
        # Sort by probability ascending
        sort_idx = np.argsort(eq_prob_curve)
        eq_prob_curve = eq_prob_curve[sort_idx]
        eq_loss_curve = eq_loss_curve[sort_idx]
    else:
        print(f"No earthquake data found for country {country}")
        # Always returns 0
        eq_prob_curve = np.array([0.0, 1.0])
        eq_loss_curve = np.array([0.0, 0.0])
        
    # Set up Flood Exceedance Probability Curve
    if has_fl:
        fl_rps = df_fl['RP'].values
        fl_losses = df_fl['Loss'].values
        
        fl_prob_curve = np.array([1.0 / rp for rp in fl_rps])
        fl_loss_curve = fl_losses.copy()
        
        # Include boundary condition: Loss = 0 at p <= 0.5 (RP <= 2)
        # Add boundary at RP = 2 (p = 0.5) and RP = 1 (p = 1.0) with loss = 0.0.
        # Since the probability curve must be increasing for np.interp, we will sort both arrays after adding the boundaries.
        fl_prob_curve = np.append(fl_prob_curve, [0.5, 1.0])
        fl_loss_curve = np.append(fl_loss_curve, [0.0, 0.0])
        
        # Sort by probability ascending
        sort_idx = np.argsort(fl_prob_curve)
        fl_prob_curve = fl_prob_curve[sort_idx]
        fl_loss_curve = fl_loss_curve[sort_idx]
    else:
        print(f"No flood data found for country {country}")
        fl_prob_curve = np.array([0.0, 1.0])
        fl_loss_curve = np.array([0.0, 0.0])
        
    # 2. Produce N independent samples for both perils simultaneously.
    # In a Monte Carlo framework, each trial represents a simulated year.
    # We draw independent uniform random variables u_eq and u_fl in [0, 1].
    # These represent the random annual exceedance probabilities (AEP) for Earthquake and Flood respectively.
    # Because u_eq and u_fl are drawn independently, we satisfy the assumption that the two hazards are independent.
    u_eq = np.random.uniform(0.0, 1.0, size=N_trials)
    u_fl = np.random.uniform(0.0, 1.0, size=N_trials)
    
    # 3. Interpolate losses for both hazards.
    # Using np.interp, we map each of the N random probability draws (u_eq and u_fl) to its corresponding loss.
    # - np.interp maps the first argument (drawn probability) using the second argument (the probability points of the curve,which must be sorted in ascending order) and the third argument (the corresponding loss points).
    # - By default, np.interp performs linear interpolation between adjacent coordinates.
    # - If a probability draw is greater than 0.1 (i.e. return period < 10 years), it will interpolate towards the boundary point we added (probability = 0.5, loss = 0.0), returning a decreasing loss down to $0 for return periods <= 2 years.
    # - If a probability draw is smaller than 0.0002 (i.e. return period > 5000 years), np.interp performs flat capping, returning the maximum 5000-year loss value.
    losses_eq = np.interp(u_eq, eq_prob_curve, eq_loss_curve)
    losses_fl = np.interp(u_fl, fl_prob_curve, fl_loss_curve)
    
    # 4. Sum losses trial-by-trial
    losses_combined = losses_eq + losses_fl
    
    # 5. Extract metadata from the existing rows
    # CAP_Stock and GDP are inherited from the country values
    cap_stock = country_df['CAP_Stock'].iloc[0] if len(country_df) > 0 else 0.0
    gdp = country_df['GDP'].iloc[0] if len(country_df) > 0 else 0.0
    sector = country_df['sector'].iloc[0] if len(country_df) > 0 else 'all_assets'
    
    # Total_AAL and Buildings_AAL are the sum of the values for Earthquake and Flood
    total_aal_sum = 0.0
    buildings_aal_sum = 0.0
    
    # Sum Total_AAL and Buildings_AAL for unique country-hazard pairs
    # Note: GIRI_Overall_Loss.csv has multiple rows per country-hazard (one per RP),but the AAL values are duplicate values within the country-hazard group.
    eq_total_aal = df_eq['Total_AAL'].iloc[0] if has_eq else 0.0
    eq_bldg_aal = df_eq['Buildings_AAL'].iloc[0] if has_eq else 0.0
    fl_total_aal = df_fl['Total_AAL'].iloc[0] if has_fl else 0.0
    fl_bldg_aal = df_fl['Buildings_AAL'].iloc[0] if has_fl else 0.0
    
    total_aal_sum = eq_total_aal + fl_total_aal
    buildings_aal_sum = eq_bldg_aal + fl_bldg_aal
    
    # 6. Compute Combined PML for each target Return Period (RP)
    for rp in return_periods:
        # Exceedance probability = 1.0 / RP
        # Percentile to query is 100.0 * (1.0 - 1.0 / RP)
        percentile = 100.0 * (1.0 - 1.0 / rp)
        pml_loss = np.percentile(losses_combined, percentile)
        
        # Build the combined hazard row
        combined_rows.append({
            'iso3cd': country,
            'hazard': 'Combined',
            'sector': sector,
            'Loss': pml_loss,
            'RP': rp,
            'Buildings_Loss': 0.0,
            'Total_AAL': total_aal_sum,
            'Buildings_AAL': buildings_aal_sum,
            'Scaling_Factor': 0.0,
            'CAP_Stock': cap_stock,
            'GDP': gdp
        })

# 7. Convert combined rows to DataFrame
df_combined = pd.DataFrame(combined_rows)

# 8. Concatenate original data with the new Combined hazard rows
df_final = pd.concat([df, df_combined], ignore_index=True)

# Filter final dataset to stop at RP 1000 for all hazards
df_final = df_final[df_final['RP'] <= 1000.0].copy()

# 9. Sort by country, hazard, and Return Period (RP) ascending
df_final = df_final.sort_values(by=['iso3cd', 'hazard', 'RP']).reset_index(drop=True)

# Save the final dataset
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
df_final.to_csv(output_file_path, index=False)

print("\n" + "=" * 80)
print(f"Stochastic PML simulation completed successfully!")
print(f"Final output dataset saved to:\n  {output_file_path}")
print(f"Final dataset shape: {df_final.shape}")
print("=" * 80)

# Print a beautiful preview of the combined PML curve for a couple of countries
preview_countries = ['AGO', 'ETH'] if 'ETH' in countries else [countries[0]]

for pc in preview_countries:
    print(f"\nCombined PML curve preview for {pc}:")
    pc_df = df_final[(df_final['iso3cd'] == pc)]
    print(pc_df[['iso3cd', 'hazard', 'RP', 'Loss']].to_string(index=False, formatters={
        'Loss': lambda x: f"${x:,.2f}",
        'RP': lambda x: f"{int(x)}"
    }))
print("=" * 80)
