"""
Script to plot Burkina Faso's Urban and Rural Population Projections
and dynamically print summarized data for publications.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
data_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_urban_projections_consolidated.csv')
filename = "Burkina_Faso_Population_Projections.png"
    
print(f"Loading data from: {data_path}")

# 2. Load and filter data for Burkina Faso (BFA)
df = pd.read_csv(data_path)
bfa_data = df[df['ISO3'] == 'BFA'].copy()

# Pivot to get years as index and indicators as columns
bfa_pivot = bfa_data.pivot(index='year', columns='indicator', values='value')

# Define year ranges
past_years = list(range(1975, 2030, 5))    # Includes 2025
future_years = list(range(2025, 2055, 5))  # Includes 2025

# 3. Plotting function supporting English and French
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

translations = {
    'en': {
        'xlabel': "Year",
        'ylabel': "Population (millions)",
        'historical': "Historical",
        'projections': "Projections",
        'urban_pop': "Urban Population",
        'rural_pop': "Rural Population",
        'ci_95': "95% Confidence Interval",
        'ci_80': "80% Confidence Interval",
        'filenames': ["Burkina_Faso_Population_Projections.png", "Burkina_Faso_Population_Projections_EN.png"]
    },
    'fr': {
        'xlabel': "Année",
        'ylabel': "Population (millions)",
        'historical': "Historique",
        'projections': "Projections",
        'urban_pop': "Population urbaine",
        'rural_pop': "Population rurale",
        'ci_95': "Intervalle de confiance à 95 %",
        'ci_80': "Intervalle de confiance à 80 %",
        'filenames': ["Burkina_Faso_Population_Projections_FR.png"]
    }
}

colors = {
    'urban': '#1f77b4',  # Medium Blue
    'rural': '#2ca02c'   # Medium Green
}

for lang, t in translations.items():
    fig, ax = plt.subplots(figsize=(3, 2.4), dpi=600)

    for aoi in ['urban', 'rural']:
        lower95_col = f'{aoi}_pop_lower95'
        upper95_col = f'{aoi}_pop_upper95'
        lower80_col = f'{aoi}_pop_lower80'
        upper80_col = f'{aoi}_pop_upper80'
        median_col = f'{aoi}_pop_median'
        historical_col = f'wup_{aoi}_pop'
            
        # Draw uncertainty bands (95% CI)
        lowers_95 = bfa_pivot.loc[future_years, lower95_col].values
        uppers_95 = bfa_pivot.loc[future_years, upper95_col].values
        ax.fill_between(future_years, lowers_95, uppers_95, color=colors[aoi], alpha=0.15, 
                        edgecolor='none')
                
        # Draw uncertainty bands (80% CI)
        lowers_80 = bfa_pivot.loc[future_years, lower80_col].values
        uppers_80 = bfa_pivot.loc[future_years, upper80_col].values
        ax.fill_between(future_years, lowers_80, uppers_80, color=colors[aoi], alpha=0.3, 
                        edgecolor='none')
                
        # Draw Historical Line (solid)
        hist_vals = bfa_pivot.loc[past_years, historical_col].values
        ax.plot(past_years, hist_vals, linewidth=1.2, 
                color=colors[aoi])
                
        # Draw Projections Line (dashed)
        proj_vals = bfa_pivot.loc[future_years, median_col].values
        ax.plot(future_years, proj_vals, linewidth=1.2, linestyle='--',
                color=colors[aoi])
                
    # 4. Styling & Customization
    ax.axvline(x=2025, color='gray', linestyle=':', alpha=0.7, linewidth=0.8)

    # Y-axis limit check & grid setup
    ax.set_ylim(0, 25)
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.grid(True, linestyle='-', alpha=0.2, linewidth=0.4)

    # Hide the last gridline (at y=25)
    gridlines = ax.yaxis.get_gridlines()
    if len(gridlines) > 0:
        gridlines[-1].set_visible(False)

    ax.set_xlabel(t['xlabel'], fontsize=7, fontweight='bold', labelpad=4)
    ax.set_ylabel(t['ylabel'], fontsize=7, fontweight='bold', labelpad=4)
    ax.set_xlim(1975, 2050)
    ax.set_xticks([1975, 2000, 2025, 2050])
    ax.tick_params(axis='both', which='both', length=0, labelsize=6, pad=2)

    # Hide the vertical gridline at x=2025 (3rd tick, index 2)
    x_gridlines = ax.xaxis.get_gridlines()
    if len(x_gridlines) > 2:
        x_gridlines[2].set_visible(False)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Annotations for Historical vs Projections
    y_min, y_max = ax.get_ylim()
    y_text = y_max
    ax.text(2024, y_text, t['historical'], color='gray', fontsize=6, fontweight='bold', ha='right', va='bottom')
    ax.text(2026, y_text, t['projections'], color='gray', fontsize=6, fontweight='bold', ha='left', va='bottom')

    # Publication legend
    legend_elements = [
        Line2D([0], [0], color='#1f77b4', lw=1.5, label=t['urban_pop']),
        Line2D([0], [0], color='#2ca02c', lw=1.5, label=t['rural_pop']),
        Patch(facecolor='gray', alpha=0.15, edgecolor='none', label=t['ci_95']),
        Patch(facecolor='gray', alpha=0.3, edgecolor='none', label=t['ci_80'])
    ]
    leg = ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=True, facecolor='white', framealpha=1.0,
              fontsize=4.8 if lang == 'fr' else 5, borderpad=0.4, labelspacing=0.4, handletextpad=0.4, handlelength=1.2)
    leg.get_frame().set_linewidth(0.4)

    # Save the figure in configured filenames
    plt.tight_layout()
    for fname in t['filenames']:
        out_path = os.path.join(script_dir, fname)
        plt.savefig(out_path, dpi=600, bbox_inches='tight')
        print(f"Successfully saved figure ({lang.upper()}) to: {out_path}")
    plt.close()

# 5. Dynamic Report Text Generation in both English and French
u_25 = bfa_pivot.loc[2025, 'wup_urban_pop'] if 'wup_urban_pop' in bfa_pivot.columns else bfa_pivot.loc[2025, 'urban_pop_median']
u_50_med = bfa_pivot.loc[2050, 'urban_pop_median']
u_50_l80 = bfa_pivot.loc[2050, 'urban_pop_lower80']
u_50_u80 = bfa_pivot.loc[2050, 'urban_pop_upper80']
u_50_l95 = bfa_pivot.loc[2050, 'urban_pop_lower95']
u_50_u95 = bfa_pivot.loc[2050, 'urban_pop_upper95']

report_text_en = f"""
================================================================================
Burkina Faso Urban Population Projections Summary (2025-2050) [EN]:
--------------------------------------------------------------------------------
In 2025, Burkina Faso’s urban population is estimated at {u_25:.1f} million. According to the median projection scenario, 
this figure is expected to reach {u_50_med:.1f} million by 2050, representing an absolute increase of {u_50_med - u_25:.1f} million people, 
or a relative growth of {((u_50_med - u_25)/u_25)*100:.1f}%. Under the 80% confidence interval, the urban population by 2050 is projected to 
range between {u_50_l80:.1f} million (a {((u_50_l80 - u_25)/u_25)*100:.1f}% relative increase) and {u_50_u80:.1f} million (a {((u_50_u80 - u_25)/u_25)*100:.1f}% increase). 
Under the wider 95% confidence interval, the 2050 urban population is projected to range between {u_50_l95:.1f} million (a {((u_50_l95 - u_25)/u_25)*100:.1f}% relative increase) 
and {u_50_u95:.1f} million (a {((u_50_u95 - u_25)/u_25)*100:.1f}% increase).
"""

report_text_fr = f"""
================================================================================
Résumé des projections de la population urbaine du Burkina Faso (2025-2050) [FR] :
--------------------------------------------------------------------------------
En 2025, la population urbaine du Burkina Faso est estimée à {u_25:.1f} millions d'habitants. Selon le scénario de projection médian,
ce chiffre devrait atteindre {u_50_med:.1f} millions d'ici 2050, représentant une augmentation absolue de {u_50_med - u_25:.1f} millions de personnes,
soit une croissance relative de {((u_50_med - u_25)/u_25)*100:.1f} %. Selon l'intervalle de confiance à 80 %, la population urbaine d'ici 2050 devrait
se situer entre {u_50_l80:.1f} millions (une hausse relative de {((u_50_l80 - u_25)/u_25)*100:.1f} %) et {u_50_u80:.1f} millions (une hausse de {((u_50_u80 - u_25)/u_25)*100:.1f} %).
Selon l'intervalle de confiance plus large à 95 %, la population urbaine en 2050 devrait se situer entre {u_50_l95:.1f} millions (une hausse relative de {((u_50_l95 - u_25)/u_25)*100:.1f} %)
et {u_50_u95:.1f} millions (une hausse de {((u_50_u95 - u_25)/u_25)*100:.1f} %).
================================================================================
"""

print(report_text_en)
print(report_text_fr)
