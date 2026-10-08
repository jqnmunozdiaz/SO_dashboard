import pandas as pd

# Load data and classifications directly
df = pd.read_csv('data/processed/WUP/WUP2025_urban_projections_consolidated.csv')
wb = pd.read_csv('data/Definitions/WB_Classification.csv')

# Get SSA countries
ssa_df = wb[wb['Region Code'] == 'SSA']
ssa_countries = dict(zip(ssa_df['ISO3'], ssa_df['Country']))

# Filter and pivot
urban = df[
    (df['ISO3'].isin(ssa_countries.keys())) & 
    (df['indicator'] == 'urban_pop_median') & 
    (df['year'].isin([2025, 2050]))
]
pivoted = urban.pivot(index='ISO3', columns='year', values='value')

# Calculate CAGR and rank
pivoted['cagr'] = (pivoted[2050] / pivoted[2025]) ** (1 / 25) - 1
pivoted['country'] = pivoted.index.map(ssa_countries)
ranked = pivoted.sort_values(by='cagr', ascending=False).reset_index()
ranked['rank'] = ranked.index + 1

# Print results
print(ranked[['rank', 'ISO3', 'country', 2025, 2050, 'cagr']])

# Report text for Burkina Faso
bfa = ranked[ranked['ISO3'] == 'BFA'].iloc[0]
report_text = (
    f"\nReport Text:\n"
    f"Between 2025 and 2050, the urban population of Burkina Faso is projected to grow "
    f"from {bfa[2025]:.2f} million to {bfa[2050]:.2f} million, representing a Compound "
    f"Annual Growth Rate (CAGR) of {bfa['cagr']*100:.2f}%. This ranks Burkina Faso "
    f"{int(bfa['rank'])}th out of {len(ranked)} Sub-Saharan African countries in terms "
    f"of projected urban population growth rate."
)
print(report_text)

