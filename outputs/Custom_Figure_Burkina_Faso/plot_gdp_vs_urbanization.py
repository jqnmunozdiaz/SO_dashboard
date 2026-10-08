import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
gdp_path = os.path.join(project_root, 'data', 'processed', 'wdi', 'NY.GDP.PCAP.PP.KD.csv')
urb_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_National_Definitions_Population_processed_pivoted.csv')
filename = "Burkina_Faso_GDP_vs_Urbanization.png"

print("Loading data...")
gdp_df = pd.read_csv(gdp_path)
urb_df = pd.read_csv(urb_path)

# Region configuration
region_configs = {
    'SSA': {'name': 'Sub-Saharan Africa', 'color': '#6c757d'},      # Cool Grey
    'AFW': {'name': 'Western and Central Africa', 'color': '#27ae60'}, # Green
    'SAS': {'name': 'South Asia', 'color': '#9b5de5'},               # Purple
    'TSA': {'name': 'South Asia', 'color': '#9b5de5'},
    'MLI': {'name': 'Mali', 'color': '#c3a339'},                     # Deep Olive Gold
    'ETH': {'name': 'Ethiopia', 'color': '#2b6cb0'}                  # Blue
}

# Helper function to plot line with constant color, including start and end markers
def plot_trajectory_line(ax, x, y, base_color, linewidth=1.0, linestyle='-', zorder=3):
    if len(x) < 2:
        return
    # Plot line with constant color
    ax.plot(x, y, color=base_color, linewidth=linewidth, linestyle=linestyle, zorder=zorder)
    
    # Add start marker (circle with white center) and end marker (solid circle)
    ax.plot(x[0], y[0], marker='o', markerfacecolor='white', markeredgecolor=base_color, markeredgewidth=0.6, markersize=2.0, zorder=zorder+1, linestyle='None')
    ax.plot(x[-1], y[-1], marker='o', color=base_color, markersize=2.0, zorder=zorder+1, linestyle='None')

# Helper function to get merged trajectory
def get_trajectory(iso):
    # Map codes if necessary (WDI GDP uses TSA, UN DESA WUP uses SAS)
    wdi_to_wup = {
        'EAS': 'EAP',
        'ECS': 'ECA',
        'MEA': 'MENA',
        'TSA': 'SAS'
    }
    gdp_iso = iso
    urb_iso = wdi_to_wup.get(iso, iso)

    gdp = gdp_df[gdp_df['Country Code'] == gdp_iso]
    urb = urb_df[urb_df['ISO3_Code'] == urb_iso].copy()
    if urb.empty or gdp.empty:
        return pd.DataFrame()
        
    urb['Year'] = urb['Year'].astype(int)
    # Convert urbanization rate from proportion (0-1) to percentage (0-100)
    urb['Value_urb'] = urb['Urbanization_Rate'] * 100.0
    
    merged = pd.merge(urb, gdp, on='Year')
    merged = merged.rename(columns={'Value': 'Value_gdp'})
    return merged.sort_values('Year')

bfa_data = get_trajectory('BFA')

# Translations configuration
translations = {
    'en': {
        'xlabel': "Share of population living in urban areas\n(national definition, %)",
        'ylabel': "GDP per capita\n(constant 2017 international dollars)",
        'bfa_label': "Burkina Faso",
        'start_label': "Start (1990)",
        'end_label': "End (2024)",
        'regions': {
            'SSA': 'Sub-Saharan Africa',
            'AFW': 'Western and Central Africa',
            'SAS': 'South Asia',
            'TSA': 'South Asia',
            'MLI': 'Mali',
            'ETH': 'Ethiopia'
        },
        'filenames': ["Burkina_Faso_GDP_vs_Urbanization.png", "Burkina_Faso_GDP_vs_Urbanization_EN.png"]
    },
    'fr': {
        'xlabel': "Part de la population vivant en zone urbaine\n(définition nationale, %)",
        'ylabel': "PIB par habitant\n(dollars internationaux constants de 2017)",
        'bfa_label': "Burkina Faso",
        'start_label': "Début (1990)",
        'end_label': "Fin (2024)",
        'regions': {
            'SSA': 'Afrique subsaharienne',
            'AFW': "Afrique de l'Ouest et du Centre",
            'SAS': 'Asie du Sud',
            'TSA': 'Asie du Sud',
            'MLI': 'Mali',
            'ETH': 'Éthiopie'
        },
        'filenames': ["Burkina_Faso_GDP_vs_Urbanization_FR.png"]
    }
}

