# Download Data Feature - Implementation Guide

## Overview

The dashboard now includes a modular **"Download Data"** button system that allows users to download the underlying CSV data for any chart. This feature is designed to be:

- **Reusable**: Single implementation pattern works across all charts
- **Flexible**: Supports single CSV or multiple CSV files (as ZIP)
- **Filterable**: Downloads respect user selections (country, benchmarks, filters)
- **User-friendly**: Clear labeling, tooltips, and consistent styling

## User Experience

### How It Works for Users

1. Navigate to any chart with a download button
2. Select country and apply any filters/benchmarks
3. Click the **"Download Data"** button below the chart
4. Receive a CSV file (or ZIP with multiple CSVs) containing:
   - Filtered data based on selections
   - Clear filename indicating country and chart type
   - Optional metadata sheet with indicator codes and sources

### Download Button Features

- **Icon**: Download icon (Font Awesome) for clear affordance
- **Tooltip**: Hover to see which data sources will be downloaded
- **Positioning**: Consistently placed in `indicator-note-container` after footnotes
- **Styling**: World Bank blue theme matching the dashboard design
- **Responsiveness**: Works on all screen sizes

## Developer Implementation Guide

### Quick Start - Adding Download to a Chart

#### Step 1: Import Download Helpers

Add to your callback file:

```python
from ...utils.download_helpers import (
    prepare_csv_download,           # For single CSV
    prepare_multi_csv_download,     # For multiple CSVs as ZIP
    get_filtered_data,              # For filtering by selections
    add_metadata_sheet              # Optional: add metadata
)
```

#### Step 2: Create Download Callback

**Single CSV Example:**

```python
@app.callback(
    Output('your-chart-download', 'data'),
    [Input('your-chart-download-button', 'n_clicks'),
     Input('main-country-filter', 'value'),
     Input('your-benchmark-selector', 'value')],
    prevent_initial_call=True
)
def download_your_data(n_clicks, selected_country, benchmarks):
    if n_clicks is None or n_clicks == 0:
        return None
    
    try:
        # Load data (same as chart callback)
        data = load_your_data()
        
        # Filter for selections
        filtered_data = get_filtered_data(
            data, 
            selected_country,
            benchmark_regions=benchmarks
        )
        
        # Create filename
        countries_dict = load_subsaharan_countries_and_regions_dict()
        country_name = countries_dict.get(selected_country, 'all')
        filename = f"data_{selected_country}_{country_name.replace(' ', '_')}"
        
        return prepare_csv_download(filtered_data, filename)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

**Multiple CSV (ZIP) Example:**

```python
@app.callback(
    Output('your-chart-download', 'data'),
    [Input('your-chart-download-button', 'n_clicks'),
     Input('main-country-filter', 'value')],
    prevent_initial_call=True
)
def download_your_data(n_clicks, selected_country):
    if n_clicks is None or n_clicks == 0:
        return None
    
    try:
        # Load multiple datasets
        dataset1 = load_first_data()
        dataset2 = load_second_data()
        
        # Filter
        data1_filtered = get_filtered_data(dataset1, selected_country)
        data2_filtered = get_filtered_data(dataset2, selected_country)
        
        # Create dict (keys become filenames)
        dataframes = {
            'dataset1_name': data1_filtered,
            'dataset2_name': data2_filtered
        }
        
        # Optional: Add metadata
        add_metadata_sheet(
            dataframes,
            indicator_code="INDICATOR_CODE",
            source="World Bank WDI",
            note="Additional context"
        )
        
        # Create filename and return ZIP
        filename = f"combined_data_{selected_country}"
        return prepare_multi_csv_download(dataframes, filename)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

#### Step 3: Add Button to Layout

In your orchestrator (e.g., `urbanization_callbacks.py`):

```python
# Import
from ..utils.ui_helpers import create_download_button

# In render callback, add after indicator note:
html.Div([
    html.P([html.B("Data Source: "), "...", html.Br(), 
            html.B("Note:"), "..."], 
           className="indicator-note"),
    create_download_button(
        'your-chart-download',  # ID matches callback Output
        ['Data Source 1', 'Data Source 2']  # Tooltip sources
    )
], className="indicator-note-container")
```

## Utility Functions Reference

### `prepare_csv_download(df, filename)`

Downloads a single DataFrame as CSV.

**Parameters:**
- `df` (pd.DataFrame): Data to download
- `filename` (str): Filename without extension

**Returns:** Download data for `dcc.Download`

**Example:**
```python
return prepare_csv_download(data, "urban_population_ETH_Ethiopia")
# Downloads: urban_population_ETH_Ethiopia.csv
```

### `prepare_multi_csv_download(dataframes_dict, zip_filename)`

Downloads multiple DataFrames as a ZIP file.

**Parameters:**
- `dataframes_dict` (dict): `{filename: DataFrame}` mapping
- `zip_filename` (str): ZIP filename without extension

**Returns:** Download data for `dcc.Download`

**Example:**
```python
dataframes = {
    'gdp_data': gdp_df,
    'urbanization_data': urb_df
}
return prepare_multi_csv_download(dataframes, "gdp_urbanization_ETH")
# Downloads: gdp_urbanization_ETH.zip
#   Contains: gdp_data.csv, urbanization_data.csv
```

### `get_filtered_data(df, selected_country, benchmark_countries=None, benchmark_regions=None)`

