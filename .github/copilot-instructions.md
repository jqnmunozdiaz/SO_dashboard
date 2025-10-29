# Sub-Saharan Africa DRM Dashboard - AI Coding Instructions

## Architecture Overview

This is a **Dash-based dashboard** for analyzing disaster risk management (DRM) data across Sub-Saharan Africa. The application follows a **strictly modular architecture** with clear separation of concerns to support easy addition of new visualizations and data sources.

### Core Architecture Layers

- **Entry Point**: `app.py` - initializes Dash app, registers callbacks, handles deployment config
- **Layout System**: `src/layouts/world_bank_layout.py` - creates World Bank-styled UI components with responsive design  
- **Callback Controllers**: `src/callbacks/` - organized by feature area with nested structure for complex visualizations
- **Data Layer**: `src/utils/` - centralized data loading, country utilities, chart helpers, and benchmark configuration
- **Configuration**: `config/settings.py` - comprehensive dashboard settings, styling, and environment configuration (NEVER hardcode values)
- **Definitions**: `data/Definitions/` - centralized configuration files for countries, disaster types, and indicators

### Modularity Principles ⚠️ CRITICAL

1. **No Hardcoding**: All configuration values (years, colors, regions, indicators) MUST be in `config/settings.py`, `data/Definitions/`, or `src/utils/*_config.py`
2. **Centralized Utilities**: Always use shared utilities in `src/utils/` - never duplicate logic across callbacks
3. **Configuration-Driven**: New visualizations should require minimal code changes - add config, not code
4. **Reusable Components**: UI components in `src/utils/ui_helpers.py` should be parametric and reusable
5. **Single Source of Truth**: Each data element, color scheme, or business rule has exactly one definition location

## Current Dashboard Structure

### Main Tabs
1. **Historical Disasters** - EM-DAT disaster analysis with four subtabs:
   - Overview of Disasters - disaster type distribution charts
   - Disasters by Year - temporal trend analysis
   - Total Affected Population - population impact analysis
   - Total Deaths - mortality impact analysis

2. **Historical Urbanization** - WDI urbanization indicators with seven subtabs:
   - Urban Population Projections - UN DESA urban population forecasts with uncertainty bands
   - Urbanization Rate - urban population growth projections with regional benchmarks
   - Urban Population Living in Slums - slums population trends with regional benchmarks
   - Access to Electricity, Urban - electricity access trends with regional benchmarks
   - GDP vs Urbanization - scatterplot with country and global benchmarks
   - Cities Distribution - city size distribution analysis
   - Cities Evolution - city growth over time

3. **Exposure to Flood Hazard** - Fathom3 flood risk analysis with five subtabs:
   - National Flood Exposure - total built-up area exposed to flooding (dynamic exposure/measurement types)
   - Cities Flood Exposure - flood exposure for major cities over time

4. **Projections of Flood Risk** - Future flood and climate scenarios with two subtabs:
   - Changes in Extreme Precipitation - precipitation return period projections under climate scenarios
   - Urbanization vs Climate Change - comparison of demographic vs climate-driven flood exposure changes

## Key Patterns & Conventions

### Data Loading Pattern (REQUIRED)
All data access MUST go through centralized utilities in `src/utils/`:

```python
# Country data - ALWAYS use centralized utilities
from src.utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_dict, load_subsaharan_countries_and_regions_dict

# Disaster data - use the standardized loader
from src.utils.data_loader import load_emdat_data

# WDI data - urbanization indicators
from src.utils.data_loader import load_wdi_data, load_urbanization_indicators_dict, load_urbanization_indicators_notes_dict

# UN DESA urban projections
from src.utils.data_loader import load_undesa_urban_projections

# Regional benchmarks - Sub-Saharan Africa specific (SSA, AFE, AFW)
from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names, get_benchmark_options

# Global benchmarks - All world regions (SSA, AFE, AFW, EAP, ECA, LCR, MNA, SAR)
from src.utils.GLOBAL_BENCHMARK_CONFIG import (
    get_global_benchmark_colors, 
    get_global_benchmark_names, 
    get_global_benchmark_options,
    get_global_benchmark_dropdown_options,
    get_all_global_benchmark_codes
)

# UI helpers - reusable components
from src.utils.ui_helpers import (
    create_benchmark_selectors, 
    create_download_trigger_button,     # Creates visible button to trigger download
    create_download_component,          # Creates hidden dcc.Download component
    create_methodological_note_button,  # Creates link to methodological note doc
    create_city_platform_button         # Creates city-level platform link
)

# Download helpers - data export functionality
from src.utils.download_helpers import prepare_csv_download, prepare_multi_csv_download

# Error handling - use shared chart utilities
from src.utils.component_helpers import create_error_chart
```

