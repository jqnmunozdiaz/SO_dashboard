# Sub-Saharan Africa DRM Dashboard — Methodological Note

Last updated: 2025-10-21

This note documents data sources, definitions, processing pipelines, and figure-specific methodologies used in the Sub-Saharan Africa Disaster Risk Management (DRM) Dashboard. It focuses on data and computation, not the application code.

- Scope: Sub-Saharan Africa (SSA) countries as defined by the World Bank classification.
- Country and region definitions: see `data/Definitions/WB_Classification.csv` (single source of truth). Subregions used: Eastern & Southern Africa (AFE) and Western & Central Africa (AFW). Global region codes may appear as SSA, EAP, ECA, LCR, MNA, SAR, etc.
- Indicators and metadata: see `data/Definitions/urbanization_indicators_selection.csv` and `data/Definitions/disaster_type_selection.txt`.

## 1) Data Sources (authoritative)

- EM-DAT: International Disaster Database (CRED) — disaster events, impacts (events, affected, deaths).
- World Bank WDI — socioeconomic indicators (urbanization, electricity access, GDP per capita, etc.).
- UN DESA — World Urbanization Prospects and Population Division (urban population levels/projections with uncertainty; growth rates).
- Fathom3 Flood Hazard — modeled fluvial/pluvial flood extents and depths by return periods.
- GHSL 2023 (Global Human Settlement Layer) — built-up area and population (baselines for exposure and city analytics).
- JMP (WHO/UNICEF Joint Monitoring Programme) — water and sanitation service ladders (urban shares).
- Africapolis — urban agglomerations/cities database (city counts, sizes; used in combination with GHSL).

Note: Specific dataset vintages are managed in the repository and processing scripts; the dashboard presents the processed outputs. 

## 2) Region and Country Universe

- Country universe and regional mapping are taken from `WB_Classification.csv`.
- SSA membership is defined by Region Code = `SSA` in that file.
- Subregional codes used: `AFE` (Eastern & Southern Africa) and `AFW` (Western & Central Africa).
- Global regions for selected comparisons: `SSA`, `AFE`, `AFW`, `EAP`, `ECA`, `LCR`, `MNA`, `SAR`.
- ISO3 country codes: authoritative and harmonized from the same classification.

All filters by country/region in the charts and processing steps rely on this single source of truth.

## 3) Processed Outputs (where the charts read from)

- EM-DAT (SSA subset): `data/processed/african_disasters_emdat.csv`
  - Columns: `Disaster Type`, `ISO`, `Year`, `Total Deaths`, `Total Affected`, `Number of Events`.
- WDI indicators (one file per indicator): `data/processed/wdi/{INDICATOR_CODE}.csv`
  - Columns: `Country Code`, `Year`, `Value`.
- UN DESA urban projections (country and consolidated):
  - Per-country: `data/processed/UNDESA_Country/{ISO3}_urban_population_projections.csv`
  - Consolidated: `data/processed/UNDESA_Country/UNDESA_urban_projections_consolidated.csv`
- Flood exposure (Fathom3 over GHSL baselines):
  - Built-up exposed (absolute): `data/processed/flood/country_ftm3_current_ghsl2023_built_s.csv`
  - Population exposed (absolute): `data/processed/flood/country_ftm3_current_ghsl2023_pop.csv`
  - Relative exposure derived by dividing by GHSL baselines (built-up/population totals).
- Cities analytics:
  - Size distribution: `data/processed/city_size_distribution.csv`
  - Agglomeration counts: `data/processed/city_agglomeration_counts.csv`
  - City-level detail: `data/processed/cities_individual.csv`
- Population totals (WPP): `data/processed/WPP2024_Total_Population.csv` (used for contextual rates where indicated).
- JMP WASH (urban): files under `data/processed/jmp_water/` and `data/processed/jmp_sanitation/`.

These files are the direct inputs to the figures; raw sources reside under `data/raw/` and are transformed by scripts under `scripts/`.

