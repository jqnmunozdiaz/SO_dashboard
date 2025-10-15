# Sub-Saharan Africa DRM Dashboard - AI Coding Instructions

## Architecture Overview

This is a **Dash-based dashboard** for analyzing disaster risk management (DRM) data across Sub-Saharan Africa. The application follows a modular architecture with clear separation of concerns:

- **Entry Point**: `app.py` - initializes Dash app, registers callbacks, handles deployment config
- **Layout System**: `src/layouts/world_bank_layout.py` - creates World Bank-styled UI components with responsive design
- **Callback Controllers**: `src/callbacks/` - organized by feature area with nested structure for complex visualizations
- **Data Layer**: `src/utils/` - centralized data loading, country utilities, chart helpers, and benchmark configuration
- **Configuration**: `config/settings.py` - comprehensive dashboard settings, styling, and environment configuration
- **Definitions**: `data/Definitions/` - centralized configuration files for countries, disaster types, and indicators

## Current Dashboard Structure

### Main Tabs
1. **Historical Disasters** - EM-DAT disaster analysis with four subtabs:
   - Frequency by Type - disaster type distribution charts
   - Disasters by Year - temporal trend analysis
   - Total Affected Population - population impact analysis
   - Total Deaths - mortality impact analysis

2. **Historical Urbanization** - WDI urbanization indicators with three subtabs:
   - Urban Population Living in Slums - slums population trends with regional benchmarks
   - Access to Electricity, Urban - electricity access trends with regional benchmarks
   - Urbanization Rate - urban population growth projections with regional benchmarks

3. **Exposure to Flood Hazard** - (placeholder for future flood risk data)
4. **Projections of Flood Risk** - (placeholder for future flood projections)

## Key Patterns & Conventions

### Data Loading Pattern
All data access goes through centralized utilities in `src/utils/`:
```python
# Country data - always use centralized utilities
from src.utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Disaster data - use the standardized loader
from src.utils.data_loader import load_emdat_data

# WDI data - urbanization indicators
from src.utils.data_loader import load_wdi_data, load_urbanization_indicators_dict

# Regional benchmarks - centralized configuration
from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names, get_benchmark_options

# Error handling - use shared chart utilities
from src.utils.component_helpers import create_error_chart
```

### Callback Registration
Callbacks are organized by feature area with nested structure:
```python
# Feature-level callback orchestrators
src/callbacks/disaster_callbacks.py     # Coordinates all disaster visualizations
src/callbacks/urbanization_callbacks.py # Coordinates all urbanization visualizations
src/callbacks/main_callbacks.py         # Handles main navigation and header updates

# Individual visualization callbacks
src/callbacks/disaster/Frequency_by_Type_callbacks.py
src/callbacks/disaster/Disasters_by_Year_callbacks.py
src/callbacks/disaster/Total_Affected_Population_callbacks.py
src/callbacks/disaster/Total_Deaths_callbacks.py
src/callbacks/urbanization/Urban_Population_Living_in_Slums_callbacks.py
src/callbacks/urbanization/Access_to_Electricity_Urban_callbacks.py
src/callbacks/urbanization/Urbanization_Rate_callbacks.py

# Registration in app.py
from src.callbacks import disaster_callbacks, urbanization_callbacks
from src.callbacks.main_callbacks import register_main_callbacks

register_main_callbacks(app)
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)
```

### Error Handling Pattern
All error states use centralized utilities in `src/utils/component_helpers.py`:
```python
# For error charts with annotations
from src.utils.component_helpers import create_error_chart

# Handle data loading errors - use create_error_chart with appropriate parameters
# Handle empty data gracefully - use create_error_chart with appropriate parameters
# Handle "no country selected" consistently - use title_suffix = "No country selected"
```

### Data Processing Pipeline

**EM-DAT Disaster Data Flow:**
1. **Raw data**: `data/raw/` - original Excel files from EM-DAT
2. **Processing script**: `scripts/clean_emdat_data.py` - filters Sub-Saharan countries, cleans columns
3. **Processed data**: `data/processed/african_disasters_emdat.csv` - cleaned CSV for dashboard use
4. **Disaster types**: `data/Definitions/disaster_type_selection.txt` - approved disaster categories

**WDI Urbanization Data Flow:**
1. **Raw data**: `data/raw/WDI_CSV/` - World Bank World Development Indicators
2. **Processing script**: `scripts/clean_WDI_data.py` - extracts urbanization indicators
3. **Processed data**: `data/processed/wdi/` - individual CSV files per indicator
4. **Indicators**: `data/Definitions/urbanization_indicators_selection.csv` - selected WDI indicators

**Country Definitions:**
- `data/Definitions/WB_Classification.csv` - World Bank country classifications (authoritative source for all Sub-Saharan African countries and regional mappings)

## Development Workflow

### Running Locally
```bash
python app.py  # Starts on localhost:8050
```

### Documentation Updates
**IMPORTANT**: Always update `.github/copilot-instructions.md` when making significant changes to:
- Architecture patterns and conventions
- New utility functions or shared components
- Error handling patterns
- File structure changes
- New visualization capabilities
- Data processing pipelines

This ensures the AI assistant has current knowledge of the codebase for future development tasks.

### Data Updates

**Updating Disaster Data:**
1. Place new EM-DAT Excel file in `data/raw/`
2. Update file path in `scripts/clean_emdat_data.py`
3. Run: `python scripts/clean_emdat_data.py`
4. Restart dashboard to pick up new data

**Updating Urbanization Data:**
1. Place new WDI CSV files in `data/raw/WDI_CSV/`
2. Update indicators in `data/Definitions/urbanization_indicators_selection.csv` if needed
3. Run: `python scripts/clean_WDI_data.py`
4. Restart dashboard to pick up new data