Filters DataFrame for selected countries and benchmarks.

**Parameters:**
- `df` (pd.DataFrame): Source data with 'Country Code' column
- `selected_country` (str): Main country ISO code
- `benchmark_countries` (list): Country benchmark ISO codes
- `benchmark_regions` (list): Regional benchmark codes (SSA, AFE, etc.)

**Returns:** Filtered DataFrame

**Example:**
```python
filtered = get_filtered_data(
    data, 
    'ETH',  # Main country
    benchmark_countries=['KEN', 'TZA'],  # Country comparisons
    benchmark_regions=['SSA', 'AFE']  # Regional comparisons
)
```

### `add_metadata_sheet(dataframes_dict, indicator_code=None, source=None, note=None)`

Adds metadata CSV to download package.

**Parameters:**
- `dataframes_dict` (dict): Dictionary to add metadata to
- `indicator_code` (str): WDI or other indicator code
- `source` (str): Data source description
- `note` (str): Additional context

**Returns:** Updated dictionary with 'metadata' sheet

**Example:**
```python
dataframes = {'data': df}
add_metadata_sheet(
    dataframes,
    indicator_code="SP.URB.TOTL.IN.ZS",
    source="World Bank WDI",
    note="Urban population as % of total"
)
# Now includes metadata.csv in ZIP
```

### `create_download_button(download_id)`

Creates styled download button UI component.

**Parameters:**
- `download_id` (str): Unique ID for download (used in callback)

**Returns:** html.Div with button and dcc.Download

**Example:**
```python
create_download_button('urban-pop-download')
```

## Implemented Examples

### Single CSV Downloads

**Urban Population Projections**
- File: `src/callbacks/urbanization/Urban_Population_Projections_callbacks.py`
- Data: UN DESA urban projections
- Callback: `download_urban_population_projections_data`
- Features: Filters by country, includes all projection indicators

### Multiple CSV Downloads (ZIP)

**GDP vs Urbanization**
- File: `src/callbacks/urbanization/GDP_vs_Urbanization_callbacks.py`
- Data: Two WDI indicators (GDP per capita + Urbanization rate)
- Callback: `download_gdp_vs_urbanization_data`
- Features: 
  - Downloads 2 CSV files in ZIP
  - Filters by country, country benchmarks, and global benchmarks
  - Includes metadata sheet with indicator codes

## File Structure

```
src/
├── utils/
│   ├── download_helpers.py         # Core download utilities
│   └── ui_helpers.py                # UI component (create_download_button)
├── callbacks/
│   ├── templates/
│   │   └── download_callback_template.py  # Implementation guide
│   ├── urbanization/
│   │   ├── Urban_Population_Projections_callbacks.py  # Example 1
│   │   └── GDP_vs_Urbanization_callbacks.py           # Example 2
│   └── urbanization_callbacks.py   # Layout orchestrator
└── ...

assets/
└── css/
    └── custom.css                   # Download button styles

app.py                               # Font Awesome CDN added
```

## Styling

The download button uses consistent World Bank theming:

```css
.download-data-button {
    background-color: #295e84;  /* WB blue */
    color: white;
    font-size: 0.875rem;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    /* Hover animations */
}
```

Positioned in:
```css
.download-button-container {
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
}
```

## Best Practices

### Naming Conventions

**Callback IDs:**
- Download output: `{chart-name}-download`
- Button trigger: `{chart-name}-download-button`

**Filenames:**
- Single country: `{data_type}_{ISO}_{Country_Name}`
- All countries: `{data_type}_all_countries`
- Multi-source: `{combined_name}_{ISO}_{Country_Name}`

### Error Handling

Always include try-except in download callbacks:

```python
try:
    # Download logic
    return prepare_csv_download(data, filename)
except Exception as e:
    print(f"Error preparing download: {str(e)}")
    return None  # Prevents callback errors
```

### Performance

- Use `prevent_initial_call=True` to avoid unnecessary processing
- Check `n_clicks` to ensure user actually clicked button
- Filter data before preparing download (reduces file size)

### User Experience

- Add descriptive tooltips with data sources
- Use clear, consistent filenames
- Include metadata for multi-file downloads
- Test downloads on different browsers

## Testing Checklist

When implementing a new download feature:

- [ ] Callback registered in appropriate orchestrator
- [ ] Button added to layout with correct ID
- [ ] Download works with no selections (if applicable)
- [ ] Download respects country filter
- [ ] Download respects benchmark selections
- [ ] Filename is descriptive and valid
- [ ] CSV/ZIP file opens correctly
- [ ] Data matches what's shown in chart
- [ ] No console errors when clicking button
- [ ] Tooltip shows correct data sources

## Future Enhancements

Potential improvements:

1. **Format Options**: Add Excel (.xlsx) export option
2. **Chart Images**: Include PNG of chart in ZIP download
3. **Date Range**: Filter by date range in downloads
4. **Bulk Downloads**: Download all charts for a country at once
5. **API Integration**: Direct API access for programmatic downloads
6. **Caching**: Cache prepared downloads for faster subsequent requests

## Support

For questions or issues:
- See working examples in `src/callbacks/urbanization/`
- Refer to template: `src/callbacks/templates/download_callback_template.py`
- Check utility docs in `src/utils/download_helpers.py`
