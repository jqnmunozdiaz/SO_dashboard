#%%
'''
Project flood risk using built-up per capita estimates for 2050.

Two options were explored: constant or trend. 
Final version uses CONSTANT approach because it is a projection "as if" current conditions persist.
The trend approach assumes we can predict built-up per capita, which is not reliable with simple econometric models.
'''

import os
import numpy as np
import pandas as pd
from osgeo import gdal
from tqdm.auto import tqdm

# Config
gdal.UseExceptions()
os.environ['USE_PYGEOS'] = '0'

# Directories
main_dir = os.path.join('C:\\', 'Users', 'jqnmu', 'OneDrive', 'World_Bank_DRM') + os.sep
data_dir = os.path.join(main_dir, 'Datasets') + os.sep
GHSL_countries_dir = os.path.join(data_dir, 'GHSL_2023', 'Countries') + os.sep

# Parameters
fyear = 2050
RPs = [10, 100] # RP = 10 
Scenarios = ['2020', f'{fyear}-SSP1_2.6', f'{fyear}-SSP2_4.5', f'{fyear}-SSP3_7.0', f'{fyear}-SSP5_8.5']

# Create iso3_list
iso3_list = pd.read_csv(data_dir + 'ISO3_list.csv')
iso3_list.set_index('ISO3', inplace = True)
iso3_list = iso3_list[iso3_list['sub-region'] == 'Sub-Saharan Africa'] # Filter SSA only

# Load linear regression results - coefficients to convert from BU growth to BU exposure growth
linreg_res = pd.read_csv(f'{main_dir}Future_Flood_Risk/Results/linreg_BUgr_BUexpgr.csv')
linreg_res.set_index('RP', inplace = True)
print(f"✓ Loaded regression coefficients for RPs: {list(linreg_res.index)}")
   
def Create_BoolArray_BU(data_dir, shp_wID_tif, year, ISO3):
    """
    Create a boolean array to filter pixels where both:
    1. Country shapefile is valid (shp != 0)
    2. Built-up area exists (BU > 0)
    
    This ensures we only analyze pixels within the country that have built-up area.
    """
    GHSL_country_dir = f'{data_dir}GHSL_2023/Countries/{ISO3}/'
    
    # Load country shapefile raster and create boolean mask
    raster = gdal.Open(shp_wID_tif, gdal.GA_Update)
    shp_bool = raster.GetRasterBand(1).ReadAsArray().flatten().astype(bool)
    
    # Load built-up area raster and create boolean mask for pixels with BU > 0
    raster = gdal.Open(f'{GHSL_country_dir}GHSL_BU_{ISO3}_{year}.tif', gdal.GA_Update)
    BU_bool = raster.GetRasterBand(1).ReadAsArray().flatten()
    
    # Combine both conditions: valid country pixel AND has built-up area
    bool_arr = shp_bool & (BU_bool > 0)
    return bool_arr

def CountryFile_simple(main_dir, country, country_dir, ISO3):
    """
    Load and process UN World Population Prospects (WPP) data for a country.
    Combines projections (2022-2050) with historical data (1980-2020).
    
    Returns DataFrame with population in millions for different projection scenarios:
    - Median, Lower 95, Lower 80, Upper 80, Upper 95 (uncertainty bands)
    """
    df = pd.DataFrame()
    
    # Load historical population data from processed file
    dfpop = pd.read_csv(country_dir + f'{ISO3}_Total_POP.csv', index_col = 'Year')
    
    # Process each projection scenario (median + uncertainty bands)
    for proj in ['Median', 'Lower 95', 'Lower 80', 'Upper 80', 'Upper 95']:
        # Load UN WPP projections from Excel sheet
        wpp = pd.read_excel(main_dir + 'Datasets/Urban/UN_PPP2022_Output_PopTot.xlsx', sheet_name = proj, skiprows = 16, header = 0)
        wpp.set_index('Region, subregion, country or area *', inplace = True)
        
        # Extract future years (2022-2050) - convert from thousands to millions
        for year in [2022, 2025, 2030, 2035, 2040, 2045, 2050]:
            df.at['wpp_' + proj.lower().replace(' ', ''), year] = wpp.at[country, year]/1000
        
        # Extract historical years (1980-2020) - convert to millions
        for year in range(1980, 2025, 5):
            df.at['wpp_' + proj.lower().replace(' ', ''), year] = dfpop.at[year, 'Total_POP']/1000000
    
    return df