for lang, t in translations.items():
    fig, ax = plt.subplots(figsize=(3, 2.4), dpi=600)

    # 3. Plot Burkina Faso (BFA)
    if not bfa_data.empty:
        plot_trajectory_line(ax, bfa_data['Value_urb'].values, bfa_data['Value_gdp'].values, '#e63946', linewidth=1.2, linestyle='-', zorder=5)

    # 4. Plot regional peers
    legend_elements = [
        Line2D([0], [0], color='#e63946', lw=1.2, label=t['bfa_label']),
        Line2D([0], [0], marker='o', color='none', markerfacecolor='white', markeredgecolor='#555555', markeredgewidth=0.6, markersize=2.0, label=t['start_label'], linestyle='None'),
        Line2D([0], [0], marker='o', color='none', markerfacecolor='#555555', markeredgecolor='none', markersize=2.0, label=t['end_label'], linestyle='None')
    ]

    plotted_base_names = set()

    for code, config in region_configs.items():
        base_name = config['name'].split(' (')[0]
        if base_name in plotted_base_names:
            continue
            
        region_data = get_trajectory(code)
        if not region_data.empty:
            plot_trajectory_line(ax, region_data['Value_urb'].values, region_data['Value_gdp'].values, config['color'], linewidth=0.7, linestyle='-', zorder=3)
            disp_name = t['regions'].get(code, config['name'])
            legend_elements.append(Line2D([0], [0], color=config['color'], lw=0.7, linestyle='-', label=disp_name))
            plotted_base_names.add(base_name)

    # 5. Styling
    ax.grid(True, linestyle='-', alpha=0.2, linewidth=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Labels and ticks
    ax.set_xlabel(t['xlabel'], fontsize=4.8, fontweight='bold', labelpad=4)
    ax.set_ylabel(t['ylabel'], fontsize=4.8, fontweight='bold', labelpad=4)
    ax.tick_params(axis='both', which='both', length=0, labelsize=4.2, pad=2)

    # Set range limits nicely
    ax.set_xlim(10, 60)
    ax.set_ylim(bottom=0, top=10000)

    ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Legend at the bottom
    leg = ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=True, 
              facecolor='white', framealpha=1.0, fontsize=4.3 if lang == 'fr' else 4.5, borderpad=0.4, labelspacing=0.4, 
              handletextpad=0.4, handlelength=2.0)
    leg.get_frame().set_linewidth(0.4)

    # Save the figure
    plt.tight_layout()
    for fname in t['filenames']:
        out_path = os.path.join(script_dir, fname)
        plt.savefig(out_path, dpi=600, bbox_inches='tight')
        print(f"Successfully saved figure ({lang.upper()}) to: {out_path}")
    plt.close()

# 6. Dynamic Report Text Generation in both English and French
if not bfa_data.empty:
    bfa_start_yr = int(bfa_data['Year'].iloc[0])
    bfa_start_urb = bfa_data['Value_urb'].iloc[0]
    bfa_start_gdp = bfa_data['Value_gdp'].iloc[0]
    bfa_end_yr = int(bfa_data['Year'].iloc[-1])
    bfa_end_urb = bfa_data['Value_urb'].iloc[-1]
    bfa_end_gdp = bfa_data['Value_gdp'].iloc[-1]

    report_gdp_en = f"""
================================================================================
Burkina Faso GDP per Capita vs Urbanization Summary ({bfa_start_yr}-{bfa_end_yr}) [EN]:
--------------------------------------------------------------------------------
Between {bfa_start_yr} and {bfa_end_yr}, Burkina Faso’s urban share of population (national definition)
increased from {bfa_start_urb:.1f}% to {bfa_end_urb:.1f}%, while real GDP per capita (constant 2017 international $)
evolved from ${bfa_start_gdp:,.0f} to ${bfa_end_gdp:,.0f}.
"""

    report_gdp_fr = f"""
================================================================================
Résumé PIB par habitant vs Urbanisation - Burkina Faso ({bfa_start_yr}-{bfa_end_yr}) [FR] :
--------------------------------------------------------------------------------
Entre {bfa_start_yr} et {bfa_end_yr}, la part de la population urbaine au Burkina Faso (définition nationale)
est passée de {bfa_start_urb:.1f} % à {bfa_end_urb:.1f} %, tandis que le PIB par habitant (dollars internationaux constants de 2017)
est passé de {bfa_start_gdp:,.0f} $ à {bfa_end_gdp:,.0f} $.
================================================================================
"""

    print(report_gdp_en)
    print(report_gdp_fr)
