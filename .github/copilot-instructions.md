# Sub-Saharan Africa DRM Dashboard - AI Coding Instructions

## Architecture Overview

This is a **Dash-based dashboard** for analyzing disaster risk management (DRM) data across Sub-Saharan Africa. The application follows a modular architecture with clear separation of concerns:

- **Entry Point**: `app.py` - initializes Dash app, registers callbacks, handles deployment config
- **Layout System**: `src/layouts/world_bank_layout.py` - creates World Bank-styled UI components matching Review_CatDDOs design patterns
- **Callback Controllers**: `src/callbacks/` - handles user interactions and data updates
- **Data Layer**: `src/utils/` - centralized data loading, country utilities, chart helpers
- **Configuration**: `config/settings.py` - styling, disaster types, risk levels, API endpoints

## Key Patterns & Conventions

### Data Loading Pattern
All data access goes through centralized utilities in `src/utils/`:
```python
# Country data - always use centralized utilities
from src.utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Disaster data - use the standardized loader
from src.utils.data_loader import load_emdat_data
```

### Callback Registration
Callbacks are organized by feature area with a registration pattern:
```python
# In callback files: define functions then register with app
def register_callbacks(app):
    @app.callback(...)
    def callback_function():
        pass

# In app.py: import and register
from src.callbacks import disaster_callbacks
disaster_callbacks.register_callbacks(app)
```

### World Bank Styling System
UI follows World Bank design system with specific color palette and styling:
- Primary blue: `#295e84`
- Layout uses flexbox with `height: 100vh` and `overflow: hidden`
- Cards use consistent shadow: `box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1)`
- Colors and styles defined in `config/settings.py` under `CHART_STYLES`

### Data Processing Pipeline
EM-DAT data follows this processing flow:
1. **Raw data**: `data/raw/` - original Excel files from EM-DAT
2. **Processing script**: `scripts/clean_emdat_data.py` - filters Sub-Saharan countries, cleans columns
3. **Processed data**: `data/processed/african_disasters_emdat.csv` - cleaned CSV for dashboard use
4. **Country filtering**: Uses `data/sub_saharan_countries.csv` and `data/non_sub_saharan_african_countries.csv`

## Development Workflow

### Running Locally
```bash
python app.py  # Starts on localhost:8050
```

### Data Updates
When updating disaster data:
1. Place new EM-DAT Excel file in `data/raw/`
2. Update file path in `scripts/clean_emdat_data.py`
3. Run: `python scripts/clean_emdat_data.py`
4. Restart dashboard to pick up new data

### Adding New Visualizations
1. Create chart function in `src/utils/chart_helpers.py`
2. Add callback in appropriate `src/callbacks/` file
3. Update layout in `src/layouts/world_bank_layout.py`
4. Register callback in `app.py`

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
3. **Callback dependencies**: Main country filter (`main-country-filter`) drives other components
4. **Data columns**: EM-DAT processed data has standardized columns: `['Disaster Type', 'ISO', 'Year', 'Total Deaths', 'Total Affected']`
5. **Error handling**: Callbacks should gracefully handle missing data and return empty charts with error messages

## File Dependencies

- Layout components depend on `src/utils/data_loader.get_subsaharan_countries()` for dropdowns
- Disaster callbacks require `data/processed/african_disasters_emdat.csv` to exist
- Chart styling pulls from `config/settings.py` constants
- Country utilities read from `data/sub_saharan_countries.csv` and `data/non_sub_saharan_african_countries.csv`

When modifying core data structures or adding features, ensure consistency across these interconnected layers.