### Download Data Feature

All charts have "Download Data" and "Methodological Note" buttons allowing users to export the underlying data as CSV files. Downloads provide the complete raw dataset without filtering. The feature uses a two-component pattern:

1. **Hidden `dcc.Download` Components** (in `src/layouts/world_bank_layout.py`)
   - Rendered in a hidden div at the end of main-content
   - One per download ID: `dcc.Download(id='chart-name-download')`
   - These persist across page navigation

2. **Visible Trigger Buttons** (in individual callback orchestrators)
   - `create_download_trigger_button('chart-name-download')` - renders as blue World Bank styled button with download icon
   - `create_methodological_note_button()` - renders as button linking to external documentation
   - Both placed in `indicator-note-container` with `buttons-container` class

3. **Download Callbacks** (in individual chart callback files)
   - Watch for button clicks: `@app.callback(Output('chart-name-download', 'data'), ...)`
   - Load raw data, prepare CSV format, return via `prepare_csv_download(data, filename)`

#### Implementation Example

In **callback orchestrator** (`src/callbacks/disaster_callbacks.py`):
```python
# In render function for each subtab
html.Div([
    html.P([html.B("Data Source: "), "...", html.Br(), html.B("Note:"), "..."], className="indicator-note"),
    html.Div([
        create_download_trigger_button('disaster-frequency-download'),
        create_methodological_note_button()
    ], className="buttons-container")
], className="indicator-note-container")
```

In **layout file** (`src/layouts/world_bank_layout.py`):
```python
# In hidden div at end of main-content
html.Div([
    create_download_component("disaster-frequency-download"),
    create_download_component("disaster-timeline-download"),
    # ... more downloads ...
], style={"display": "none"})
```

In **chart callback file** (`src/callbacks/disaster/Frequency_by_Type_callbacks.py`):
```python
@app.callback(
    Output('disaster-frequency-download', 'data'),
    [Input('disaster-frequency-download-button', 'n_clicks'),
     Input('main-country-filter', 'value')],
    prevent_initial_call=True
)
def download_disaster_frequency_data(n_clicks, selected_country):
    if n_clicks is None or n_clicks == 0:
        return None
    try:
        data = load_emdat_data()
        if selected_country:
            data = data[data['ISO'] == selected_country]
        countries_dict = load_subsaharan_countries_and_regions_dict()
        country_name = countries_dict.get(selected_country, 'all')
        filename = f"disaster_frequency_{selected_country}_{country_name.replace(' ', '_')}"
        return prepare_csv_download(data, filename)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
```

**Key Patterns:**
- Download IDs follow format: `{chart-name}-download`
- Trigger button IDs automatically append `-button`: `{chart-name}-download-button`
- All charts should have both Download and Methodological Note buttons
- Hidden components centralized in layout; visible buttons scattered logically near charts
- Use `prepare_csv_download()` for single files, `prepare_multi_csv_download()` for multiple CSVs

### Benchmark System Architecture

The dashboard supports two levels of regional benchmarks:

1. **Regional Benchmarks** (`benchmark_config.py`): Sub-Saharan Africa specific regions
   - SSA (Sub-Saharan Africa) - Red
   - AFE (Eastern and Southern Africa) - Orange
   - AFW (Western and Central Africa) - Green
   - Used for: checkboxes in urbanization charts

2. **Global Benchmarks** (`GLOBAL_BENCHMARK_CONFIG.py`): All world regions  
   - Includes SSA, AFE, AFW plus:
   - EAP (East Asia & Pacific) - Blue
   - ECA (Europe & Central Asia) - Purple
   - LCR (Latin America & Caribbean) - Dark Orange
   - MNA (Middle East & North Africa) - Teal
   - SAR (South Asia) - Dark Red
   - Used for: dropdown in GDP vs Urbanization chart

### Creating Benchmark Selectors (UI Pattern)

```python
# In urbanization_callbacks.py or disaster_callbacks.py orchestrator

from src.utils.ui_helpers import create_benchmark_selectors

# Example 1: Regional checkboxes + Country dropdown
*create_benchmark_selectors(
    regional_id='slums-benchmark-selector',
    country_id='slums-country-benchmark-selector',
    include_regional=True,
    include_country=True
)

# Example 2: Global dropdown + Country dropdown (GDP vs Urbanization pattern)
*create_benchmark_selectors(
    regional_id='gdp-vs-urbanization-benchmark-selector',
    country_id='gdp-vs-urbanization-country-benchmark-selector',
    global_id='gdp-vs-urbanization-global-benchmark-selector',
    include_regional=False,
    include_country=True,
    include_global=True
)
```

