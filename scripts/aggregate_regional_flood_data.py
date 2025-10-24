"""
Aggregate flood exposure data for regional codes (SSA, AFE, AFW)
by summing values from constituent countries
"""

import pandas as pd
import os

# Load WB Classification to get regional mappings
wb_classification = pd.read_csv('data/Definitions/WB_Classification.csv')

# Create regional mappings
regional_mappings = {
    'AFE': wb_classification[wb_classification['Subregion Code'] == 'AFE']['ISO3'].tolist(),
    'AFW': wb_classification[wb_classification['Subregion Code'] == 'AFW']['ISO3'].tolist(),
    'SSA': wb_classification[wb_classification['Region Code'] == 'SSA']['ISO3'].tolist()
}

print(f"Regional mappings created:")
print(f"  AFE: {len(regional_mappings['AFE'])} countries")
print(f"  AFW: {len(regional_mappings['AFW'])} countries")
print(f"  SSA: {len(regional_mappings['SSA'])} countries")

# Load the flood exposure data files
flood_files = [
    'data/raw/Fathom3-GHSL/country_ftm3_current_ghsl2023_built_s.csv',
    'data/raw/Fathom3-GHSL/country_ghsl2023_built_s.csv',
    'data/raw/Fathom3-GHSL/country_ftm3_current_ghsl2023_pop.csv',
    'data/raw/Fathom3-GHSL/country_ghsl2023_pop.csv'
]

for file_path in flood_files:
    print(f"\nProcessing: {file_path}")
    
    # Read the original data
    df = pd.read_csv(file_path)
    original_count = len(df)
    
    # Filter for flood_type if column exists
    if 'flood_type' in df.columns:
        df = df[df['flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED']
        print(f"  Filtered to {len(df)} rows with flood_type='FLUVIAL_PLUVIAL_DEFENDED'")
    
    # Drop unwanted columns
    columns_to_drop = [
        'ftm3_ghsl_new_pop_#', 'ftm3_ghsl_rate_pop_%', 'ftm3_ghsl_new_built_s_km2', 'ftm3_ghsl_rate_built_s_%',
        'ghsl_new_pop_#', 'ghsl_rate_pop_%', 'ghsl_new_built_s_km2', 'ghsl_rate_built_s_%', 'ghsl_type', 'fathom_year'
    ]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    
    # List to store regional aggregates
    regional_data = []
    
    # Process each region
    for region_code, country_list in regional_mappings.items():
        
        # Filter data for countries in this region
        region_df = df[df['ISO_A3'].isin(country_list)].copy()
        
        if region_df.empty:
            print(f"    Warning: No data found for {region_code}")
            continue
        
        # Determine grouping columns based on file type
        if 'flood_type' in df.columns and 'return_period' in df.columns:
            # This is the flood exposure file (ftm3_current)
            group_cols = ['ghsl_year', 'flood_type', 'return_period']
            
            # Determine if it's built_s or pop based on column names
            if 'ftm3_ghsl_total_built_s_km2' in df.columns:
                sum_cols = ['ftm3_ghsl_total_built_s_km2']
            elif 'ftm3_ghsl_total_pop_#' in df.columns:
                sum_cols = ['ftm3_ghsl_total_pop_#']
        else:
            # This is the total file (non-flood)
            group_cols = ['ghsl_year']
            
            # Determine if it's built_s or pop based on column names
            if 'ghsl_total_built_s_km2' in df.columns:
                sum_cols = ['ghsl_total_built_s_km2']
            elif 'ghsl_total_pop_#' in df.columns:
                sum_cols = ['ghsl_total_pop_#']
        
        # Group and sum
        aggregated = region_df.groupby(group_cols, as_index=False)[sum_cols].sum()
        
        # Add region code
        aggregated['ISO_A3'] = region_code
        
        # Reorder columns to match original
        aggregated = aggregated[df.columns]
        
        regional_data.append(aggregated)
    
    # Combine original data with regional aggregates
    if regional_data:
        all_regional = pd.concat(regional_data, ignore_index=True)
        combined = pd.concat([df, all_regional], ignore_index=True)
        
        # Save to processed folder instead of overwriting raw data
        output_path = file_path.replace('data/raw/Fathom3-GHSL', 'data/processed/flood')
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        combined.to_csv(output_path, index=False)
    else:
        print(f"  No regional data to add")

print("\n✅ Regional flood data aggregation complete!")


#%%
# Load the processed flood population exposure file
flood_pop_path = 'data/processed/flood/country_ftm3_current_ghsl2023_pop.csv'
flood_data = pd.read_csv(flood_pop_path)

# Load the processed total population file
total_pop_path = 'data/processed/flood/country_ghsl2023_pop.csv'
total_pop_data = pd.read_csv(total_pop_path)

# Merge flood data with total population data on ISO_A3 and ghsl_year
merged_data = flood_data.merge(total_pop_data[['ISO_A3', 'ghsl_year', 'ghsl_total_pop_#']], on=['ISO_A3', 'ghsl_year'], how='left')

# Compute relative exposure percentage
merged_data['relative_exposure_pct'] = (merged_data['ftm3_ghsl_total_pop_#'] / merged_data['ghsl_total_pop_#']) * 100

# Resave the updated file
merged_data.to_csv(flood_pop_path, index=False)

#%%
print("\n✅ Relative exposure calculation complete for population data!")

# Load the processed flood builtup exposure file
flood_builtup_path = 'data/processed/flood/country_ftm3_current_ghsl2023_built_s.csv'
flood_builtup_data = pd.read_csv(flood_builtup_path)

# Load the processed total builtup file
total_builtup_path = 'data/processed/flood/country_ghsl2023_built_s.csv'
total_builtup_data = pd.read_csv(total_builtup_path)

# Merge flood builtup data with total builtup data on ISO_A3 and ghsl_year
merged_builtup_data = flood_builtup_data.merge(total_builtup_data[['ISO_A3', 'ghsl_year', 'ghsl_total_built_s_km2']], on=['ISO_A3', 'ghsl_year'], how='left')

# Compute relative exposure percentage
merged_builtup_data['relative_exposure_pct'] = (merged_builtup_data['ftm3_ghsl_total_built_s_km2'] / merged_builtup_data['ghsl_total_built_s_km2']) * 100

# Resave the updated file
merged_builtup_data.to_csv(flood_builtup_path, index=False)

print("\n✅ Relative exposure calculation complete for builtup data!")