"""
Process WUP2025 data files
- Filter DEGURBA Level1 data by columns and categories
- Filter Population by size class data by columns
- Filter for Sub-Saharan Africa countries only
- Save processed files to data/processed/WUP/
"""

import pandas as pd
import os
import sys

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import centralized country utilities
from src.utils.country_utils import load_wb_regional_classifications

# Load World Bank regional classifications
afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

def add_regional_aggregates(df, group_by_cols=['Category', 'Year'], agg_cols={'Pop': 'sum'}):
    """
    Add regional aggregates (AFE, AFW, SSA) to a DataFrame
    
    Args:
        df: DataFrame with ISO3_Code column and data to aggregate
        group_by_cols: List of columns to group by (in addition to region grouping)
        agg_cols: Dictionary of {column_name: aggregation_function} for aggregation
        
    Returns:
        DataFrame with regional aggregates appended
    """
    regional_data = []
    region_mappings = {
        'AFE': afe_countries,
        'AFW': afw_countries,
        'SSA': ssa_countries
    }
    
    # Get all unique combinations of grouping columns
    if group_by_cols:
        # Create a MultiIndex of all unique combinations
        group_values = df[group_by_cols].drop_duplicates()
        
        for _, group_row in group_values.iterrows():
            # Create filter for this group using query-style filtering
            group_data = df.copy()
            for col in group_by_cols:
                group_data = group_data[group_data[col] == group_row[col]]
            
            # Calculate aggregates for each region
            for region_code, country_list in region_mappings.items():
                region_data = group_data[group_data['ISO3_Code'].isin(country_list)]
                if not region_data.empty:
                    # Build the regional row
                    region_row = {'ISO3_Code': region_code}
                    
                    # Add grouping column values
                    for col in group_by_cols:
                        region_row[col] = group_row[col]
                    
                    # Add aggregated columns
                    for col, agg_func in agg_cols.items():
                        if agg_func == 'sum':
                            region_row[col] = region_data[col].sum()
                    
                    regional_data.append(region_row)
    
    # Convert regional data to DataFrame and append to main data
    if regional_data:
        regional_df = pd.DataFrame(regional_data)
        df = pd.concat([df, regional_df], ignore_index=True)
    
    return df

"""
Process WUP2025-DB-DEGURBA-Level1-Population-Surface-Data.csv
Keep only columns: ISO3_Code, Category, Year, Pop
Delete rows where Category is 'Cities and Towns' or 'Total'
Add regional aggregates for SSA, AFE, AFW
"""

# Read raw data
raw_path = os.path.join(project_root, 'data', 'raw', 'WUP2025', 
                        'WUP2025-DB-DEGURBA-Level1-Population-Surface-Data.csv')
df = pd.read_csv(raw_path, low_memory=False)

# Keep only specified columns
df = df[['ISO3_Code', 'Category', 'Year', 'Pop']]

# Filter for Sub-Saharan African countries only
df = df[df['ISO3_Code'].isin(ssa_countries)]

# Delete rows where Category is 'Cities and Towns' or 'Total'
df = df[~df['Category'].isin(['Cities and Towns', 'Total'])]

# Convert population from thousands to actual values
df['Pop'] = df['Pop'] * 1000

# Add regional aggregates
df = add_regional_aggregates(df, group_by_cols=['Category', 'Year'], agg_cols={'Pop': 'sum'})

# Calculate Pop_rel (share of total population for each year and ISO3_Code)
df['Pop_rel'] = df.groupby(['Year', 'ISO3_Code'])['Pop'].transform(lambda x: x / x.sum())

# Sort by year, ISO3_Code, and category
df = df.sort_values(['Year', 'ISO3_Code', 'Category'])

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)

# Save processed data
output_path = os.path.join(output_dir, 'WUP2025_Level1_Population_Surface_processed.csv')
df.to_csv(output_path, index=False)


