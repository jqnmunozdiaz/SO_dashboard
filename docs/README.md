# Sub-Saharan Africa Disaster Risk Management Dashboard

A comprehensive Dash-based dashboard for visualizing and analyzing disaster risk data across Sub-Saharan African countries, including historical disasters, urbanization trends, and flood risk assessments.

## Features

- **Historical Disasters Analysis**: Interactive visualizations of past disaster events, patterns, and impacts
- **Urbanization Trends**: Population growth and urban development indicators over time
- **Flood Risk Assessment**: Current and projected flood risk maps and statistics
- **Country Comparisons**: Side-by-side analysis of different Sub-Saharan African countries
- **Interactive Maps**: Geospatial visualizations with country-level detail

## Project Structure

```
SO_dashboard/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── config/                  # Configuration files
├── data/                    # Data storage
│   ├── raw/                 # Original, unprocessed data
│   ├── processed/           # Cleaned and transformed data
│   └── external/            # External API data cache
├── src/                     # Source code
│   ├── components/          # Reusable Dash components
│   ├── layouts/             # Page layouts
│   ├── callbacks/           # Interactive callback functions
│   └── utils/               # Utility functions and data processing
├── assets/                  # Static assets
│   ├── css/                 # Custom stylesheets
│   └── images/              # Images and icons
├── notebooks/               # Jupyter notebooks for analysis
├── scripts/                 # Data processing and utility scripts
└── tests/                   # Unit and integration tests
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SO_dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the dashboard:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:8050`

## Data Sources

- **Historical Disasters**: EM-DAT (Emergency Events Database)
- **Urbanization Data**: World Bank Urban Development Indicators
- **Flood Risk Data**: World Bank Climate Change Knowledge Portal
- **Geospatial Data**: Natural Earth, OpenStreetMap

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.