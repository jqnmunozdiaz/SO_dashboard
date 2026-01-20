# Data Directory

This folder contains processed data files used by the SO Dashboard.

## Directory Structure

```
data/
├── processed/          # Clean, ready-to-use data files
├── raw/                # Original source data (if any)
└── Definitions/        # Reference/lookup tables
```

---

## Processed Data Files

### Disaster Data (EM-DAT)

| File | Description | Used By |
|------|-------------|---------|
| `african_disasters_emdat.csv` | Historical disaster events from EM-DAT database | All Disaster tab subtabs |

---

### Population & Urbanization Data

| File | Description | Used By |
|------|-------------|---------|
| `WPP2024_Total_Population.csv` | Total population by country (WPP2024) | Population projections |
| `WUP/WUP2025_*.csv` | World Urbanization Prospects 2025 projections | Population, Urbanization Level tabs |
| `UNDESA_Country/` | UN DESA country-level data | Older population visualizations |

---

### World Bank WDI Indicators

Location: `wdi/`

| File | Indicator | Used By |
|------|-----------|---------|
| `SP.URB.TOTL.IN.ZS.csv` | Urban population (% of total) | GDP vs Urbanization |
| `EN.POP.SLUM.UR.ZS.csv` | Population living in slums (%) | Population Living in Slums |
| `EG.ELC.ACCS.UR.ZS.csv` | Access to electricity, urban (%) | Access to Electricity |
| `NY.GDP.PCAP.PP.CD.csv` | GDP per capita (PPP) | GDP vs Urbanization |

---

### JMP WASH Data

| Folder | Description | Used By |
|--------|-------------|---------|
| `jmp_water/` | Urban drinking water access | Access to Drinking Water |
| `jmp_sanitation/` | Urban sanitation access | Access to Sanitation |

---

### City-Level Data (Africapolis + GHSL)

| File | Description | Used By |
|------|-------------|---------|
| `africapolis_worldpop_final_merged.csv` | Africapolis cities with WorldPop population | Cities Evolution, Cities Growth |
| `africapolis_ghsl_simple.csv` | Africapolis cities with GHSL built-up (2000-2020) | Built-up per capita in Cities |
| `africapolis2024_centroids.csv` | City coordinates for mapping | City maps |
| `agglomeration_population_builtup_merged.csv` | Agglomeration data with population/built-up | Cities Distribution |
| `cities_individual.csv` | Individual city records | City dropdown lists |
| `built_up_per_capita_m2_by_country_year.csv` | National built-up per capita | Built-up per capita tab |

---

### Flood Exposure Data

Location: `flood/`

| File | Description | Used By |
|------|-------------|---------|
| `Flood_exposure_*.csv` | Fathom3 flood exposure by return period (1in5, 1in10, 1in100) | Flood Exposure tabs |

Data combines:
- **Fathom3**: Flood hazard maps (fluvial + pluvial, defended/undefended)
- **GHSL**: Built-up area and population grids

---

### Climate Projections

| File | Description | Used By |
|------|-------------|---------|
| `ReturnPeriods-1day-clean.csv` | Precipitation return period projections from CCKP | Precipitation tab |
| `ALL_SSA_BUexp_projected_consolidated.csv` | Future flood exposure projections | Urbanization vs Climate Change |

---

## Data Sources Reference

| Source | Acronym | Website |
|--------|---------|---------|
| Emergency Events Database | EM-DAT | emdat.be |
| World Development Indicators | WDI | data.worldbank.org |
| World Urbanization Prospects | WUP | population.un.org |
| World Population Prospects | WPP | population.un.org |
| JMP Water & Sanitation | JMP | washdata.org |
| Africapolis | - | africapolis.org |
| Global Human Settlement Layer | GHSL | ghsl.jrc.ec.europa.eu |
| Fathom Global Flood Data | Fathom3 | fathom.global |
| Climate Change Knowledge Portal | CCKP | climateknowledgeportal.worldbank.org |