#%%

# Loop through all Sub-Saharan African countries
for ISO3 in tqdm(iso3_list.index, desc="Processing countries"):
    country = iso3_list.at[ISO3, 'Country']
    print(f"Processing: {country} ({ISO3})")    
    try:
        # Set up directory paths for this country
        GHSL_country_dir = f'{data_dir}GHSL_2023/Countries/{ISO3}/'
        FTM_dir = f'{data_dir}Fathom_3/data/{ISO3}/binaries_data/'
        country_dir = f'{main_dir}Future_Flood_Risk/Model_2024/{ISO3}/'
        shp_wID_tif = f'{data_dir}GADM4.1/{ISO3}/gadm41_{ISO3}_0_wID.tif'

        # Load UN DESA urban population projection data
        df_exp = CountryFile_simple(main_dir, country, country_dir, ISO3)

        # STEP 1: Calculate Built-up per capita for 2020 (baseline)
        dfbu = pd.read_csv(country_dir + f'{ISO3}_results.csv', index_col = 'Year')
        dfpop = pd.read_csv(country_dir + f'{ISO3}_Total_POP.csv', index_col = 'Year')
        dfbu['Total_POP'] = dfpop['Total_POP']  # Merge population data
        dfbu['BUperCAP'] = dfbu['Total_BU'] * 1e6 / dfbu['Total_POP']  # m² per person
        bupercap1 = dfbu.at[2020, 'BUperCAP']  # Baseline built-up per capita in 2020


        # Calculate relative exposure (proportion of total built-up exposed to flooding)
        for RP in RPs:
            dfbu[f'Total_BU_exposed_{RP}_rel'] = dfbu[f'Total_BU_exposed_{RP}']/dfbu['Total_BU']

        # STEP 2: Project future built-up using CONSTANT per capita assumption
        # Scenario 1 (s1): Assumes built-up per capita stays constant at 2020 level
        print(f"  → Projecting future built-up (constant per capita scenario)...")
        for proj in ['median', 'lower80', 'lower95', 'upper80', 'upper95']:
            # Future (2050): Population × constant BU per capita
            df_exp.at[f'bup_s1_{proj}', 2050] = df_exp.at[f'wpp_{proj}', 2050] * bupercap1
            # Baseline (2020): Population × constant BU per capita
            df_exp.at[f'bup_s1_{proj}', 2020] = df_exp.at[f'wpp_{proj}', 2020] * bupercap1
        print(f"  ✓ Built-up projections calculated for all scenarios")
        
        # STEP 3: Load spatial rasters and create boolean filter
        print(f"  → Loading spatial rasters...")
        # Create mask: only pixels within country boundary AND with built-up area
        bool_arr = Create_BoolArray_BU(data_dir, shp_wID_tif, 2020, ISO3)
        print(f"  ✓ Boolean filter created: {bool_arr.sum():,} valid pixels")

        # Load 2020 built-up area raster and filter to valid pixels
        raster = gdal.Open(f'{GHSL_countries_dir}/{ISO3}/GHSL_BU_{ISO3}_2020.tif', gdal.GA_Update)
        BU_2020 = raster.GetRasterBand(1).ReadAsArray().flatten()[bool_arr].astype('float32')
        print(f"  ✓ Built-up 2020 raster loaded: {BU_2020.sum()/1e6:.2f} km²")

        # STEP 4: Process flood exposure by return period and climate scenario
        print(f"  → Processing flood exposure scenarios...")
        dff = pd.DataFrame()  # Store all results for this country
        dff.at[country, 'BU_2020'] = BU_2020.sum()/1e6  # Total built-up in 2020 (km²)
        
        for RP in tqdm(RPs, desc=f"  Return periods", leave=False):
            print(f"    → Processing RP-{RP} year flood...")
            
            # Load flood exposure for each climate scenario
            for SSP in Scenarios:
                # Load Fathom3 flood binary: 1 = flooded, 0 = not flooded
                raster = gdal.Open(FTM_dir + f'1in{RP}-COMBIN-DEFENDED-{SSP}.tif', gdal.GA_Update)
                fath = raster.GetRasterBand(1).ReadAsArray().flatten()[bool_arr]
                
                # Calculate exposed built-up: sum of BU where flood occurs
                dff.at[country, f'{SSP}_{RP}'] = np.sum(BU_2020 * fath)/1e6  # km²
            
            print(f"    ✓ RP-{RP}: Loaded {len(Scenarios)} scenarios")
            
            # STEP 5: Project 2050 flood exposure with urbanization growth
            print(f"    → Projecting 2050 exposure with urbanization...")
            for perc in ['lower95', 'lower80', 'median', 'upper80', 'upper95']:
                # Use regression coefficients to scale exposure by built-up growth
                coef = linreg_res.at[RP, 'constant']  # Intercept
                beta1 = linreg_res.at[RP, 'beta1']    # Slope coefficient
                
                # Formula: Future_Exposure = coef + beta1 × (Current_Exposure × BU_growth_ratio)
                # BU_growth_ratio = (BU_2050 / BU_2020) under constant per capita assumption
                dff.at[country, f'bupsc1_{perc}_{RP}'] = coef + beta1 * (
                    dff.at[country, f'2020_{RP}'] * 
                    df_exp.at[f'bup_s1_{perc}', 2050] / 
                    df_exp.at[f'bup_s1_{perc}', 2020]
                )
            print(f"    ✓ RP-{RP}: Projected 5 urbanization scenarios")
        
        # Save results to CSV
        output_file = country_dir + f'{ISO3}_BUexp_projected.csv'
        dff.to_csv(output_file)
        print(f"\n  ✅ SUCCESS: Results saved to {ISO3}_BUexp_projected.csv")
    
    except Exception as e:
        print(f"\n  ❌ ERROR processing {country} ({ISO3}): {str(e)}")
        print(f"  Skipping to next country...\n")
        continue

