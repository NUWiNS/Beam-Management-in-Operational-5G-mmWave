import numpy as np
import pickle
import matplotlib.pyplot as plt

def load_data_from_pickle(filename):
    """
    Load data from pickle file
    """
    with open(filename, 'rb') as file:
        loaded_data = pickle.load(file)
    print(f"loaded from {filename} ")
    return loaded_data

def data_to_box(group_24, group_32, group_36, group_144, link_type, save_flag, show_flag):
    # Calculate statistics
    means = [np.mean(group_24['rsrp_diffs']), np.mean(group_32['rsrp_diffs']), 
             np.mean(group_36['rsrp_diffs']), np.mean(group_144['rsrp_diffs'])]
    medians = [np.median(group_24['rsrp_diffs']), np.median(group_32['rsrp_diffs']), 
               np.median(group_36['rsrp_diffs']), np.median(group_144['rsrp_diffs'])]
    percentiles_75 = [np.percentile(group_24['rsrp_diffs'], 75), np.percentile(group_32['rsrp_diffs'], 75),
                      np.percentile(group_36['rsrp_diffs'], 75), np.percentile(group_144['rsrp_diffs'], 75)]

    # Print statistics
    print(f'{link_type} Statistics:')
    for i, label in enumerate(['24', '32', '36', '144']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    fig, ax = plt.subplots()
    
    positions = [1, 2, 3, 4]
    labels = ['24', '32', '36', '144'] 
    bp = ax.boxplot([group_24['rsrp_diffs'], group_32['rsrp_diffs'], 
                     group_36['rsrp_diffs'], group_144['rsrp_diffs']],
                    positions=positions, patch_artist=True, widths=0.6)

    for box in bp['boxes']:
        box.set_facecolor('lightgray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)

    ax.set_xticks(positions)
    ax.set_xlabel('# beams per gNB')
    ax.set_xticklabels(labels)

    ylim = (-1, 17)
    ax.set_ylim(*ylim)

    ax.set_ylabel('RSRP difference (dB)')

    ax.axvline(x=3.5, color='black', linestyle='--')

    # Print out outliers beyond ylim
    outliers = {'24': [], '32': [], '36': [], '144': []}
    for group, label in zip([group_24['rsrp_diffs'], group_32['rsrp_diffs'], 
                           group_36['rsrp_diffs'], group_144['rsrp_diffs']], 
                           ['24', '32', '36', '144']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers beyond ylim={ylim} for {link_type}:")
    for label in ['24', '32', '36', '144']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    if save_flag:
        plt.savefig(f'D:/git/plots/box_rsrp_diff_{link_type.lower()}.pdf',
                    bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()

loaded_data = load_data_from_pickle('D:/git/pkl/Beam_top_set.pkl')

save_flag = 1
show_flag = 0

data_to_box(loaded_data['group_24'], loaded_data['group_32'], 
            loaded_data['group_36'], loaded_data['group_144'], 
            'Downlink', save_flag, show_flag)