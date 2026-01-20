# SO Dashboard Source Code Documentation

This document provides a comprehensive guide to the Sub-Saharan Africa DRM Dashboard codebase, including tab/subtab structure, data sources, and benchmarking configuration.

## Tab Structure Overview

The dashboard has 4 main tabs, each with multiple subtabs:

| Main Tab | Tab ID | Subtabs |
|----------|--------|---------|
| Historical Disasters | `disasters` | 4 subtabs |
| Urbanization Trends | `urbanization` | 14 subtabs |
| Exposure to Flood Hazard | `flood-exposure` | 2 subtabs |
| Future Precipitation Extremes | `flood-projections` | 3 subtabs |

---

## 1. Historical Disasters Tab

### Subtabs and Data

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| Overview of Disasters | `disaster-frequency` | `disaster/Frequency_by_Type_callbacks.py` | `african_disasters_emdat.csv` |
| Disasters by Year | `disaster-timeline` | `disaster/Disasters_by_Year_callbacks.py` | `african_disasters_emdat.csv` |
| Total Affected Population | `disaster-affected` | `disaster/Total_Affected_Population_callbacks.py` | `african_disasters_emdat.csv` |
| Total Deaths | `disaster-deaths` | `disaster/Total_Deaths_callbacks.py` | `african_disasters_emdat.csv` |

**Main Data Source**: EM-DAT Emergency Events Database  
**Data Loader**: `load_emdat_data()` in `utils/data_loader.py`

---

## 2. Urbanization Trends Tab

### Subtabs (Blue Group - National Indicators)

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| Population | `urban-population-projections` | `urbanization/Urban_Population_Projections_callbacks.py` | `WUP/` folder (WUP2025 + WPP2024) |
| Urbanization Level | `urbanization-rate` | `urbanization/Urbanization_Rate_callbacks.py` | `WUP/WUP2025_National_Definitions.csv` |
| Urban System | `urban-system` | `urbanization/Urban_System_callbacks.py` | WUP2025 Level1 data |
| GDP vs Urbanization | `gdp-vs-urbanization` | `urbanization/GDP_vs_Urbanization_callbacks.py` | `wdi/SP.URB.TOTL.IN.ZS.csv` |
| Built-up per capita | `urban-density` | `urbanization/Urban_Density_callbacks.py` | `built_up_per_capita_m2_by_country_year.csv` |
| Population Living in Slums | `urban-population-slums` | `urbanization/Urban_Population_Living_in_Slums_callbacks.py` | `wdi/EN.POP.SLUM.UR.ZS.csv` |

### Subtabs (Green Group - Infrastructure Access)

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| Access to Drinking Water | `access-to-drinking-water` | `urbanization/Access_to_Drinking_Water_callbacks.py` | `jmp_water/` |
| Access to Sanitation | `access-to-sanitation` | `urbanization/Access_to_Sanitation_callbacks.py` | `jmp_sanitation/` |
| Access to Electricity | `access-to-electricity-urban` | `urbanization/Access_to_Electricity_Urban_callbacks.py` | `wdi/EG.ELC.ACCS.UR.ZS.csv` |

### Subtabs (Orange Group - City-Level Data)

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| Cities Distribution | `cities-distribution` | `urbanization/Cities_Distribution_callbacks.py` | `agglomeration_population_builtup_merged.csv` |
| Cities Evolution | `cities-evolution` | `urbanization/Cities_Evolution_callbacks.py` | `africapolis_worldpop_final_merged.csv` |
| Built-up per capita in Cities | `cities-growth-rate` | `urbanization/Cities_builtup_per_capita.py` | `africapolis_ghsl_simple.csv` |
| Cities Growth | `cities-growth` | `urbanization/Cities_Growth_callbacks.py` | `africapolis_worldpop_final_merged.csv` |
| Population & Economic Activity | `population-economic-activity` | `urbanization/Population_Economic_Activity_callbacks.py` | `gdp_pop_raster_images_3d/` |

**Main Data Sources**:
- UN DESA WUP2025 (World Urbanization Prospects)
- UN WPP2024 (World Population Prospects)  
- World Bank WDI (World Development Indicators)
- JMP WASH (Water/Sanitation)
- Africapolis (City-level data)
- GHSL (Global Human Settlement Layer)

---

## 3. Flood Exposure Tab

### Subtabs and Data

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| National Flood Exposure | `national-flood-exposure` | `flood/National_Flood_Exposure_*.py` | `flood/Flood_exposure_*.csv` |
| Cities Flood Exposure | `cities-flood-exposure` | `flood/Cities_Flood_Exposure_callbacks.py` | `flood/Flood_exposure_*.csv` |