The `create_benchmark_selectors` function automatically:
- Creates properly styled containers
- Applies correct CSS classes
- Sets default values (global benchmarks default to all except AFE/AFW)
- Returns unpacked components ready for layout

### Callback Registration Pattern

Callbacks are organized by feature area with nested structure:

```python
# Feature-level callback orchestrators (in src/callbacks/)
disaster_callbacks.py     # Coordinates all disaster visualizations
urbanization_callbacks.py # Coordinates all urbanization visualizations
flood_callbacks.py        # Coordinates all flood exposure visualizations
flood_projections_callbacks.py  # Coordinates all flood projections visualizations
main_callbacks.py         # Handles main navigation and header updates
country_benchmark_callbacks.py  # Populates country benchmark dropdowns

# Individual visualization callbacks (in src/callbacks/disaster/, urbanization/, flood/, or flood_projections/)
disaster/Frequency_by_Type_callbacks.py
disaster/Disasters_by_Year_callbacks.py
disaster/Total_Affected_Population_callbacks.py
disaster/Total_Deaths_callbacks.py
urbanization/Urban_Population_Projections_callbacks.py
urbanization/Urbanization_Rate_callbacks.py
urbanization/Urban_Population_Living_in_Slums_callbacks.py
urbanization/Access_to_Electricity_Urban_callbacks.py
urbanization/GDP_vs_Urbanization_callbacks.py
urbanization/Cities_Distribution_callbacks.py
urbanization/Cities_Evolution_callbacks.py
flood/National_Flood_Exposure_callbacks.py
flood/National_Flood_Exposure_Relative_callbacks.py
flood/National_Flood_Exposure_Population_callbacks.py
flood/National_Flood_Exposure_Population_Relative_callbacks.py
flood/Cities_Flood_Exposure_callbacks.py
flood_projections/Precipitation_callbacks.py
flood_projections/Urbanization_vs_Climate_Change_callbacks.py

# Registration in app.py (THIS IS THE ONLY PLACE CALLBACKS ARE REGISTERED)
from src.callbacks import disaster_callbacks, urbanization_callbacks, flood_callbacks, flood_projections_callbacks
from src.callbacks.main_callbacks import register_main_callbacks

register_main_callbacks(app)
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)
flood_callbacks.register_callbacks(app)
flood_projections_callbacks.register_callbacks(app)
flood_callbacks.register_callbacks(app)
```

### Error Handling Pattern (REQUIRED)

All error states MUST use centralized utilities - never create local error functions:

```python
from src.utils.component_helpers import create_error_chart

# Standard error handling pattern
try:
    # Load data
    data = load_emdat_data()
    
    # Filter and process
    if selected_country:
        data = data[data['ISO'] == selected_country]
    
    # Check for empty data
    if data.empty:
        raise Exception("No data available for selected country")
    
    # Create chart
    fig = create_chart(data)
    return fig
    
except Exception as e:
    return create_error_chart(
        error_message=f"Error loading data: {str(e)}",
        chart_type='bar',  # or 'line', 'scatter'
        xaxis_title='X Axis Label',
        yaxis_title='Y Axis Label',
        title='Chart Title'
    )
```

**NEVER** use these outdated patterns:
- ❌ Creating local `create_empty_chart` functions
- ❌ Raising `ValueError` for "no country selected" (use create_error_chart instead)
- ❌ Using `@handle_callback_errors` decorator (deprecated - use try/except)

### Data Processing Pipeline

#### EM-DAT Disaster Data Flow
1. **Raw data**: `data/raw/` - original Excel files from EM-DAT
2. **Processing script**: `scripts/clean_emdat_data.py` - filters Sub-Saharan countries, cleans columns
3. **Processed data**: `data/processed/african_disasters_emdat.csv` - cleaned CSV with columns:
   - `Disaster Type`, `ISO`, `Year`, `Total Deaths`, `Total Affected`, `Number of Events`
4. **Disaster types**: `data/Definitions/disaster_type_selection.txt` - 10 approved disaster categories