**Updating Country Lists:**
1. Modify `data/Definitions/WB_Classification.csv` for country additions/removals or regional changes
2. Update Region Code (SSA), Subregion Code (AFE/AFW), and country classifications as needed
3. No processing script needed - changes take effect on restart

### Adding New Visualizations
1. **Create individual callback file** in appropriate subfolder (`src/callbacks/disaster/` or `src/callbacks/urbanization/`)
2. **Follow naming convention**: `Feature_Name_callbacks.py` with `register_feature_name_callbacks(app)` function
3. **Update orchestrator** (`disaster_callbacks.py` or `urbanization_callbacks.py`) to import and register new callback
4. **Add subtab** to `src/layouts/world_bank_layout.py` in the appropriate tab section
5. **Update chart container logic** in orchestrator to handle new subtab rendering
6. **Use centralized utilities**: `benchmark_config.py` for regional comparisons, `data_loader.py` for data access
7. **Follow error handling patterns**: graceful degradation with informative error messages

### Adding New Data Sources
1. **Place raw data** in `data/raw/` with descriptive subfolder
2. **Create processing script** in `scripts/` folder following `clean_*.py` pattern
3. **Output processed data** to `data/processed/` with clear naming
4. **Add data definitions** to `data/Definitions/` if applicable
5. **Update data_loader.py** with new loading functions
6. **Test data loading** before creating visualizations

### Regional Benchmark Integration
When adding charts with regional comparisons:
1. **Import benchmark utilities**: `from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names, get_benchmark_options`
2. **Use standard colors**: SSA (red), AFE (orange), AFW (green)
3. **Add benchmark selector**: Use `get_benchmark_options()` for consistent checklist options
4. **Handle benchmark data**: Filter for regional codes and apply appropriate styling

## Deployment Context

- **Render.com**: Uses `render.yaml` with build command `./build.sh`
- **Heroku**: Uses `Procfile` with `web: python app.py`
- **Environment Variables**: `PORT` (defaults to 8050), `ENVIRONMENT` (dev/production)
- **Python Version**: 3.10+ (see `runtime.txt`)

## Critical Dependencies

Core stack (from `requirements.txt`):
- `dash` + `dash-bootstrap-components` - UI framework
- `plotly` - charting library
- `pandas` + `numpy` - data processing
- `flask` - underlying web server

Optional packages commented out for deployment compatibility - install separately if needed.

## Common Gotchas

1. **Import paths**: Callbacks use relative imports (`..utils`) with try/catch fallback for direct execution
2. **Country filtering**: Always filter by Sub-Saharan Africa using centralized country utilities, never hardcode ISO lists
3. **Callback dependencies**: Main country filter (`main-country-filter`) drives other components across all tabs
4. **Data columns**: 
   - EM-DAT processed data: `['Disaster Type', 'ISO', 'Year', 'Total Deaths', 'Total Affected']`
   - WDI processed data: `['Country Code', 'Year', 'Value']`
5. **Regional benchmarks**: Use `src/utils/benchmark_config.py` for colors, names, and options - never hardcode
6. **Error handling**: Always use `create_error_chart()` from `component_helpers.py` for consistent error states - never create local `create_empty_chart` functions
7. **No country selected**: Always use `title_suffix = "No country selected"` instead of raising `ValueError` - this allows benchmark data to still be displayed
8. **File paths**: All definition files moved to `data/Definitions/` - update imports accordingly
9. **Chart IDs**: Each visualization has unique IDs (e.g., `urban-population-slums-chart`, `access-to-electricity-urban-chart`)

## File Dependencies & Data Structure

### Core Data Files
- **Country Selection**: `src/utils/data_loader.get_subsaharan_countries()` for dropdowns
- **Disaster Data**: `data/processed/african_disasters_emdat.csv` (required for disaster callbacks)
- **Urbanization Data**: `data/processed/wdi/*.csv` (individual indicator files)
- **Chart Styling**: `config/settings.py` constants and `src/utils/benchmark_config.py`

### Definition Files (data/Definitions/)
- `WB_Classification.csv` - World Bank country classifications (authoritative source for countries and regions)
- `disaster_type_selection.txt` - 10 approved disaster types
- `urbanization_indicators_selection.csv` - 2 WDI indicators (slums, electricity)

### Folder Structure
```
src/
├── callbacks/
│   ├── disaster/           # Individual disaster chart callbacks
│   ├── urbanization/       # Individual urbanization chart callbacks
│   ├── disaster_callbacks.py      # Disaster orchestrator
│   ├── urbanization_callbacks.py  # Urbanization orchestrator
│   └── main_callbacks.py          # Navigation & header
├── layouts/
│   └── world_bank_layout.py       # Complete UI layout
└── utils/
    ├── benchmark_config.py         # Regional benchmark settings
    ├── component_helpers.py        # Shared chart utilities and error handling
    ├── data_loader.py             # Data loading utilities
    ├── country_utils.py           # Country filtering utilities
    └── [other utilities]
```

### Current Visualization Capabilities
1. **Disaster Analysis** (4 charts): Frequency by type, timeline trends, affected population, deaths analysis
2. **Urbanization Analysis** (4 charts): Slums population trends, electricity access trends, urbanization rate projections, GDP vs urbanization scatterplot
3. **Regional Benchmarks**: SSA, Eastern/Southern Africa, Western/Central Africa comparisons
4. **Interactive Features**: Country selection, benchmark toggling, responsive design

When modifying core data structures or adding features, ensure consistency across these interconnected layers.