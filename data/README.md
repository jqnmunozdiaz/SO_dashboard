# Data directories

## raw/
Contains original, unprocessed data files from various sources:
- EM-DAT disaster database exports
- World Bank urbanization indicators
- Climate data from World Bank Climate Change Knowledge Portal
- Geospatial boundary files

## processed/
Contains cleaned and standardized data files ready for dashboard use:
- disasters.csv: Processed historical disaster data
- urbanization.csv: Urban development indicators
- flood_risk.csv: Flood risk assessments and projections

## external/
Contains data from external APIs and cached responses:
- Country boundary files (GeoJSON)
- API response caches
- Third-party data sources

## Data Sources

### Historical Disasters
- **Source**: EM-DAT (Emergency Events Database)
- **URL**: https://www.emdat.be/
- **Coverage**: 1900-present
- **Variables**: Disaster type, date, location, deaths, injuries, affected population, economic damage

### Urbanization Trends  
- **Source**: World Bank Open Data
- **URL**: https://data.worldbank.org/
- **Indicators**:
  - SP.URB.TOTL.IN.ZS: Urban population (% of total)
  - SP.URB.GROW: Urban population growth (annual %)
  - EN.POP.DNST: Population density (people per sq. km of land area)

### Flood Risk Data
- **Source**: World Bank Climate Change Knowledge Portal
- **URL**: https://climateknowledgeportal.worldbank.org/
- **Coverage**: Current and projected flood risk scenarios (2030, 2050)
- **Variables**: Risk level, exposure, sensitivity, adaptive capacity

### Geospatial Data
- **Source**: Natural Earth
- **URL**: https://www.naturalearthdata.com/
- **Files**: Country boundaries, admin boundaries for Sub-Saharan Africa