## 4) Processing Pipelines (scripts)

All scripts live under `scripts/` and use shared utilities for country filtering and configuration.

### 4.1 EM-DAT (Disasters)
- Script: `scripts/clean_emdat_data.py`
- Steps:
  1. Load raw EM-DAT workbook(s) from `data/raw/`.
  2. Harmonize country codes to ISO3 using `WB_Classification.csv`.
  3. Filter to SSA countries only.
  4. Map to a curated set of 10 disaster categories using `data/Definitions/disaster_type_selection.txt`.
  5. Aggregate metrics per (`Disaster Type`, `ISO`, `Year`): `Number of Events`, `Total Affected`, `Total Deaths`.
  6. Output tidy CSV: `data/processed/african_disasters_emdat.csv`.
- Data handling:
  - Missing numeric fields are treated as zeros when aggregating by year/type.
  - Years outside the analysis window may be excluded via configuration.

### 4.2 WDI (Urbanization, Electricity, GDP, etc.)
- Script: `scripts/clean_WDI_data.py`
- Steps:
  1. Load `data/raw/WDI_CSV/WDICSV.csv`.
  2. Select indicators defined in `data/Definitions/urbanization_indicators_selection.csv` (codes, names, units, notes).
  3. Extract series into one tidy CSV per indicator: `Country Code`, `Year`, `Value` at annual frequency.
  4. Include series for global/region aggregates where WDI publishes them (e.g., SSA, AFE, AFW, other world regions), enabling benchmark overlays.
- Data handling:
  - Values are used “as published” by WDI unless explicitly noted; no smoothing by default.
  - Some charts may select the latest common year across series for cross-sectional comparisons.

### 4.3 UN DESA (Urban Population Projections and Growth)
- Script: `scripts/process_urban_population.py`
- Steps:
  1. Load UN DESA urban population levels and projections from `data/raw/Urban/`.
  2. Produce per-country and consolidated outputs with central (median) projections and uncertainty bands (e.g., lower/upper intervals when available).
  3. Derive annual growth rates from multi-year steps using compounded annual growth rate (CAGR).
- Formulas:
  - Annualized CAGR over k years for a series V:
    $$\text{CAGR} = \left(\frac{V_t}{V_{t-k}}\right)^{\frac{1}{k}} - 1$$
  - In our workflow, when projections are at 5-year intervals, we use $k = 5$.
- Data handling:
  - Country codes harmonized to ISO3; SSA subset is selected for country-level visuals.
  - Uncertainty bands are plotted when available (central, lower, upper).

### 4.4 Flood Exposure (Fathom3 × GHSL 2023)
- Script(s): `scripts/aggregate_regional_flood_data.py` (aggregation); preprocessing steps are reflected in `data/processed/flood/`.
- Concepts:
  - Flood hazard types: typically fluvial (river) and pluvial (surface) flooding.
  - Return periods (RPs): e.g., 1-in-5, 1-in-10, 1-in-25, 1-in-50, 1-in-100, 1-in-250 (exact set configured in data).
- Steps:
  1. Overlay Fathom3 flood hazard footprints by hazard type and RP with GHSL 2023 rasters (built-up, population) for each country.
  2. Sum exposed built-up area and exposed population within hazard footprints ➜ absolute exposure.
  3. Obtain total built-up and population baselines (GHSL-derived) ➜ relative exposure as shares of totals.
  4. Aggregate to regional benchmarks as needed (SSA/AFE/AFW) using published regional series where available; otherwise compute totals/weighted averages consistently with the metric.
- Metrics:
  - Absolute exposure: total exposed built-up (area units) or population (persons).
  - Relative exposure: $\text{share} = \frac{\text{exposed}}{\text{total baseline}}$.

