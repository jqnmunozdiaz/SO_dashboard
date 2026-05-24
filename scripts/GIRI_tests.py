"""
Script to analyze GIRI Processed dataset and generate a figure with pie plots.
Produces a grid of subfigures (one per country) showing the overall AAL (Average Annual Loss) 
by hazard, summed across all sectors/subsectors.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Add project root to sys.path to load centralized utilities
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)
from src.utils.country_utils import load_subsaharan_countries_dict

# File paths
data_file = os.path.join(project_root, 'data', 'processed', 'GIRI', 'GIRI_Processed.csv')
output_dir = os.path.join(project_root, 'outputs')
output_image = os.path.join(output_dir, 'GIRI_AAL_by_Country.png')

# Ensure outputs directory exists
os.makedirs(output_dir, exist_ok=True)

# Load dataset
print(f"Reading processed data from: {data_file}")
df = pd.read_csv(data_file)

# Filter for Average Annual Loss (AAL)
df_aal = df[df['risk_metric_abbr'] == 'AAL'].copy()

# Aggregate Loss per country and hazard
print("Aggregating AAL per country and hazard...")
agg_df = df_aal.groupby(['iso3cd', 'hazard'])['Loss'].sum().reset_index()

# Get unique countries and sort them
countries = sorted(agg_df['iso3cd'].unique())
num_countries = len(countries)
print(f"Found {num_countries} countries in the dataset.")

# Get country names dictionary for better titles
country_names = load_subsaharan_countries_dict()

# Get unique hazards and assign a premium color palette
hazards = sorted(agg_df['hazard'].unique())
print(f"Hazards identified: {hazards}")

# Set premium, professional colors for the hazards
# Warm earth tones, blues, and teals for modern DRM aesthetic
color_map = {
    'Flood': '#1f77b4',             # Mid blue
    'Tropical cyclone': '#ff7f0e',   # Warm orange
    'Landslide': '#8c564b',          # Earthy brown
    'Tsunami': '#17becf',            # Bright teal/cyan
    'Earthquake': '#d62728',         # Soft red
    'Volcano': '#9467bd',            # Purple
    'Storm surge': '#2ca02c'         # Soft green
}

# Fallback to default tab10 colors if any hazard is not mapped
colors = [color_map.get(h, plt.cm.tab10(i)) for i, h in enumerate(hazards)]
hazard_colors = dict(zip(hazards, colors))

# Determine grid layout (aiming for ~6 columns)
cols = 6
rows = int(np.ceil(num_countries / cols))

# Create the figure with high resolution
fig, axes = plt.subplots(rows, cols, figsize=(20, 3.2 * rows), dpi=150)
axes = axes.flatten()  # Flatten the 2D array of axes for easy indexing

# Style configuration
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

for i, country_code in enumerate(countries):
    ax = axes[i]
    
    # Get data for this country
    country_data = agg_df[agg_df['iso3cd'] == country_code]
    
    # Aggregate loss by hazard for this country
    hazard_losses = country_data.groupby('hazard')['Loss'].sum()
    
    # Filter out hazards with 0 or negative loss to avoid rendering issues
    hazard_losses = hazard_losses[hazard_losses > 0]
    
    country_name = country_names.get(country_code, country_code)
    
    if hazard_losses.empty or hazard_losses.sum() == 0:
        # Draw a blank placeholder circle for countries with 0 loss
        ax.pie([1], colors=['#e0e0e0'], labels=['No Risk/AAL'], labeldistance=0, 
               textprops={'fontsize': 8, 'color': '#757575', 'weight': 'bold', 'ha': 'center', 'va': 'center'})
    else:
        # Prepare sizes and labels
        labels = hazard_losses.index.tolist()
        sizes = hazard_losses.values
        slice_colors = [hazard_colors[label] for label in labels]
        
        # Simple autopct function to hide small percentages
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = pct * total / 100.0
                return f'{pct:.0f}%' if pct >= 10 else ''
            return my_autopct
        
        ax.pie(
            sizes, 
            colors=slice_colors,
            autopct=make_autopct(sizes),
            pctdistance=0.65,
            textprops={'fontsize': 8, 'color': 'white', 'weight': 'bold'},
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 0.8}
        )
        
    # Title of subfigure
    ax.set_title(f"{country_name}\n({country_code})", fontsize=10, weight='bold', pad=2)
    ax.axis('equal')
    
# Hide any unused subplots
for j in range(num_countries, len(axes)):
    fig.delaxes(axes[j])
    
# Add a global main title
fig.suptitle('GIRI Overall Average Annual Loss (AAL) by Hazard per Country', 
             fontsize=18, weight='bold', y=0.98, color='#2c3e50')

# Add a unified global legend
legend_handles = [plt.Rectangle((0,0),1,1, color=hazard_colors[h]) for h in hazards]
fig.legend(legend_handles, hazards, loc='lower center', ncol=len(hazards), 
           fontsize=12, frameon=True, facecolor='#f8f9fa', edgecolor='#e2e8f0',
           bbox_to_anchor=(0.5, 0.01))

# Tight layout with space for main title and legend
plt.tight_layout(rect=[0, 0.04, 1, 0.95])

# Save the figure
print(f"Saving overall AAL pie plot figure to: {output_image}")
plt.savefig(output_image, dpi=200, bbox_inches='tight')
plt.close()

print("Figure generated and saved successfully!")