#### WDI Urbanization Data Flow
1. **Raw data**: `data/raw/WDI_CSV/WDICSV.csv` - World Bank World Development Indicators
2. **Processing script**: `scripts/clean_WDI_data.py` - extracts urbanization indicators for all global regions
3. **Processed data**: `data/processed/wdi/{INDICATOR_CODE}.csv` - one file per indicator with columns:
   - `Country Code`, `Year`, `Value`
4. **Indicators**: `data/Definitions/urbanization_indicators_selection.csv` - selected WDI indicators with metadata

#### UN DESA Urban Projections Flow
1. **Raw data**: `data/raw/Urban/` - UN World Urbanization Prospects and Population Division data
2. **Processing script**: `scripts/process_urban_population.py` - processes urban projections with uncertainty
3. **Processed data**: `data/processed/UNDESA_Country/{ISO3}_urban_population_projections.csv` - projections per country
4. **Consolidated**: `data/processed/UNDESA_Country/UNDESA_urban_projections_consolidated.csv` - all countries combined

#### Country Definitions
- `data/Definitions/WB_Classification.csv` - **Authoritative source** for:
  - All Sub-Saharan African countries (Region Code = SSA)
  - Regional mappings (Subregion Code = AFE or AFW)
  - Country metadata (income group, lending category)

## Development Workflow

### Running Locally
```bash
python app.py  # Starts on localhost:8050
```

### Adding New Visualizations (Step-by-Step)

#### Step 1: Create Callback File
Create `src/callbacks/urbanization/New_Feature_callbacks.py`:

```python
"""
Callbacks for [Feature Name] visualization
[Description of what this chart shows]
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.data_loader import load_wdi_data  # or appropriate loader
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_wdi_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from config.settings import CHART_STYLES

def register_new_feature_callbacks(app):
    """Register callbacks for [Feature Name] chart"""
    
    @app.callback(
        Output('new-feature-chart', 'figure'),
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_new_feature_chart(selected_country):
        try:
            # Load data
            data = load_wdi_data('INDICATOR_CODE')
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Handle no country selected
            if selected_country:
                title_suffix = countries_dict.get(selected_country)
                data = data[data['Country Code'] == selected_country]
            else:
                raise Exception("No country selected")
            
            if data.empty:
                raise Exception("No data available for selected country")
            
            # Create chart
            fig = go.Figure()
            # ... add traces ...
            
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | Chart Title',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']}
            )
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='line',
                title='Chart Title'
            )
```

#### Step 2: Register in Orchestrator
Update `src/callbacks/urbanization_callbacks.py`:

```python
# Add import at top
from .urbanization.New_Feature_callbacks import register_new_feature_callbacks

# Add registration in register_callbacks()
def register_callbacks(app):
    # ... existing registrations ...
    register_new_feature_callbacks(app)
    
    # Add new subtab rendering in render_urbanization_chart()
    elif active_subtab == 'new-feature':
        return html.Div([
            dcc.Graph(id="new-feature-chart"),
            html.Div([
                html.P([html.B("Data Source"), ": Source info.", html.Br(), 
                       html.B("Note:"), " Description."], 
                       className="indicator-note")
            ], className="indicator-note-container")
        ], className="chart-container")
```

#### Step 3: Add UI Tab
Update `src/layouts/world_bank_layout.py`:

```python
# Add new tab in create_world_bank_urbanization_tab_content()
dbc.Tab(
    label="New Feature",
    tab_id="new-feature"
)
```

### Adding New Data Sources

1. **Place raw data** in `data/raw/` with descriptive subfolder
2. **Create processing script** in `scripts/` folder following `clean_*.py` pattern:
   - Use centralized utilities: `from src.utils.country_utils import load_subsaharan_countries_dict`
   - Use centralized config: `from config.settings import DATA_CONFIG`
   - Filter by Sub-Saharan countries using `WB_Classification.csv`
   - Output to `data/processed/` with clear naming
3. **Add data definitions** to `data/Definitions/` if applicable
4. **Update data_loader.py** with new loading function:
```python
def load_new_data_source(indicator_code: str = None) -> pd.DataFrame:
    """
    Load new data source
    
    Args:
        indicator_code: Optional indicator code to filter
        
    Returns:
        DataFrame with columns: ['Country Code', 'Year', 'Value']
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, 'data', 'processed', 'new_source', f'{indicator_code}.csv')
    return pd.read_csv(file_path)
```
5. **Test data loading** before creating visualizations

### Regional Benchmark Integration

When adding charts with regional comparisons:

