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

# ==============================================================================
# SECTION 1A: Original Grid layout of Pie Charts per Country
# ==============================================================================
print("\n" + "="*80)
print(" GENERATING ORIGINAL PIE CHART GRID LAYOUT ")
print("="*80)

# Determine grid layout (aiming for ~6 columns)
cols = 6
rows = int(np.ceil(num_countries / cols))

# Create the figure with high resolution
fig_grid, axes_grid = plt.subplots(rows, cols, figsize=(20, 3.2 * rows), dpi=150)
axes_grid = axes_grid.flatten()  # Flatten the 2D array of axes for easy indexing

# Style configuration
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

for i, country_code in enumerate(countries):
    ax = axes_grid[i]
    
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
for j in range(num_countries, len(axes_grid)):
    fig_grid.delaxes(axes_grid[j])
    
# Add a global main title
fig_grid.suptitle('GIRI Overall Average Annual Loss (AAL) by Hazard per Country', 
             fontsize=18, weight='bold', y=0.98, color='#2c3e50')

# Add a unified global legend
legend_handles_grid = [plt.Rectangle((0,0),1,1, color=hazard_colors[h]) for h in hazards]
fig_grid.legend(legend_handles_grid, hazards, loc='lower center', ncol=len(hazards), 
           fontsize=12, frameon=True, facecolor='#f8f9fa', edgecolor='#e2e8f0',
           bbox_to_anchor=(0.5, 0.01))

# Tight layout with space for main title and legend
fig_grid.tight_layout(rect=[0, 0.04, 1, 0.95])

# Save the grid figure (backward compatible name + grid name)
output_image_grid = os.path.join(output_dir, 'GIRI_AAL_by_Country_Grid.png')
print(f"Saving overall AAL grid layout figure to: {output_image}")
fig_grid.savefig(output_image, dpi=200, bbox_inches='tight')
print(f"Saving a copy of grid layout to: {output_image_grid}")
fig_grid.savefig(output_image_grid, dpi=200, bbox_inches='tight')

# Close original figure
plt.close(fig_grid)

# ==============================================================================
# SECTION 1B: Map generation with overlaid pie charts
# ==============================================================================
print("\n" + "="*80)
print(" GENERATING NEW GEOGRAPHICAL MAP OVERLAY ")
print("="*80)

import geopandas as gpd
import urllib.request
import json

# Define centroids fallback for major SSA countries to guarantee 100% robust layout
CENTROID_FALLBACKS = {
    'AGO': (17.87, -11.20), 'BDI': (29.91, -3.37), 'BEN': (2.31, 9.30), 'BFA': (-1.56, 12.23),
    'BWA': (23.95, -22.32), 'CAF': (20.93, 6.61), 'CIV': (-5.54, 7.54), 'CMR': (12.35, 7.36),
    'COD': (23.65, -2.87), 'COG': (15.82, -0.22), 'COM': (43.87, -11.87), 'CPV': (-23.04, 16.0),
    'ERI': (39.78, 15.17), 'ETH': (39.78, 9.14), 'GAB': (11.60, -0.80), 'GHA': (-1.02, 7.94),
    'GIN': (-10.94, 9.94), 'GMB': (-15.31, 13.44), 'GNB': (-15.18, 12.01), 'GNQ': (10.26, 1.65),
    'KEN': (37.90, -1.28), 'LBR': (-9.42, 6.42), 'LSO': (28.23, -29.60), 'MDG': (46.86, -18.76),
    'MLI': (-3.99, 17.57), 'MOZ': (35.52, -18.66), 'MRT': (-10.94, 21.0), 'MUS': (57.55, -20.34),
    'MWI': (34.30, -13.25), 'NAM': (17.29, -22.95), 'NER': (8.08, 17.60), 'NGA': (8.67, 9.08),
    'RWA': (29.87, -1.94), 'SDN': (30.21, 12.86), 'SEN': (-14.45, 14.49), 'SLE': (-11.77, 8.46),
    'SOM': (46.19, 5.15), 'SSD': (30.21, 4.85), 'STP': (6.61, 0.20), 'SWZ': (31.46, -26.52),
    'SYC': (55.49, -4.67), 'TCD': (18.73, 15.45), 'TGO': (0.82, 8.61), 'TZA': (34.88, -6.36),
    'UGA': (32.29, 1.37), 'ZAF': (25.04, -28.47), 'ZMB': (27.84, -13.13), 'ZWE': (29.15, -19.01)
}

