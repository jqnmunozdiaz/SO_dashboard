"""
# https://zenodo.org/records/16741980

"""

import os
import sys
import rasterio
import geopandas as gpd
import numpy as np
from shapely.geometry import mapping
from rasterstats import zonal_stats

# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

def load_gdp_data():
    """Load GDP raster data"""
    # Path to raster file - using high-resolution 30 arcsec raster
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'rast_gdpTot_1990_2020_30arcsec.tif')
    raster = rasterio.open(raster_path)
    return raster

def load_population_data():
    """Load population raster data"""
    # Path to raster file - 1km resolution population data for 2020
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'global_pop_2020_CN_1km_R2025A_UA_v1.tif')
    
    raster = rasterio.open(raster_path)
    return raster

def load_cities(iso3):
    """
    Load cities by population for a country
    
    Args:
        iso3: ISO3 country code
        
    Returns:
        GeoDataFrame with cities
    """
    
    cities_path = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Datasets\Africapolis\Africapolis_2023\africapolis2023.gpkg'
    cities = gpd.read_file(cities_path) 

    # Filter cities within country boundary
    cities = cities[cities['ISO3'] == iso3]
    cities = cities.sort_values('Pop2020', ascending=False).head(10)
    return cities

ISO3 = 'BFA'
cities = load_cities(ISO3)
gdp_raster = load_gdp_data()
pop_raster = load_population_data()

def _zonal_stats_for_geometry(raster, geom, band=None, all_touched=True):
    """Compute zonal sum using rasterstats.zonal_stats.

    Args:
        raster: opened rasterio dataset
        geom: shapely geometry
        band: integer band index (1-based) or None for single-band
    Returns:
        dict with key 'sum'
    """
    try:
        # zonal_stats returns a list of dicts when given a single geometry
        zs = zonal_stats(mapping(geom), raster.name, stats=['sum'], band=band, all_touched=all_touched, nodata=raster.nodata)
        if isinstance(zs, list) and len(zs) > 0:
            s = zs[0].get('sum')
        elif isinstance(zs, dict):
            s = zs.get('sum')
        else:
            s = None

        return {'sum': float(s) if s is not None else np.nan}
    except Exception:
        return {'sum': np.nan}


def append_zonal_stats_to_cities(cities_gdf, gdp_raster, pop_raster, gdp_band=7):
    """Compute zonal stats for GDP (band) and population and append columns to cities_gdf.

    Adds columns: `gdp_2020_sum`, `pop_2020_sum`
    """
    # Prepare empty columns
    cities_gdf['gdp_2020_sum'] = np.nan
    cities_gdf['pop_2020_sum'] = np.nan

    for idx, row in cities_gdf.iterrows():
        geom = row.geometry

        gdp_stats = _zonal_stats_for_geometry(gdp_raster, geom, band=gdp_band)
        pop_stats = _zonal_stats_for_geometry(pop_raster, geom, band=1)

        cities_gdf.at[idx, 'gdp_2020_sum'] = gdp_stats.get('sum', np.nan)
        cities_gdf.at[idx, 'pop_2020_sum'] = pop_stats.get('sum', np.nan)

    return cities_gdf

# Compute zonal statistics and append to cities
cities = append_zonal_stats_to_cities(cities, gdp_raster, pop_raster, gdp_band=7)

cities = cities[['agglosID','agglosName', 'ISO3', 'Pop2010', 'Pop2015', 'Pop2020', 'gdp_2020_sum', 'pop_2020_sum']]
# Export to CSV
output_path = os.path.join(project_root, 'data', 'processed', f'{ISO3}_cities_gdp_pop.csv')
cities.to_csv(output_path, index=False)
print(f"Exported data to {output_path}")
   
# Close rasters
gdp_raster.close()
pop_raster.close()
