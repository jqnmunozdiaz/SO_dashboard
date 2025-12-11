# Methodological Note: Sub-Saharan Africa DRM Dashboard

**Last Updated:** November 2025

## Overview
This dashboard integrates data from multiple authoritative sources to provide a comprehensive view of disaster risk, urbanization trends, and climate exposure in Sub-Saharan Africa. This note details the data sources, processing methodologies, and known limitations for each component of the dashboard. Users should be aware that, because the dashboard draws on multiple data sources, some estimates may not align perfectly.

---

## 1. Historical Disasters

### Data Source
*   **Source:** [EM-DAT (The International Disaster Database)](https://www.emdat.be/), Centre for Research on the Epidemiology of Disasters (CRED).
*   **Access Date:** October 2025.

### Methodology
*   **Scope:** The analysis includes all Sub-Saharan African countries (as defined by the World Bank).
*   **Disaster Types:** Filtered to include only relevant natural hazard categories (e.g., Drought, Flood, Storm, Earthquake, Landslide, Wildfire, Extreme Temperature).
*   **Metrics:**
    *   **Total Deaths:** Number of people who lost their lives.
    *   **Total Affected:** Sum of injured, homeless, and affected populations.
    *   **Frequency:** Number of reported disaster events.
*   **Regional Aggregation:** Data is aggregated into three regions:
    *   **SSA:** Sub-Saharan Africa (Total)
    *   **AFE:** Eastern and Southern Africa
    *   **AFW:** Western and Central Africa

### Limitations
*   **Reporting Bias:** EM-DAT relies on reporting from various agencies. Smaller events, particularly in remote areas, may be underreported.
*   **Economic Damages:** Economic damage data is often missing or incomplete for African countries and is therefore excluded from some visualizations to avoid misleading comparisons.
*   **Thresholds:** EM-DAT includes events that meet at least one of the following criteria: 10+ deaths, 100+ affected, declaration of a state of emergency, or call for international assistance. Smaller events are excluded.

---

## 2. Historical Urbanization

### 2.1 Urban Population & Projections
*   **Source:** United Nations Department of Economic and Social Affairs (UN DESA).
    *   **Population:** [World Population Prospects (WPP) 2024](https://population.un.org/wpp/).
    *   **Urbanization Rates:** [World Urbanization Prospects (WUP) 2025](https://population.un.org/wup/).
*   **Methodology:**
    *   Urban population is calculated by applying WUP urbanization rates to WPP total population estimates.
    *   **Uncertainty Bands:** The dashboard presents probabilistic projections (Median, 80% prediction interval, 95% prediction interval) to reflect demographic uncertainty.
    *   **Rural Population:** Derived as the residual of Total Population minus Urban Population.

### 2.2 Urbanization Indicators (WDI)
*   **Source:** [World Development Indicators (WDI)](https://databank.worldbank.org/source/world-development-indicators), World Bank.
*   **Indicators Included:**
    *   Urban population (% of total)
    *   Population living in slums (% of urban population)
    *   Access to electricity (% of urban population)
    *   GDP per capita (current US$)
*   **Benchmarking:** Country values are compared against regional aggregates (SSA, AFE, AFW) and global benchmarks (e.g., East Asia & Pacific, Latin America & Caribbean) derived directly from WDI regional data.

### 2.3 City Size Distribution
*   **Source:** [Africapolis](https://africapolis.org/) (OECD/SWAC).
*   **Methodology:**
    *   Utilizes the comprehensive database of urban agglomerations in Africa defined by spatial continuity of built-up areas.
    *   Agglomerations are classified by population size to analyze the distribution of urban settlements across the region.
    *   Africapolis provides a more granular view of the urban system compared to traditional sources, capturing small and medium-sized towns often omitted in global datasets.

### 2.4 Urban Density
*   **Sources:**
    *   **Population:** [Africapolis](https://africapolis.org/) (OECD/SWAC), 2023 update.
    *   **Built-up Area:** [Global Human Settlement Layer (GHSL)](https://ghsl.jrc.ec.europa.eu/), GHS-BUILT-S R2023A.
*   **Methodology:**
    *   Data is matched at the urban agglomeration level.
    *   **Metric:** Built-up Area per Capita (m² per person) = Total Built-up Area / Total Population.
    *   **Aggregation:** Agglomeration-level data is summed to produce national and regional averages.
*   **Note:** This metric reflects the physical footprint of cities relative to their population, serving as a proxy for urban density and land consumption efficiency.

### 2.5 Cities Growth
*   **Sources:**
    *   **Population:** [Africapolis](https://africapolis.org/) (OECD/SWAC).
    *   **Built-up Area:** [WorldPop](https://www.worldpop.org/), computed based on Africapolis extents.
*   **Methodology:**
    *   Built-up area values were derived by aggregating WorldPop built-up layers within the urban extents defined by Africapolis.

---

## 3. Flood Exposure (Current)

### Data Sources
*   **Flood Hazard:** [Fathom 3.0](https://www.fathom.global/) Global Flood Map (30m resolution).
    *   **Types:** Fluvial (riverine) and Pluvial (surface water).
    *   **Defenses:** Assumes "Defended" scenario (flood protection infrastructure is active where present).
*   **Exposure Layer:** [Global Human Settlement Layer (GHSL)](https://ghsl.jrc.ec.europa.eu/) 2023.
    *   **Population:** GHS-POP.
    *   **Built-up Area:** GHS-BUILT-S.

### Methodology
*   **Intersection:** Flood hazard maps are intersected with population and built-up area layers.
*   **Metrics:**
    *   **Absolute Exposure:** Total population or built-up area (km²) located within the flood extent.
    *   **Relative Exposure:** Percentage of the total national population or built-up area located within the flood extent.
*   **Regional Aggregation:** Country-level exposure is summed to generate regional totals (SSA, AFE, AFW).

---

## 4. Future Flood Risk Projections

### 4.1 Urbanization vs. Climate Change
This analysis decomposes future flood risk into two drivers: **Climate Change** (changing hazard) and **Urbanization** (changing exposure).

*   **Baseline (2020):** Fathom 3.0 flood hazard intersected with GHSL 2020 built-up area.
*   **Projection Horizon:** 2050.
*   **Urbanization Scenario:**
    *   **Assumption:** "Constant Built-up Per Capita". Future built-up area is projected by multiplying UN WPP 2024 population projections by the country's 2020 built-up per capita rate.
    *   **Rationale:** This assumes that future urban expansion will follow current land consumption patterns.
*   **Climate Scenarios (SSPs):**
    *   Shared Socioeconomic Pathways (SSPs) from CMIP6 models are used to project future flood hazards:
        *   **SSP1-2.6:** Sustainability (Low emissions)
        *   **SSP2-4.5:** Middle of the Road (Intermediate emissions)
        *   **SSP3-7.0:** Regional Rivalry (High emissions)
        *   **SSP5-8.5:** Fossil-fueled Development (Very high emissions)
*   **Methodology:**
    *   Future exposure is estimated using a regression model that relates built-up area growth to flood exposure growth.
    *   The results compare the increase in exposure due solely to urban growth (holding climate constant) vs. the additional impact of climate change.

### 4.2 Extreme Precipitation Changes
*   **Source:** [World Bank Climate Change Knowledge Portal (CCKP)](https://climateknowledgeportal.worldbank.org/).
*   **Methodology:**
    *   Analyzes projected changes in the magnitude of 1-day and 5-day extreme rainfall events.
    *   Compares historical return periods (e.g., a 1-in-100 year event) with their projected future frequency under different SSP scenarios.

---

## 5. General Definitions

### Regions
*   **SSA (Sub-Saharan Africa):** Includes all 48 countries defined as Sub-Saharan Africa by the World Bank.
*   **AFE (Eastern and Southern Africa):** A World Bank operational region comprising 26 countries (e.g., Kenya, South Africa, Ethiopia, DRC).
*   **AFW (Western and Central Africa):** A World Bank operational region comprising 22 countries (e.g., Nigeria, Ghana, Senegal).
