#%%
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

# Check if running in Jupyter notebook / IPython to determine whether to show or close the plot
try:
    shell = get_ipython().__class__.__name__
    is_jupyter = (shell == 'ZMQInteractiveShell')
except NameError:
    is_jupyter = False

if is_jupyter:
    plt.show()
else:
    plt.close()

print("Figure generated and saved successfully!")

#%%
# ==============================================================================
# NEW SECTION: Buildings Share of AAL for Earthquake and Flood
# ==============================================================================
print("\n" + "="*80)
print(" STARTING BUILDINGS SHARE OF AAL ANALYSIS ")
print("="*80)

# 1. Calculate total AAL per country and hazard (excluding Combined hazard)
total_aal = df_aal.groupby(['iso3cd', 'hazard'])['Loss'].sum().reset_index(name='Total_AAL')

# 2. Calculate Buildings AAL per country and hazard
buildings_aal = df_aal[df_aal['sector'] == 'Buildings'].groupby(['iso3cd', 'hazard'])['Loss'].sum().reset_index(name='Buildings_AAL')

# Merge to match total and sector loss
share_df = pd.merge(total_aal, buildings_aal, on=['iso3cd', 'hazard'], how='left').fillna(0)

# Calculate share percentage
share_df['Share_Pct'] = np.where(
    share_df['Total_AAL'] > 0,
    (share_df['Buildings_AAL'] / share_df['Total_AAL']) * 100.0,
    0.0
)

# Sort for output
share_df = share_df.sort_values(by=['iso3cd', 'hazard']).reset_index(drop=True)

# Print table to console
print("\n" + "="*95)
print(f"{'Country':<25} | {'Hazard':<15} | {'Buildings AAL (USD)':<20} | {'Total AAL (USD)':<20} | {'Buildings Share (%)':<10}")
print("="*95)
for idx, row in share_df.iterrows():
    c_name = country_names.get(row['iso3cd'], row['iso3cd'])
    print(f"{c_name:<25} | {row['hazard']:<15} | {row['Buildings_AAL']:<20,.2f} | {row['Total_AAL']:<20,.2f} | {row['Share_Pct']:<10.2f}%")
print("="*95 + "\n")

# Save table as a text file in outputs directory
output_table_file = os.path.join(output_dir, 'GIRI_Buildings_Share_Table.txt')
with open(output_table_file, 'w', encoding='utf-8') as f:
    f.write("="*95 + "\n")
    f.write(f"{'Country':<25} | {'Hazard':<15} | {'Buildings AAL (USD)':<20} | {'Total AAL (USD)':<20} | {'Buildings Share (%)':<10}\n")
    f.write("="*95 + "\n")
    for idx, row in share_df.iterrows():
        c_name = country_names.get(row['iso3cd'], row['iso3cd'])
        f.write(f"{c_name:<25} | {row['hazard']:<15} | {row['Buildings_AAL']:<20,.2f} | {row['Total_AAL']:<20,.2f} | {row['Share_Pct']:<10.2f}%\n")
    f.write("="*95 + "\n")
print(f"Table successfully saved to: {output_table_file}")

def format_loss(val):
    if val >= 1e6:
        return f"{val/1e6:.1f} M"
    elif val >= 1e3:
        return f"{val/1e3:.1f} K"
    else:
        return f"{val:.0f}"

# Create a figure with one subplot for Earthquake and one for Floods
fig_share, (ax_eq, ax_fl) = plt.subplots(1, 2, figsize=(16, 8), dpi=150)

# Filter data for each hazard
eq_data = share_df[share_df['hazard'] == 'Earthquake'].copy()
fl_data = share_df[share_df['hazard'] == 'Flood'].copy()

# Add country labels for plotting
eq_data['Country_Label'] = eq_data['iso3cd'].map(country_names).fillna(eq_data['iso3cd'])
fl_data['Country_Label'] = fl_data['iso3cd'].map(country_names).fillna(fl_data['iso3cd'])

# Sort countries alphabetically for cleaner y-axis
eq_data = eq_data.sort_values(by='Country_Label', ascending=False)
fl_data = fl_data.sort_values(by='Country_Label', ascending=False)

# Earthquake subplot
bars_eq = ax_eq.barh(eq_data['Country_Label'], eq_data['Share_Pct'], color='#d62728', edgecolor='none', height=0.6)
ax_eq.set_title('Earthquake: "Buildings" Sector AAL Share (%)', fontsize=12, weight='bold', pad=15, color='#2c3e50')
ax_eq.set_xlabel('Share of Total Earthquake AAL (%)', fontsize=10, weight='bold')
ax_eq.set_xlim(0, 175)
ax_eq.grid(axis='x', linestyle='--', alpha=0.5)

# Add value labels inside/beside the bars
for bar, row in zip(bars_eq, eq_data.itertuples()):
    width = bar.get_width()
    label_text = f'{width:.1f}% ({format_loss(row.Buildings_AAL)} out of {format_loss(row.Total_AAL)})'
    ax_eq.text(width + 1.5, bar.get_y() + bar.get_height()/2, label_text, 
               va='center', ha='left', fontsize=7, color='#475569', weight='bold')

# Flood subplot
bars_fl = ax_fl.barh(fl_data['Country_Label'], fl_data['Share_Pct'], color='#1f77b4', edgecolor='none', height=0.6)
ax_fl.set_title('Flood: "Buildings" Sector AAL Share (%)', fontsize=12, weight='bold', pad=15, color='#2c3e50')
ax_fl.set_xlabel('Share of Total Flood AAL (%)', fontsize=10, weight='bold')
ax_fl.set_xlim(0, 175)
ax_fl.grid(axis='x', linestyle='--', alpha=0.5)

# Add value labels inside/beside the bars
for bar, row in zip(bars_fl, fl_data.itertuples()):
    width = bar.get_width()
    label_text = f'{width:.1f}% ({format_loss(row.Buildings_AAL)} out of {format_loss(row.Total_AAL)})'
    ax_fl.text(width + 1.5, bar.get_y() + bar.get_height()/2, label_text, 
               va='center', ha='left', fontsize=7, color='#475569', weight='bold')

# Main overall figure title
fig_share.suptitle('GIRI AAL: Share of "Buildings" Sector relative to Total Hazard AAL by Country', 
                   fontsize=15, weight='bold', y=0.98, color='#2c3e50')

# Adjust layout to fit titles and axes neatly
plt.tight_layout(rect=[0, 0.02, 1, 0.94])

# Save the figure
output_image_share = os.path.join(output_dir, 'GIRI_Buildings_Share_by_Country.png')
plt.savefig(output_image_share, dpi=200, bbox_inches='tight')

if is_jupyter:
    plt.show()
else:
    plt.close()
print(f"Buildings share subplots figure saved to: {output_image_share}")
print("Analysis complete!")

