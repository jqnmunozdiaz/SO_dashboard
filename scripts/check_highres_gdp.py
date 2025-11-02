import rasterio
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Check the high-resolution raster
raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 'rast_gdpTot_1990_2020_30arcsec.tif')

print("Opening high-resolution raster...")
raster = rasterio.open(raster_path)
print(f"Raster info:")
print(f"  Bands: {raster.count}")
print(f"  Shape: {raster.shape}")
print(f"  Resolution: {raster.res}")
print(f"  NoData value: {raster.nodata}")
print(f"  Data type: {raster.dtypes[0]}")
print(f"  CRS: {raster.crs}")

# Calculate which band would be 2020 (last available year)
start_year = 1990
end_year = 2020
expected_bands = end_year - start_year + 1
print(f"\nExpected bands for {start_year}-{end_year}: {expected_bands}")
print(f"Actual bands: {raster.count}")

if raster.count == expected_bands:
    print(f"\n✓ Band structure matches expected range")
    print(f"  Year 2020 should be in band {expected_bands}")
else:
    print(f"\n⚠ Band count mismatch!")

raster.close()