"""
Process WUP2025-DB-DEGURBA-Population-by-size-class-of-cities.csv
Keep only columns: ISO3_Code, Category, Year, Cities, Pop
Add regional aggregates for SSA, AFE, AFW
"""

# Read raw data
raw_path = os.path.join(project_root, 'data', 'raw', 'WUP2025', 
                        'WUP2025-DB-DEGURBA-Population-by-size-class-of-cities.csv')
df = pd.read_csv(raw_path, low_memory=False)

# Keep only specified columns
df = df[['ISO3_Code', 'Category', 'Year', 'Cities', 'Pop']]

# Filter for Sub-Saharan African countries only
df = df[df['ISO3_Code'].isin(ssa_countries)]

# Convert population from thousands to actual values
df['Pop'] = df['Pop'] * 1000

# Add regional aggregates
df = add_regional_aggregates(df, group_by_cols=['Category', 'Year'], agg_cols={'Cities': 'sum', 'Pop': 'sum'})

# Calculate Pop_rel and Cities_rel (share of total for each year and ISO3_Code)
df['Pop_rel'] = df.groupby(['Year', 'ISO3_Code'])['Pop'].transform(lambda x: x / x.sum())
df['Cities_rel'] = df.groupby(['Year', 'ISO3_Code'])['Cities'].transform(lambda x: x / x.sum())

# Sort by year, ISO3_Code, and category
df = df.sort_values(['Year', 'ISO3_Code', 'Category'])

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)

# Save processed data
output_path = os.path.join(output_dir, 'WUP2025_Population_by_Size_Class_processed.csv')
df.to_csv(output_path, index=False)


"""
Process WUP2025-DB-National-Definitions-Population-Data.csv
Keep only columns: ISO3_Code, Category, Year, Pop
Delete rows where Category is 'Total'
Add Pop_Rel column (relative population share)
Filter for Sub-Saharan Africa countries only
Add regional aggregates for SSA, AFE, AFW
"""

# Read raw data
raw_path = os.path.join(project_root, 'data', 'raw', 'WUP2025', 
                        'WUP2025-DB-National-Definitions-Population-Data.csv')
df = pd.read_csv(raw_path, low_memory=False)

# Keep only specified columns
df = df[['ISO3_Code', 'Category', 'Year', 'Pop']]

# Filter for Sub-Saharan African countries only
df = df[df['ISO3_Code'].isin(ssa_countries)]

# Delete rows where Category is 'Total'
df = df[df['Category'] != 'Total']

# Convert population from thousands to actual values
df['Pop'] = df['Pop'] * 1000

# Add regional aggregates
df = add_regional_aggregates(df, group_by_cols=['Category', 'Year'], agg_cols={'Pop': 'sum'})

# Calculate Pop_Rel (share of total population for each year and ISO3_Code)
df['Pop_Rel'] = df.groupby(['Year', 'ISO3_Code'])['Pop'].transform(lambda x: x / x.sum())

# Sort by year, ISO3_Code, and category
df = df.sort_values(['Year', 'ISO3_Code', 'Category'])

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)

# Save processed data
output_path = os.path.join(output_dir, 'WUP2025_National_Definitions_Population_processed.csv')
df.to_csv(output_path, index=False)


# Pivot the data to get Urban and Rural in separate columns
pivot_df = df.pivot_table(
    index=['ISO3_Code', 'Year'],
    columns='Category',
    values='Pop',
    aggfunc='first'
).reset_index()

# Calculate urbanization metrics
pivot_df['Total_Pop'] = pivot_df['Urban'] + pivot_df['Rural']
pivot_df['Urbanization_Rate'] = pivot_df['Urban'] / pivot_df['Total_Pop']

# Rename columns for clarity
pivot_df = pivot_df.rename(columns={
    'Urban': 'Urban_Pop',
    'Rural': 'Rural_Pop'
})

output_path = os.path.join(output_dir, 'WUP2025_National_Definitions_Population_processed_pivoted.csv')
pivot_df.to_csv(output_path, index=False)
