#%%
"""
Merge Africapolis_GIS_2024 with agglomeration_population_stats.csv
Filter Africapolis for 2020 geometry year, create ID column, and merge with population data
Includes function to visualize CAGR distributions by country with variability analysis
"""

import pandas as pd
import geopandas as gpd
import os
import numpy as np
import matplotlib.pyplot as plt

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths
africapolis_gpkg = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')
agglomeration_csv = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025', 'agglomeration_population_stats.csv')
agglomeration_builtup_csv = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025', 'agglomeration_builtup_stats.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_2020_agglomeration_merged.csv')

def create_cagr_distribution_plot(df, cagr_column, title_suffix="", output_filename=None):
    """
    Create an 8x6 grid visualization showing CAGR distributions by country with variability analysis

    Parameters:
    df (pd.DataFrame): DataFrame containing the data
    cagr_column (str): Name of the column containing CAGR values (as fractions, e.g., 0.02 = 2%)
    title_suffix (str): Optional suffix to add to the plot title
    output_filename (str): Optional filename to save the plot (without extension)

    Returns:
    matplotlib.figure.Figure: The created figure object
    """
    # Get unique ISO3 codes sorted alphabetically
    countries = sorted(df['ISO3_africapolis'].unique())

    # Create figure with 8x6 subplots (48 total)
    fig, axes = plt.subplots(8, 6, figsize=(24, 32))
    axes = axes.flatten()

    # Plot distribution for each country
    for idx, iso3 in enumerate(countries):
        ax = axes[idx]

        # Filter data for this country
        country_data = df[df['ISO3_africapolis'] == iso3][cagr_column].dropna()

        # Get country name (try to find it from the data)
        country_name = iso3  # Default to ISO3
        try:
            # Look for country name in various possible columns
            name_cols = ['Country', 'Country_Name', 'country_name']
            for col in name_cols:
                if col in df.columns:
                    names = df[df['ISO3_africapolis'] == iso3][col].dropna()
                    if len(names) > 0:
                        country_name = names.iloc[0]
                        break
        except:
            pass

        if len(country_data) > 0:
            # Calculate variability measures
            mean_val = country_data.mean() * 100
            median_val = country_data.median() * 100
            std_val = country_data.std() * 100
            cv = (std_val / abs(mean_val)) * 100 if mean_val != 0 else 0  # Coefficient of variation
            range_val = (country_data.max() - country_data.min()) * 100

            # Plot histogram
            ax.hist(country_data * 100, bins=20, edgecolor='black', alpha=0.7, color='steelblue')

            # Add statistics lines
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}%')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'Median: {median_val:.2f}%')

            # Color code based on variability (low variability = blue, high = red)
            if cv < 10:  # Low variability
                variability_color = 'blue'
                variability_label = f'Low Var (CV: {cv:.1f}%)'
            elif cv < 25:  # Medium variability
                variability_color = 'orange'
                variability_label = f'Med Var (CV: {cv:.1f}%)'
            else:  # High variability
                variability_color = 'red'
                variability_label = f'High Var (CV: {cv:.1f}%)'

            # Add variability indicator in title
            ax.set_title(f'{iso3} - {country_name}\n(n={len(country_data)}) | {variability_label}',
                        fontsize=9, fontweight='bold', color=variability_color)

            ax.set_xlabel(f'{cagr_column.replace("_", " ").title()} (%)', fontsize=8)
            ax.set_ylabel('Frequency', fontsize=8)
            ax.legend(fontsize=7, loc='upper right')
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=7)

            # Add variability text in bottom left
            ax.text(0.02, 0.02, f'Std: {std_val:.2f}%\nRange: {range_val:.2f}%',
                    transform=ax.transAxes, fontsize=7, verticalalignment='bottom',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        else:
            ax.text(0.5, 0.5, f'{iso3}\nNo Data',
                    ha='center', va='center', fontsize=10, transform=ax.transAxes)
            ax.set_title(f'{iso3} - {country_name}', fontsize=10, fontweight='bold')

    # Hide any unused subplots
    for idx in range(len(countries), 48):
        axes[idx].axis('off')

    # Create title
    column_display_name = cagr_column.replace("_", " ").replace("cagr", "CAGR").title()
    full_title = f'Distribution of {column_display_name} by Country\nColor-coded by variability (CV: Coefficient of Variation)'
    if title_suffix:
        full_title += f' {title_suffix}'

    plt.suptitle(full_title, fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()

    # Save figure if filename provided
    if output_filename:
        output_path = os.path.join(project_root, 'data', 'processed', f'{output_filename}.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")

    return fig

#%% [Data Processing Section]
africapolis_gdf = gpd.read_file(africapolis_gpkg)
agglomeration_df = pd.read_csv(agglomeration_csv)
agglomeration_builtup_df = pd.read_csv(agglomeration_builtup_csv)

# Get unique ISO3 codes sorted alphabetically
countries = sorted(agglomeration_df['ISO3'].unique())

# Step 1: Filter Africapolis for Select_Geometry_Year == 2020
africapolis_2020 = africapolis_gdf[africapolis_gdf['Select_Geometry_Year'] == 2020].copy()

# Step 2: Create ID column by concatenating ISO3 and Agglomeration_ID
required_cols = ['ISO3', 'Agglomeration_ID']
missing_cols = [col for col in required_cols if col not in africapolis_2020.columns]

africapolis_2020 = africapolis_2020[africapolis_2020['ISO3'].isin(countries)].copy()

# Create the ID column
africapolis_2020['unique_id'] = africapolis_2020['ISO3'] + '_' + africapolis_2020['Agglomeration_ID'].astype(int).astype(str)

# Step 3: Merge with agglomeration data
merged_df = pd.merge(
    africapolis_2020,
    agglomeration_df,
    on='unique_id',
    how='outer',  # Keep all records from both datasets
    suffixes=('_africapolis', '_agglomeration'),
    indicator=False)

# Step 4: Merge with builtup data
merged_df = pd.merge(
    merged_df,
    agglomeration_builtup_df[['unique_id', 'worldpop_built_cagr_2015_2020']],  # Only merge the builtup CAGR column
    on='unique_id',
    how='left',  # Left join to keep all existing records
    suffixes=('', '_builtup')
)

# Drop geometry column if present, then save merged data
merged_df = merged_df.drop(columns=['geometry'])

merged_df = merged_df[[
    'Agglomeration_ID',
    'Agglomeration_Name_africapolis',
    'ISO3_africapolis',
    'Population_2015',
    'Population_2020',
    'worldpop_pop_2015',
    'worldpop_pop_2020',
    'worldpop_pop_cagr_2015_2020',
    'worldpop_built_cagr_2015_2020'
]]

# Remove cities where Population_2015 == 0, then rename population columns
merged_df = merged_df[merged_df['Population_2015'].fillna(0) != 0].copy()

merged_df = merged_df.rename(columns={'Population_2015': 'africapolis_pop_2015', 'Population_2020': 'africapolis_pop_2020'})

merged_df.to_csv(output_file, index=False)

df = merged_df

# Ensure numeric types
df['africapolis_pop_2015'] = pd.to_numeric(df['africapolis_pop_2015'], errors='coerce')
df['africapolis_pop_2020'] = pd.to_numeric(df['africapolis_pop_2020'], errors='coerce')

# Compute 5-year CAGR (2015 -> 2020) safely (as fractional growth, e.g. 0.02 == 2%)
periods = 5
valid = (df['africapolis_pop_2015'] > 0) & (df['africapolis_pop_2020'] > 0)
df.loc[valid, 'africapolis_pop_cagr_2015_2020'] = (
    (df.loc[valid, 'africapolis_pop_2020'] / df.loc[valid, 'africapolis_pop_2015']) ** (1 / periods) - 1
)
df.loc[~valid, 'africapolis_pop_cagr_2015_2020'] = np.nan

#%% [Visualization Section]
# Create visualization for worldpop_pop_cagr_2015_2020
fig1 = create_cagr_distribution_plot(
    df,
    'worldpop_pop_cagr_2015_2020',
    title_suffix="(WorldPop Data)",
    output_filename='worldpop_population_cagr_distributions_by_country_with_variability'
)

plt.show()

# Create visualization for africapolis_pop_cagr_2015_2020
fig2 = create_cagr_distribution_plot(
    df,
    'africapolis_pop_cagr_2015_2020',
    title_suffix="(Africapolis Data)",
    output_filename='africapolis_population_cagr_distributions_by_country_with_variability'
)

plt.show()

# Create visualization for worldpop_built_cagr_2015_2020
fig3 = create_cagr_distribution_plot(
    df,
    'worldpop_built_cagr_2015_2020',
    title_suffix="(Built-up Area Growth)",
    output_filename='worldpop_builtup_cagr_distributions_by_country_with_variability'
)

plt.show()

#%% 
