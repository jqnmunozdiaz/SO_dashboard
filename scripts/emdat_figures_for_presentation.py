#%%
"""
EM-DAT Figures for Presentation
Creates visualizations of disaster data for AFW countries since 2000
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_wb_regional_classifications

# Load the processed EM-DAT data
data_file = "data/processed/african_disasters_emdat.csv"
df = pd.read_csv(data_file)

# Get AFW countries
afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

print(f"AFW countries: {afw_countries}")
print(f"Total AFW countries: {len(afw_countries)}")

# Filter for AFW countries only and year >= 2000
df_afw = df[df['ISO'].isin(afw_countries) & (df['Year'] >= 2001)]

# Remove epidemic and volcanic disasters from the analysis
df_afw = df_afw[~df_afw['Disaster Type'].isin(['Volcanic activity'])]

print(f"\nTotal disasters in AFW countries since 2000 (excluding epidemics and volcanic events): {len(df_afw)}")
print(f"Year range: {df_afw['Year'].min()} - {df_afw['Year'].max()}")

# Group by disaster type and sum the number of events
disaster_distribution = df_afw.groupby('Disaster Type')['Number of Events'].sum().sort_values(ascending=False)

# Define main categories to keep separate, group the rest as "Other"
main_categories = ['Flood', 'Drought', 'Storm', 'Epidemic']

# Create new distribution with "Other" category
disaster_dist_grouped = {}
other_count = 0
other_types = []  # Track what goes into "Other"

for disaster_type, count in disaster_distribution.items():
    if disaster_type in main_categories:
        disaster_dist_grouped[disaster_type] = count
    else:
        other_count += count
        other_types.append((disaster_type, count))

if other_count > 0:
    disaster_dist_grouped['Other'] = other_count

# Convert to Series and sort
disaster_distribution = pd.Series(disaster_dist_grouped).sort_values(ascending=False)

# Print what's included in "Other"
if other_types:
    print("\n'Other' category includes:")
    for disaster_type, count in sorted(other_types, key=lambda x: x[1], reverse=True):
        print(f"  - {disaster_type}: {count:,} events")

# Create pie chart
fig, ax = plt.subplots(figsize=(12, 8))

# Define custom colors - blue for Flood, orange for Drought, gray for Storm
color_map = {
    'Flood': '#90D5FF',  # Light Blue
    'Drought': '#ff7f0e',  # Orange
    'Storm': '#7f7f7f',  # Gray
    'Epidemic': '#27AE60',  # Green
    'Other': '#D5D8DC',  # Light Gray
}
# Create color list based on disaster types
colors = [color_map.get(disaster_type, plt.cm.Set3(i)) 
          for i, disaster_type in enumerate(disaster_distribution.index)]

# Create the pie chart
wedges, texts, autotexts = ax.pie(
    disaster_distribution.values, 
    labels=disaster_distribution.index,
    autopct='%1.0f%%',  # No decimal places
    startangle=90,
    colors=colors,
    textprops={'fontsize': 20, 'fontweight': 'bold'}  # Larger label text
)

# Enhance the percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(20)  # Larger percentage text

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

plt.tight_layout()

# Save the figure
output_dir = "outputs/figures"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "afw_disaster_distribution_pie_chart.png")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")

# Show the plot
plt.show()

#%% Bar Chart: People Affected by Disaster Type Over Time (configurable year periods)

# Configuration: Set the number of years per period
years_per_period = 5
start_year = 2001
end_year = 2025

# Use same categories as pie chart: main ones separate, rest as "Other"
bar_main_categories = ['Flood', 'Drought', 'Storm', 'Epidemic']

# Tag each row as its disaster type or "Other"
df_bar = df_afw[(df_afw['Year'] >= start_year) & (df_afw['Year'] <= end_year)].copy()
df_bar['Bar Type'] = df_bar['Disaster Type'].apply(
    lambda x: x if x in bar_main_categories else 'Other'
)

# Automatically create period bins
def assign_period(year):
    period_start = ((year - start_year) // years_per_period) * years_per_period + start_year
    period_end = min(period_start + years_per_period - 1, end_year)
    return f'{period_start}-{period_end}'

df_bar['Period'] = df_bar['Year'].apply(assign_period)

# Group by period and disaster type, sum the total affected
affected_by_period = df_bar.groupby(['Period', 'Bar Type'])['Total Affected'].sum().unstack(fill_value=0)

# Ensure all categories are present
bar_all_categories = ['Flood', 'Drought', 'Storm', 'Epidemic', 'Other']
for disaster_type in bar_all_categories:
    if disaster_type not in affected_by_period.columns:
        affected_by_period[disaster_type] = 0

# Reorder columns to match pie chart order
affected_by_period = affected_by_period[bar_all_categories]

# Sort periods chronologically (they're already in the right format)
affected_by_period = affected_by_period.sort_index()

print(f"\n\nPeople affected by disaster type (by {years_per_period}-year periods):")
print(affected_by_period)

# Create bar chart
fig, ax = plt.subplots(figsize=(14, 8))

# Create stacked bar chart using same colors as pie chart
x = range(len(affected_by_period.index))
width = 0.6

bottom = pd.Series([0] * len(affected_by_period), index=affected_by_period.index)
for disaster_type in bar_all_categories:
    ax.bar(x, affected_by_period[disaster_type], width,
           label=disaster_type, color=color_map[disaster_type], bottom=bottom)
    bottom = bottom + affected_by_period[disaster_type]

# Customize the chart
ax.set_ylabel('People Affected', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(affected_by_period.index, fontsize=14, fontweight='bold')
ax.tick_params(axis='y', labelsize=14)
ax.legend(fontsize=14, loc='upper left')

# Format y-axis to show numbers in millions
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y/1e6:.0f}M'))

# Add grid for better readability
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()

# Save the figure
output_file_bar = os.path.join(output_dir, "afw_people_affected_by_period_bar_chart.png")
plt.savefig(output_file_bar, dpi=300, bbox_inches='tight')
print(f"\nBar chart saved to: {output_file_bar}")

# Show the plot
plt.show()
# %%