### 4.5 Cities and Urban Form (Africapolis × GHSL)
- Scripts: `scripts/process_city_size_distribution.py`, `scripts/process_city_agglomeration_counts.py`, `scripts/merge_africapolis_ghsl_data.py`
- Steps:
  1. Integrate Africapolis urban agglomeration boundaries/attributes with GHSL population/built-up for harmonized time slices.
  2. Compute counts and distributions of cities by size classes used in the dashboard.
  3. Produce country-level time series and cross-sections for city size distributions and evolution.
- Notes:
  - Exact thresholds/bins for size classes are the ones embedded in the processed outputs (e.g., size bins present in `city_size_distribution.csv`).
  - Country selections are constrained to SSA (per `WB_Classification.csv`).

### 4.6 JMP (Water and Sanitation — Urban)
- Scripts: `scripts/clean_JMP_water_data.py`, `scripts/clean_JMP_sanitation_data.py`
- Steps:
  1. Load JMP urban ladder data from `data/raw/jmp_*` (water and sanitation).
  2. Map to JMP service ladders for urban populations (e.g., safely managed, basic, limited, unimproved; and surface water for drinking water where applicable).
  3. Output tidy country-year shares for each service level category under `data/processed/jmp_water/` and `data/processed/jmp_sanitation/`.
- Metrics:
  - Values are typically percentages of the urban population by service level; categories may sum to ~100% subject to data availability.

## 5) Figure-specific Methods

This section explains how each chart uses the processed data. Unless otherwise noted, figures use SSA country series and (optional) benchmark overlays.

### 5.1 Historical Disasters (EM-DAT)
- Overview by Type: share or count of `Number of Events` by `Disaster Type` over the selected period; optionally stacked/100% bar.
- Disasters by Year: annual time series of `Number of Events` summed across types or filtered by type.
- Total Affected Population: annual `Total Affected` time series; unit is persons.
- Total Deaths: annual `Total Deaths` time series; unit is persons.
- Filters/Notes:
  - Country filter applies by ISO; when a country is selected, only that ISO is used.
  - If the analysis period is configured (e.g., starting year), series are truncated accordingly.

### 5.2 Historical Urbanization (WDI, UN DESA)
- Urban Population Projections (UN DESA):
  - Central (median) projection series for urban population levels, with lower/upper uncertainty bands when available.
  - Growth-rate mode displays annualized CAGR computed from 5-year steps using the formula above.
- Urbanization Rate (WDI):
  - Urban share of total population (indicator configured in `urbanization_indicators_selection.csv`).
  - Benchmarks: SSA/AFE/AFW (and optionally global regions) shown as reference series when selected.
- Urban Population Living in Slums (WDI):
  - Share of urban population living in slum households (as defined by WDI/UN-Habitat).
  - Benchmarks available where WDI publishes regional series.
- Access to Electricity, Urban (WDI):
  - Urban population with access to electricity (indicator as defined in `urbanization_indicators_selection.csv`, typically EG.ELC.ACCS.UR.ZS).
  - Plotted as a percent of urban population; benchmark overlays available.
- GDP vs Urbanization (WDI):
  - Cross-section scatter using latest common year for: GDP per capita and urbanization rate.
  - Indicator codes are configured in `urbanization_indicators_selection.csv` (e.g., GDP per capita constant USD and urban share).
  - Benchmarks: selectable set of global regions for context.
- Cities Distribution & Evolution (Africapolis × GHSL):
  - Distribution: composition of urban population by city size classes in a target year; treemap or bar representation.
  - Evolution: stacked series showing how shares by city size class change over time.

### 5.3 Exposure to Flood Hazard (Fathom3 × GHSL)
- Built-up Absolute: total built-up area exposed by return period and hazard type.
- Built-up Relative: exposed built-up share of total built-up area.
- Population Absolute: total population exposed by return period and hazard type.
- Population Relative: exposed population share of total population.
- Controls:
  - Hazard type selector (e.g., fluvial or pluvial) and return period selector.
  - Benchmarks (SSA/AFE/AFW) can be shown to compare a country against regional levels.