#%%
# STEP 6: Combine all country files into a single consolidated dataframe
print("Combining all country results into consolidated file...")

combined_df = pd.DataFrame()  # Initialize empty dataframe to store all results

for ISO3 in tqdm(iso3_list.index, desc="Reading country files"):
    country = iso3_list.at[ISO3, 'Country']
    country_file = f'{main_dir}Future_Flood_Risk/Model_2024/{ISO3}/{ISO3}_BUexp_projected.csv'
    
    try:
        # Read individual country file
        df_temp = pd.read_csv(country_file, index_col=0)
        df_temp.insert(0, 'ISO3', ISO3)  # Add ISO3 column as first column
        
        # Append to combined dataframe
        combined_df = pd.concat([combined_df, df_temp], axis=0)
        print(f"  ✓ Added {country} ({ISO3})")
        
    except FileNotFoundError:
        print(f"  ⚠ File not found for {country} ({ISO3}), skipping...")
        continue
    except Exception as e:
        print(f"  ❌ Error reading {country} ({ISO3}): {str(e)}")
        continue

# Save combined dataframe in two directories
output_file = f'{main_dir}Future_Flood_Risk/Results/ALL_SSA_BUexp_projected_consolidated.csv'
combined_df.to_csv(output_file)
output_file = os.path.join('data', 'processed', 'ALL_SSA_BUexp_projected_consolidated.csv')
combined_df.to_csv(output_file)

print(f"Total countries in combined file: {len(combined_df)}")
print(f"Total columns: {len(combined_df.columns)}")
print(f"Output saved to: ALL_SSA_BUexp_projected_consolidated.csv")
print(f"{'='*80}\n")
    