```python
# For Sub-Saharan Africa regional benchmarks (checkboxes)
from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names, get_benchmark_options

# In callback:
if benchmark_regions:  # e.g., ['SSA', 'AFE']
    colors = get_benchmark_colors()
    names = get_benchmark_names()
    for region_code in benchmark_regions:
        # Filter data for region
        region_data = data[data['Country Code'] == region_code]
        # Plot with colors[region_code]
```

```python
# For global benchmarks (dropdown)
from src.utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_colors, get_global_benchmark_names

# In callback:
if global_benchmarks:  # e.g., ['EAP', 'ECA', 'LCR']
    colors = get_global_benchmark_colors()
    names = get_global_benchmark_names()
    for region_code in global_benchmarks:
        # Filter data for region
        region_data = data[data['Country Code'] == region_code]
        # Plot with colors[region_code]
```

## Critical Configuration Files

### config/settings.py
Contains all hardcoded values that should be configurable:
- `DATA_CONFIG['emdat_start_year']` - Starting year for analysis (currently 1976)
- `DATA_CONFIG['analysis_period']` - Display string for time period
- `CHART_STYLES['colors']` - Color palette for charts
- `DASHBOARD_CONFIG` - App settings (title, port, debug mode)

### src/utils/benchmark_config.py
Regional benchmarks for Sub-Saharan Africa:
- `BENCHMARK_CONFIG` - Dictionary of region codes to names and colors
- SSA, AFE, AFW definitions

### src/utils/GLOBAL_BENCHMARK_CONFIG.py
Global regional benchmarks:
- `GLOBAL_BENCHMARK_CONFIG` - Merges BENCHMARK_CONFIG with additional world regions
- SSA, AFE, AFW, EAP, ECA, LCR, MNA, SAR definitions
- Functions for dropdown options and default selections

### data/Definitions/WB_Classification.csv
**Single source of truth** for:
- All country-to-region mappings
- Sub-Saharan Africa country list (Region Code = SSA)
- Subregional groupings (AFE, AFW)
- Country metadata (income levels, lending categories)

## Common Gotchas ⚠️

1. **Import paths**: Callbacks use relative imports (`..utils`) with try/catch fallback for direct execution
2. **Country filtering**: ALWAYS filter by Sub-Saharan Africa using centralized country utilities, NEVER hardcode ISO lists
3. **Callback dependencies**: Main country filter (`main-country-filter`) drives other components across all tabs
4. **Data columns**:
   - EM-DAT: `['Disaster Type', 'ISO', 'Year', 'Total Deaths', 'Total Affected', 'Number of Events']`
   - WDI: `['Country Code', 'Year', 'Value']`
   - UNDESA: Wide format with years as columns, indicators as rows
   - Fathom3 Flood: Country code, flood type, return period, built-up area/population values
5. **Regional benchmarks**: NEVER hardcode colors or names - always use `get_benchmark_colors()` and `get_benchmark_names()`
6. **Error handling**: ALWAYS use `create_error_chart()` - never create local error functions
7. **No country selected**: Use `create_error_chart()` with appropriate message - don't raise exceptions
8. **File paths**: All definition files in `data/Definitions/` - never use relative paths
9. **Chart IDs**: Must be unique across entire app - use format `{feature}-{chart-type}-chart`
10. **Global vs Regional**: Use GLOBAL_BENCHMARK_CONFIG for world regions, benchmark_config for SSA-only
11. **Download buttons**: ALWAYS add download functionality to new charts - follows two-component pattern:
    - Hidden `dcc.Download` component in layout (one ID per download)
    - Visible `create_download_trigger_button()` in orchestrator render function
    - Data callback watches button clicks and populates dcc.Download data
12. **Download IDs**: Download component IDs must follow pattern `{chart-name}-download` with button `{chart-name}-download-button`
13. **UI Helper Imports**: Always import the specific helper you need (`create_download_trigger_button`, `create_methodological_note_button`, etc.) not generic names
14. **Hero Map Button**: City-level platform button positioned in `.hero-map-action` (positioned absolutely within `.hero-map`)
15. **Flood Tab Structure**: 4 subtabs with flood-type-selector and return-period-selector; each subtab follows standard download/methodological pattern