## 6) Benchmarks and Aggregation

- Regional benchmarks (SSA/AFE/AFW) and global regions are presented where source data publishes region series (e.g., WDI provides region aggregates).
- Where region series are not directly available (e.g., derived metrics), aggregation follows metric-consistent rules:
  - Sums for counts/totals (e.g., exposed population totals).
  - Weighted averages for rates/shares using appropriate denominators (e.g., population-weighting for shares).
- Names and codes of regions are standardized; colors are a presentation choice and not part of the methodology.

## 7) Computation Notes and Formulas

- Annualized growth rate (CAGR):
  $$\text{CAGR}_{t,k} = \left(\frac{V_t}{V_{t-k}}\right)^{\frac{1}{k}} - 1$$
- Relative exposure shares:
  $$\text{Relative Exposure} = \frac{\text{Exposed}}{\text{Total Baseline}}$$
- Cross-section alignment:
  - For scatter plots (e.g., GDP vs Urbanization), a “latest common year” across involved indicators is used to minimize missingness bias.
- Missing data:
  - Unless otherwise stated, series are used as published by sources. No interpolation/smoothing is applied by default in the processed files displayed.

## 8) Quality Assurance

- ISO3 harmonization: all country series are aligned to `WB_Classification.csv`.
- SSA filter: country lists and region membership come from the same classification file.
- Schema checks: processed files follow tidy, consistent column names noted above.
- Sanity checks:
  - Disasters: totals and event counts inspected for expected temporal patterns.
  - WDI/JMP: percentage ladders checked to be within [0, 100] and to sum to ~100 when categories are exhaustive.
  - Flood exposure: relative exposure confined to [0, 1] domain given totals.

## 9) Limitations

- EM-DAT underreporting may vary by country/year; changes in reporting standards can affect time series comparability.
- WDI timeliness and revisions: late revisions can introduce breaks; region aggregates may not exactly equal the sum of country series due to WDI regional methodology.
- UN DESA projections carry model and assumption uncertainty; only central scenarios are emphasized with bands when available.
- Flood hazard modeling (Fathom3) is an approximation of real-world processes; exposure estimates depend on hazard, exposure, and baseline data quality.
- GHSL and Africapolis definitions of urban areas/agglomerations may differ from national definitions.
- JMP ladder categories sometimes do not sum to 100% due to missingness or definitional changes in some years.

## 10) Reproducibility and Updates

- Raw data location: `data/raw/` (not tracked in version control for size/licensing).
- Processing scripts: see `scripts/` directory (named by source, e.g., `clean_*`, `process_*`).
- Processed outputs: `data/processed/` — charts and downloads read from these files.
- Country/indicator definitions: `data/Definitions/`.
- Update cadence: when sources update, re-run scripts to regenerate processed outputs; version and date this note accordingly.

## 11) Downloads

- Each chart includes a “Download data” button that returns the underlying processed dataset used for that visualization.
- Downloads are provided in CSV format; filenames indicate the chart/indicator and (when relevant) the selected country/region context.
- The intent is to provide the processed dataset “as used” in the chart without additional ad hoc filtering or smoothing beyond the pipeline.

## 12) Glossary (selected)

- Affected (EM-DAT): persons requiring immediate assistance during a period of emergency; see EM-DAT documentation for precise definition.
- Built-up (GHSL): spatial footprint of built structures derived from remote sensing; used as exposure baseline.
- CAGR: compounded annual growth rate between two points in time.
- Return period (flood): average recurrence interval (years) associated with a flood magnitude; inverse of exceedance probability.
- Slum households (WDI/UN-Habitat): as defined by UN-Habitat; see WDI metadata.
- Urbanization rate: share of population living in urban areas (WDI definition).

---

Contacts: For questions about data processing, please refer to the repository’s `scripts/` and `data/Definitions/` folders or reach out to the maintainers.