# Sub-Saharan Africa DRM Dashboard - AI Coding Instructions

## Architecture Overview

Dash-based dashboard for analyzing disaster risk management (DRM), urbanization, and flood exposure across Sub-Saharan Africa. **Strictly modular architecture** with clear separation of concerns.

### Core Layers

- **Entry**: `app.py` - initializes app, registers callbacks, deployment config
- **Layout**: `src/layouts/world_bank_layout.py` - World Bank-styled UI, responsive design  
- **Callbacks**: `src/callbacks/` - organized by feature with nested structure
- **Data**: `src/utils/` - centralized loading, country utilities, chart helpers, benchmarks
- **Config**: `config/settings.py` - all settings, styling, environment (NEVER hardcode)
- **Definitions**: `data/Definitions/` - countries, disaster types, indicators

### Critical Principles ⚠️

1. **No Hardcoding**: Values → `config/settings.py`, `data/Definitions/`, or `src/utils/*_config.py`
2. **Centralized Utilities**: Use `src/utils/` - never duplicate logic
3. **Config-Driven**: Add config, not code
4. **Reusable Components**: `src/utils/ui_helpers.py` - parametric and reusable
5. **Single Source**: One definition per element

## Dashboard Structure

1. **Historical Disasters** (EM-DAT): Overview, By Year, Affected Population, Deaths
2. **Historical Urbanization** (WDI/UN DESA): Projections, Rate, Density, Slums, Electricity, GDP vs Urban, Cities Distribution/Evolution, Pop & Economic Activity
3. **Flood Hazard** (Fathom3): National Exposure, Cities Exposure
4. **Flood Projections**: Precipitation Changes, Urbanization vs Climate

## Key Patterns

### Data Loading (REQUIRED - Always Use Centralized)

```python
# Country utilities
from src.utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Data loaders
from src.utils.data_loader import load_emdat_data, load_wdi_data, load_undesa_urban_projections

# Benchmarks: Regional (SSA/AFE/AFW) vs Global (all regions)
from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names
from src.utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_colors, get_global_benchmark_names

# UI components & downloads
from src.utils.ui_helpers import create_benchmark_selectors, create_download_trigger_button, create_methodological_note_button
from src.utils.download_helpers import prepare_csv_download, prepare_multi_csv_download
from src.utils.component_helpers import create_error_chart
```

### Download Pattern

Two-component pattern for CSV downloads:

1. **Hidden Component** (layout): `create_download_component("chart-name-download")`
2. **Visible Button** (orchestrator): `create_download_trigger_button('chart-name-download')`
3. **Callback** (chart file): Watches button clicks, returns `prepare_csv_download(data, filename)`

```python
# Callback example
@app.callback(
    Output('chart-download', 'data'),
    [Input('chart-download-button', 'n_clicks'), Input('main-country-filter', 'value')],
    prevent_initial_call=True
)
def download_data(n_clicks, country):
    if not n_clicks: return None
    data = load_emdat_data()
    if country: data = data[data['ISO'] == country]
    return prepare_csv_download(data, f"data_{country}")
```

### Benchmark System

**Regional** (SSA/AFE/AFW) vs **Global** (all regions including EAP/ECA/LCR/MNA/SAR)

```python
from src.utils.ui_helpers import create_benchmark_selectors

# Regional checkboxes + Country dropdown
*create_benchmark_selectors(
    regional_id='chart-benchmark-selector',
    country_id='chart-country-benchmark-selector',
    include_regional=True, include_country=True
)

# Global dropdown + Country dropdown  
*create_benchmark_selectors(
    global_id='chart-global-benchmark-selector',
    country_id='chart-country-benchmark-selector',
    include_global=True, include_country=True
)
```

### Callback Registration

```python
# Orchestrators coordinate feature areas
src/callbacks/disaster_callbacks.py
src/callbacks/urbanization_callbacks.py
src/callbacks/flood_callbacks.py
src/callbacks/flood_projections_callbacks.py

# Individual chart callbacks in subdirectories
src/callbacks/disaster/Frequency_by_Type_callbacks.py
src/callbacks/urbanization/Urban_Population_Projections_callbacks.py
src/callbacks/flood/National_Flood_Exposure_callbacks.py

# Registration ONLY in app.py
from src.callbacks import disaster_callbacks, urbanization_callbacks
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)
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

- **Google Cloud Run**: Built and deployed via Cloud Build using `cloudbuild.yaml` (image caching, dual tagging to `:latest` and `:$COMMIT_SHA`, deploy pinned `:$COMMIT_SHA`).
- **Service Configuration**: Key settings managed in Cloud Run (region, min/max instances, memory/CPU, concurrency, timeout). App binds to `0.0.0.0` and reads `PORT`.
- **Environment Variables**: `PORT` (defaults to 8050 when local), `ENVIRONMENT` (dev/production).
- **Python Version**: 3.10+ (see `runtime.txt`).

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