## Folder Structure
```
├── app.py                    # Main entry point
├── config/
│   └── settings.py          # All configuration constants
├── data/
│   ├── Definitions/         # Config files (countries, indicators)
│   ├── processed/           # Cleaned data ready for dashboard
│   └── raw/                # Original data files
├── scripts/                # Data processing scripts
│   ├── clean_emdat_data.py
│   ├── clean_WDI_data.py
│   └── process_urban_population.py
├── src/
│   ├── callbacks/
│   │   ├── disaster/       # Individual disaster chart callbacks
│   │   ├── urbanization/   # Individual urbanization chart callbacks
│   │   ├── flood/          # Individual flood exposure chart callbacks
│   │   ├── flood_projections/  # Individual flood projections chart callbacks
│   │   ├── disaster_callbacks.py      # Disaster orchestrator
│   │   ├── urbanization_callbacks.py  # Urbanization orchestrator
│   │   ├── flood_callbacks.py         # Flood exposure orchestrator
│   │   ├── flood_projections_callbacks.py  # Flood projections orchestrator
│   │   ├── main_callbacks.py          # Navigation & header
│   │   └── country_benchmark_callbacks.py  # Country dropdown population
│   ├── layouts/
│   │   └── world_bank_layout.py       # Complete UI layout
│   └── utils/
│       ├── benchmark_config.py         # Regional benchmarks (SSA-specific)
│       ├── GLOBAL_BENCHMARK_CONFIG.py  # Global benchmarks (all regions)
│       ├── component_helpers.py        # Shared chart utilities and error handling
│       ├── data_loader.py             # Data loading utilities
│       ├── country_utils.py           # Country filtering utilities
│       ├── ui_helpers.py              # Reusable UI components
│       ├── download_helpers.py        # Data export utilities
│       ├── color_utils.py             # Disaster color configuration
│       ├── flood_ui_helpers.py        # Flood-specific UI components
│       └── precipitation_config.py    # Precipitation SSP color configuration
│       ├── color_utils.py             # Disaster color configuration
│       └── flood_ui_helpers.py        # Flood-specific UI components
├── assets/
│   ├── css/
│   │   ├── base.css                  # Global typography, spacing
│   │   ├── layout.css                # Page structure and grid
│   │   ├── hero.css                  # Hero section and SSA map
│   │   ├── navigation.css            # Header, tabs, nav styling
│   │   ├── filters.css               # Filter section styling
│   │   ├── dropdowns.css             # Dropdown component styling
│   │   ├── buttons.css               # Button styling (includes hero-map-action for city-level button)
│   │   ├── slider.css                # Year slider styling
│   │   ├── benchmarks.css            # Benchmark selector styling
│   │   ├── tabs-theme.css            # Tab styling and theme
│   │   ├── notes.css                 # Notes and indicators styling
│   │   ├── responsive.css            # Media queries for mobile/tablet
│   │   └── custom.css                # Imports all above
│   ├── documents/                    # Methodological notes and documentation
│   └── images/                       # Logos, icons, background images
├── DOWNLOAD_FEATURE.md                # Complete download feature guide
└── tests/
    └── [currently empty - old tests removed]
```

### Key CSS Structure Notes

- **Modular CSS**: Each component area has its own file, imported in `custom.css`
- **Tab Color Themes**: Use class-based styling in `tabs-theme.css` - apply `class_name="tab-blue"`, `class_name="tab-green"`, or `class_name="tab-orange"` to `dbc.Tab` components
  - Blue theme: Urban indicators, national-level data
  - Green theme: Services & infrastructure (water, sanitation, electricity)
  - Orange theme: City-level data and analysis
- **Hero Map Button**: `.hero-map-action` positioned with `position: absolute; top: 0.6rem; right: 0.6rem;` over `.hero-map` background
- **Download Buttons**: `.download-data-button` class styled with World Bank blue (295e84), hover effects
- **Subtabs**: Border-bottom removed from subtabs for clean appearance (`border-bottom: none` in tabs-theme.css)
- **Year Slider**: `dcc.Slider` component with custom CSS for compact, responsive display

## Deployment Context

- **Render.com**: Uses `render.yaml` with build command `./build.sh`
- **Heroku**: Uses `Procfile` with `web: python app.py`
- **Environment Variables**: `PORT` (defaults to 8050), `ENVIRONMENT` (dev/production)
- **Python Version**: 3.10+ (see `runtime.txt`)

## Dependencies

Core stack (from `requirements.txt`):
- `dash` + `dash-bootstrap-components` - UI framework
- `plotly` - charting library
- `pandas` + `numpy` - data processing
- `flask` - underlying web server

## Documentation Maintenance

**ALWAYS update this file** when making changes to:
- Architecture patterns and conventions
- New utility functions or shared components
- Error handling patterns
- File structure changes
- New visualization capabilities
- Data processing pipelines
- Configuration files or settings
- Benchmark systems

This ensures AI assistants have current knowledge for future development.
