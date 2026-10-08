"""
Fill the missing Cabo Verde (CPV) 1-in-100 flood exposure in the national time series
(country_ftm3_current_ghsl2023_built_s.csv / _pop.csv, 1975-2020).

The original extraction left CPV 1-in-100 blank. The data producer supplied corrected Fathom3
FLUVIAL_PLUVIAL_DEFENDED 2020 flood masks (data/raw/CPV). Exposure is computed as the sum of the
GHSL layer (built-up m2 / population) over flooded pixels, for each GHSL year. The 1-in-5 and
1-in-10 values computed the same way reproduce the existing CSV values (<0.1%), which validates
the method; only the blank 1-in-100 rows (and the AFE/AFW/SSA aggregates that include CPV) are
overwritten.

Run from the project root: python scripts/fix_cpv_flood_exposure_timeseries.py
"""

import os
import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds

GHSL_DIR = r'G:\My Drive\World_Bank_DRM\Datasets\GHSL_2023\Countries\CPV'
FLOOD_TIF = 'data/raw/CPV/CPV_ftm3_FLUVIAL_PLUVIAL_DEFENDED_2020_{rp}.tif'
FLOOD_TYPE = 'FLUVIAL_PLUVIAL_DEFENDED'
YEARS = range(1975, 2021, 5)
TOLERANCE = 0.01  # max relative deviation allowed on 1in5/1in10 vs existing data

# kind -> (GHSL prefix, value column, total column, unit divisor)
KINDS = {
    'built_s': ('BU', 'ftm3_ghsl_total_built_s_km2', 'ghsl_total_built_s_km2', 1e6),  # m2 -> km2
    'pop': ('POP', 'ftm3_ghsl_total_pop_#', 'ghsl_total_pop_#', 1.0),
}

wb = pd.read_csv('data/Definitions/WB_Classification.csv')
regions = {
    'AFE': wb[wb['Subregion Code'] == 'AFE']['ISO3'].tolist(),
    'AFW': wb[wb['Subregion Code'] == 'AFW']['ISO3'].tolist(),
    'SSA': wb[wb['Region Code'] == 'SSA']['ISO3'].tolist(),
}

masks = {}
for rp in ('1in5', '1in10', '1in100'):
    with rasterio.open(FLOOD_TIF.format(rp=rp)) as src:
        masks[rp] = src.read(1) > 0
        bounds = src.bounds

for kind, (prefix, val_col, tot_col, div) in KINDS.items():
    path = f'data/processed/flood/country_ftm3_current_ghsl2023_{kind}.csv'
    # Read as text so untouched cells are written back byte-for-byte
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    num = lambda col: pd.to_numeric(df[col], errors='coerce')
    is_cpv = (df['ISO_A3'] == 'CPV') & (df['flood_type'] == FLOOD_TYPE)

    # Exposure per year / return period from the rasters (flood grid is aligned to the GHSL grid)
    for year in YEARS:
        with rasterio.open(os.path.join(GHSL_DIR, f'GHSL_{prefix}_CPV_{year}.tif')) as g:
            win = from_bounds(*bounds, transform=g.transform).round_offsets().round_lengths()
            layer = g.read(1, window=win)
        for rp, mask in masks.items():
            assert layer.shape == mask.shape, (layer.shape, mask.shape)
            value = float(layer[mask].sum()) / div
            row = is_cpv & (df['ghsl_year'] == str(year)) & (df['return_period'] == rp)
            assert row.sum() == 1, (kind, year, rp)
            if rp != '1in100':
                existing = float(df.loc[row, val_col].iloc[0])
                dev = abs(value / existing - 1)
                assert dev < TOLERANCE, f'{kind} {year} {rp}: computed {value} vs existing {existing}'
                continue
            df.loc[row, val_col] = repr(value)
            df.loc[row, 'relative_exposure_pct'] = repr(value / float(df.loc[row, tot_col].iloc[0]) * 100)

    # Regional aggregates = sum over member countries (same as aggregate_regional_flood_data.py)
    for region, members in regions.items():
        if 'CPV' not in members:
            continue
        for year in YEARS:
            sel = (df['ghsl_year'] == str(year)) & (df['flood_type'] == FLOOD_TYPE) & (df['return_period'] == '1in100')
            total = num(val_col)[sel & df['ISO_A3'].isin(members)].sum()
            row = sel & (df['ISO_A3'] == region)
            if row.sum() == 1:
                df.loc[row, val_col] = repr(float(total))
                df.loc[row, 'relative_exposure_pct'] = repr(float(total) / float(df.loc[row, tot_col].iloc[0]) * 100)

    df.to_csv(path, index=False)  # lineterminator defaults to os.linesep (CRLF), as in the source files
    print(f'Updated {path}')
    print(df[is_cpv & (df['return_period'] == '1in100')][['ghsl_year', val_col, 'relative_exposure_pct']].to_string(index=False))
