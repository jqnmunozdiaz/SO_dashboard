#%% Plot
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
# Directories
processed_dir = os.path.join(project_root, 'data', 'processed') + os.sep

fyear = 2050
RPs = [10, 100] # Return periods to analyze
var_name = '1day'

ISO3 = 'BFA'

df = pd.read_csv(processed_dir + f'ReturnPeriods-1day-clean.csv')
df = df[(df['ISO3'] == ISO3) & (df['year'] == fyear) & (df['RP'].isin(RPs))]

#%%
fig, axs = plt.subplots(len(RPs), 1, figsize = (6, 2), dpi = 300)
axs[0].scatter([None], [None], marker='x', color = 'black', zorder = 3, alpha = 1, s = 6, label = 'Today')
xfin = df['mult'].max()
for j, ax in enumerate(axs):
    rp = RPs[j]
    ep = 1/rp
    dft = df[df['RP'] == rp]
    dft = dft.set_index('SSP')
    ax.plot([min(dft['Future_EP']), max(dft['Future_EP'])], [0, 0], marker='|', color = '#DEDEDE', zorder = 3, alpha = 1, lw = 2)
    ax.scatter(ep, 0, marker='x', color = 'black', zorder = 10, alpha = 1, s = 20, clip_on=False)
    for i, ssp in enumerate(df['SSP'].unique()):         
        ax.scatter(dft.at[ssp, 'Future_EP'], 0, marker = 'o', zorder = 4, s = 20, clip_on=False)
        if j == 0:
            ax.scatter([None], [None], marker = 'o', s = 6, label = ssp)
    ax.set_xlim(ep, ep*xfin)
    ax.set_xticklabels(list(ax.get_xticks()), size = 10)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1, decimals = 1))
    ax.spines[['left', 'right', 'top']].set_visible(False)
    ax.set_yticks([-0.2, 0, 0.4])
    ax.set_yticklabels(['', f'{rp}-year', ''], fontsize = 10)
    ax.tick_params(axis='both', which='both', bottom=True, top=False, left=False, right=False, direction = 'out')
    ax.tick_params(axis='y', pad=10)  # Add space between y-axis and y labels

axs[-1].set_xlabel('Annual exceedance probability', fontsize = 11) # Probabilité annuelle de dépassement
plt.tight_layout()
legend = axs[0].legend(ncols = 1, loc = 'center', bbox_to_anchor=(1.15, -0.8), handletextpad=0, fontsize = 9, frameon = False, labelspacing = 1.2)
for handle in legend.legend_handles: handle.set_sizes([20])  # Adjust the value (100 in this example) to change the legend symbol size