**Data Loader**: `load_flood_exposure_data()` in `utils/flood_data_loader.py`  
**Main Data Sources**: Fathom3 (flood hazard) + GHSL (built-up areas)

### National Flood Exposure Display Options

Four variants controlled by exposure type and measurement type:
- Built-up Area (Absolute) → `National_Flood_Exposure_callbacks.py`
- Built-up Area (Relative %) → `National_Flood_Exposure_Relative_callbacks.py`
- Population (Absolute) → `National_Flood_Exposure_Population_callbacks.py`
- Population (Relative %) → `National_Flood_Exposure_Population_Relative_callbacks.py`

---

## 4. Future Precipitation Extremes Tab

### Subtabs and Data

| Subtab | Tab ID | Callback File | Data Source |
|--------|--------|--------------|-------------|
| Overview | `overview` | N/A (static content) | None |
| Changes in Extreme Precipitation | `precipitation` | `flood_projections/Precipitation_callbacks.py` | `ReturnPeriods-1day-clean.csv` |
| Urbanization and Climate Change | `urbanization-vs-climate` | `flood_projections/Urbanization_vs_Climate_Change_callbacks.py` | `ALL_SSA_BUexp_projected_consolidated.csv` |

**Data Sources**: Climate Change Knowledge Portal (CCKP) precipitation projections

---

## Benchmarking Menu System

The dashboard allows comparing countries against regional benchmarks.

### Configuration Files

| File | Purpose |
|------|---------|
| `utils/benchmark_config.py` | SSA regional benchmarks |
| `utils/GLOBAL_BENCHMARK_CONFIG.py` | Global regional benchmarks |

### SSA Regional Benchmarks (`benchmark_config.py`)

| Code | Region | Color |
|------|--------|-------|
| `SSA` | Sub-Saharan Africa | #e74c3c (Red) |
| `AFE` | Eastern and Southern Africa | #f39c12 (Orange) |
| `AFW` | Western and Central Africa | #27ae60 (Green) |

### Global Benchmarks (`GLOBAL_BENCHMARK_CONFIG.py`)

| Code | Region | Color |
|------|--------|-------|
| `EAS` | East Asia & Pacific | #2980b9 |
| `ECS` | Europe & Central Asia | #8e44ad |
| `LCN` | Latin America & Caribbean | #d35400 |
| `MEA` | Middle East & North Africa | #16a085 |
| `TSA` | South Asia | #c0392b |

### UI Helper Functions

Located in `utils/ui_helpers.py`:
- `create_combined_benchmark_selector()` - Creates checkbox group for benchmark selection
- Benchmark selections stored in `dcc.Store(id='flood-benchmark-store')`

---

## Key Data Files Summary

### Location: `data/processed/`

| File | Used By | Description |
|------|---------|-------------|
| `african_disasters_emdat.csv` | Disaster tabs | EM-DAT historical disaster events |
| `WUP/WUP2025_*.csv` | Population, Urbanization Level | UN urbanization projections |
| `WPP2024_Total_Population.csv` | Population projections | Total population by country |
| `wdi/*.csv` | GDP, Slums, Electricity | World Bank indicators |
| `jmp_water/`, `jmp_sanitation/` | Water, Sanitation | JMP WASH data |
| `africapolis_*.csv` | Cities tabs | Africapolis city-level data |
| `africapolis_ghsl_simple.csv` | Built-up per capita | GHSL built-up areas |
| `flood/Flood_exposure_*.csv` | Flood tabs | Fathom3 flood exposure |
| `ReturnPeriods-1day-clean.csv` | Precipitation | CCKP precipitation projections |
| `ALL_SSA_BUexp_projected_consolidated.csv` | Climate Change | Future flood exposure projections |

---

## Callback Architecture

### Main Orchestrators

| File | Responsibility |
|------|----------------|
| `callbacks/disaster_callbacks.py` | Routes disaster subtab selection |
| `callbacks/urbanization_callbacks.py` | Routes urbanization subtab selection |
| `callbacks/flood_callbacks.py` | Routes flood exposure subtab selection |
| `callbacks/flood_projections_callbacks.py` | Routes flood projections subtab selection |

### Registration Flow

1. `app.py` imports and calls `register_callbacks(app)` for each orchestrator
2. Orchestrator registers individual subtab callbacks
3. Orchestrator callback routes to appropriate chart based on active subtab

---

## Adding New Visualizations

1. Create new callback file in appropriate subfolder (e.g., `callbacks/urbanization/`)
2. Implement `register_*_callbacks(app)` function that:
   - Loads data at registration time for performance
   - Creates `@app.callback` for chart generation
   - Creates download callback using `create_simple_download_callback()`
3. Import and call in orchestrator file
4. Add tab to layout in `layouts/world_bank_layout.py`
5. Add download component to hidden div in layout