# Coordinate offsets to resolve overlap issues (lon_offset, lat_offset, pie_size_scale)
MAP_ADJUSTMENTS = {
    'BDI': (3.0, -1.5, 0.85),    # Shift Burundi right & down
    'RWA': (-3.0, 1.5, 0.85),    # Shift Rwanda left & up
    'LSO': (3.5, 0.5, 0.85),     # Shift Lesotho out of South Africa
    'SWZ': (3.5, -1.5, 0.85),    # Shift Eswatini out of South Africa
    'CPV': (-4.0, 0.0, 0.9),     # Cape Verde
    'COM': (3.0, 0.5, 0.85),     # Comoros
    'MUS': (3.5, -1.0, 0.85),    # Mauritius
    'SYC': (3.0, 1.0, 0.85),     # Seychelles
    'STP': (-2.5, -1.5, 0.85),   # São Tomé
    'GMB': (-2.0, 1.5, 0.8),     # Gambia
}

# Local GeoJSON cache path
geojson_cache_path = os.path.join(project_root, 'data', 'Definitions', 'ne_110m_admin_0_countries.geojson')

# Download the boundaries GeoJSON locally if not cached
if not os.path.exists(geojson_cache_path):
    print("GeoJSON cache not found. Downloading country boundaries...")
    try:
        url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson"
        urllib.request.urlretrieve(url, geojson_cache_path)
        print("GeoJSON boundaries downloaded and cached successfully.")
    except Exception as e:
        print(f"Warning: Could not download country boundaries ({e}). Falling back to coordinates grid.")

# Read boundaries
use_map = False
ssa_world = None
if os.path.exists(geojson_cache_path):
    try:
        world = gpd.read_file(geojson_cache_path)
        # Filter for SSA countries in our dataset
        ssa_world = world[world['iso_a3'].isin(countries)].copy()
        if not ssa_world.empty:
            use_map = True
            print("Loaded geopandas base map of Sub-Saharan Africa successfully.")
    except Exception as e:
        print(f"Warning: Could not parse GeoJSON boundaries with Geopandas ({e}). Falling back to grid layout.")

# Create the figure with high resolution
fig_map, ax_map = plt.subplots(figsize=(16, 12), dpi=150)

# Apply a professional visual style
ax_map.set_facecolor('#f8fafc')  # Clean soft background
fig_map.patch.set_facecolor('#f1f5f9')

if use_map and ssa_world is not None:
    # Plot countries background with a premium light slate color
    ssa_world.plot(ax=ax_map, color='#e2e8f0', edgecolor='#94a3b8', linewidth=0.6, alpha=0.9)
    # Style the bounding coordinates of Sub-Saharan Africa
    ax_map.set_xlim(-25, 58)
    ax_map.set_ylim(-38, 22)
    ax_map.set_xlabel("Longitude (Degrees)", fontsize=10, weight='bold', color='#475569')
    ax_map.set_ylabel("Latitude (Degrees)", fontsize=10, weight='bold', color='#475569')
    ax_map.set_title("GIRI Average Annual Loss (AAL) by Hazard (Map Overlay)", fontsize=14, weight='bold', pad=15, color='#1e293b')
    ax_map.grid(True, linestyle='--', color='#e2e8f0', alpha=0.5)
else:
    # Grid Fallback if shapefile is unavailable
    print("Rendering as a scatter grid coordinate system.")
    ax_map.set_xlim(-30, 60)
    ax_map.set_ylim(-40, 25)
    ax_map.set_xlabel("Longitude (Degrees)", fontsize=10, weight='bold', color='#475569')
    ax_map.set_ylabel("Latitude (Degrees)", fontsize=10, weight='bold', color='#475569')
    ax_map.set_title("GIRI Average Annual Loss (AAL) by Hazard (Scatter Coordinate Overlay)", fontsize=14, weight='bold', pad=15, color='#1e293b')
    ax_map.grid(True, linestyle='--', color='#cbd5e1', alpha=0.3)

