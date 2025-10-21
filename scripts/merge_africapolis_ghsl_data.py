#%%
"""
Merge Africapolis GHSL 2023 population and built surface data.

This script:
1. Loads population and built surface data from separate CSV files
2. Verifies that agglosID and ghsl_year uniquely define rows in each dataset
3. Merges the datasets on agglosID and ghsl_year
4. Outputs the merged dataset to a CSV file
"""

import pandas as pd
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Define file paths
pop_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_pop.csv')
built_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_built_s.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl2023_merged.csv')

pop_df = pd.read_csv(pop_file)
built_df = pd.read_csv(built_file)

# Merge datasets
df = pd.merge(pop_df, built_df, on=['agglosID', 'ghsl_year'], how='outer', suffixes=('_pop', '_built'))

# Handle duplicated columns (ISO3, agglosName, ghsl_type) Keep the _pop versions since they should be the same
df['ISO3'] = df['ISO3_pop']
df['agglosName'] = df['agglosName_pop']
df = df.drop(['ISO3_pop', 'ISO3_built'], axis=1)
df = df.drop(['agglosName_pop', 'agglosName_built'], axis=1)
df = df.drop(['ghsl_type_pop', 'ghsl_type_built'], axis=1)

# Drop specified columns
df = df.drop(['ghsl_new_pop_#', 'ghsl_rate_pop_%', 'ghsl_new_built_s_km2', 'ghsl_rate_built_s_%'], axis=1)

# Reorder columns
df = df[['ISO3', 'agglosName', 'agglosID', 'ghsl_year', 'ghsl_total_pop_#', 'ghsl_total_built_s_km2']]

# Rename cols
df = df.rename(columns={'ghsl_year': 'year','ghsl_total_pop_#': 'pop', 'ghsl_total_built_s_km2': 'built_up'})

df = df.dropna()

year1 = 2000
year2 = 2020
df = df[df['year'].isin([year1, year2])]

#%%
# Calculate CAGR (Compound Annual Growth Rate) between 2010 and 2020
# CAGR = (End Value / Start Value) ^ (1 / number of years) - 1

def calculate_cagr(group, year1, year2):
    """Calculate CAGR for a single agglomeration between year 1 and year 2"""
    if len(group) != 2:
        return None

    # Sort by year
    group = group.sort_values('year')
    
    diff = year2 - year1
    
    start_val = group.iloc[0]
    end_val = group.iloc[1]

    # Check that we have 2000 and 2020
    if start_val['year'] != year1 or end_val['year'] != year2:
        return None
    
    start_pop = start_val['pop']
    end_pop = end_val['pop']
    start_built = start_val['built_up']
    end_built = end_val['built_up']
    
    # Calculate CAGR only if start values are positive
    if start_pop > 0 and start_built > 0:
        cagr_pop = (end_pop / start_pop) ** (1 / diff) - 1
        cagr_built = (end_built / start_built) ** (1 / diff) - 1
    else:
        cagr_pop = None
        cagr_built = None
    
    return pd.Series({
        'pop_2010': start_pop,
        'pop_2020': end_pop,
        'pop_cagr': cagr_pop,
        'built_up_2010': start_built,
        'built_up_2020': end_built,
        'built_up_cagr': cagr_built
    })

# Group by agglomeration and calculate CAGR
cagr_df = df.groupby(['ISO3', 'agglosID', 'agglosName']).apply(calculate_cagr, year1=year1, year2=year2).reset_index()

cagr_df['size_category'] = pd.cut(
    cagr_df['pop_2020'], 
    bins=[0, 300000, 500000, 1000000, 5000000, 10000000, float('inf')], 
    labels=['Fewer than 300 000', '300 000 to 500 000', '500 000 to 1 million', '1 to 5 million', '5 to 10 million', '10 million or more']
)

cagr_df = cagr_df.dropna()

# Save CAGR data
cagr_output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl2023_cagr_{}_{}.csv'.format(year1, year2))
os.makedirs(os.path.dirname(cagr_output_file), exist_ok=True)
cagr_df.to_csv(cagr_output_file, index=False)

#%%