# Plot pie charts on top of each country
for country_code in countries:
    # 1. Get centroid coordinates
    lon, lat = None, None
    if use_map and ssa_world is not None:
        country_geom = ssa_world[ssa_world['iso_a3'] == country_code]
        if not country_geom.empty:
            geom = country_geom.geometry.values[0]
            if geom is not None and not geom.is_empty:
                centroid = geom.centroid
                lon, lat = centroid.x, centroid.y

    # Fallback to predefined centroids if map geometry is missing
    if lon is None or lat is None:
        lon, lat = CENTROID_FALLBACKS.get(country_code, (None, None))
        
    if lon is None or lat is None:
        continue  # Skip if coordinates are completely unknown

    # 2. Get data for this country
    country_data = agg_df[agg_df['iso3cd'] == country_code]
    
    # Aggregate loss by hazard for this country
    hazard_losses = country_data.groupby('hazard')['Loss'].sum()
    hazard_losses = hazard_losses[hazard_losses > 0]
    
    # 3. Determine custom scale and offset to avoid overlays
    offset_lon, offset_lat, scale_factor = MAP_ADJUSTMENTS.get(country_code, (0.0, 0.0, 1.0))
    lon_p = lon + offset_lon
    lat_p = lat + offset_lat
    
    # Default base size is 2.4 degrees width/height on the map
    base_pie_size = 2.4
    pie_size = base_pie_size * scale_factor
    
    # Draw leader line from original country centroid to shifted pie chart position if shifted
    if offset_lon != 0.0 or offset_lat != 0.0:
        ax_map.plot([lon, lon_p], [lat, lat_p], color='#64748b', linestyle='-', linewidth=0.7, zorder=2)
        ax_map.scatter([lon], [lat], color='#ef4444', s=6, zorder=3)  # Centroid bullet point

    if hazard_losses.empty or hazard_losses.sum() == 0:
        # Draw a blank gray placeholder circle for countries with 0 loss
        ax_inset = ax_map.inset_axes([lon_p - pie_size/2, lat_p - pie_size/2, pie_size, pie_size], transform=ax_map.transData)
        ax_inset.pie([1], colors=['#e2e8f0'], wedgeprops={'edgecolor': '#94a3b8', 'linewidth': 0.5})
        ax_inset.axis('equal')
    else:
        # Prepare sizes and labels
        labels = hazard_losses.index.tolist()
        sizes = hazard_losses.values
        slice_colors = [hazard_colors[label] for label in labels]
        
        # Add inset axis for the pie chart
        ax_inset = ax_map.inset_axes([lon_p - pie_size/2, lat_p - pie_size/2, pie_size, pie_size], transform=ax_map.transData)
        ax_inset.pie(
            sizes, 
            colors=slice_colors,
            startangle=140,
            wedgeprops={'edgecolor': 'white', 'linewidth': 0.4}
        )
        ax_inset.axis('equal')
        
    # Label the country code below the pie chart
    ax_map.text(lon_p, lat_p - pie_size/2 - 0.25, country_code, fontsize=7.5, weight='bold', 
            ha='center', va='top', color='#1e293b',
            bbox=dict(boxstyle='square,pad=0.15', fc='white', ec='#cbd5e1', lw=0.4, alpha=0.85))

# Add a global main title
fig_map.suptitle('Sub-Saharan Africa: GIRI Overall Average Annual Loss (AAL) by Hazard', 
             fontsize=18, weight='bold', y=0.96, color='#0f172a')

# Add a unified legend at the bottom
legend_handles_map = [plt.Rectangle((0,0),1,1, color=hazard_colors[h]) for h in hazards]
ax_map.legend(legend_handles_map, hazards, loc='lower center', ncol=len(hazards), 
          fontsize=10, frameon=True, facecolor='#ffffff', edgecolor='#cbd5e1',
          bbox_to_anchor=(0.5, 0.02))

# Save the map figure
output_image_map = os.path.join(output_dir, 'GIRI_AAL_by_Country_Map.png')
print(f"Saving overall AAL map overlay figure to: {output_image_map}")
fig_map.savefig(output_image_map, dpi=200, bbox_inches='tight')

# Check if running in Jupyter notebook / IPython to determine whether to show or close the plot
try:
    shell = get_ipython().__class__.__name__
    is_jupyter = (shell == 'ZMQInteractiveShell')
except NameError:
    is_jupyter = False

if is_jupyter:
    plt.show()
else:
    plt.close(fig_map)

print("Grid and Map figures generated and saved successfully!")

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

