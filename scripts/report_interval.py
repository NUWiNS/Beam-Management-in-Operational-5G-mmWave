import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

def load_data_from_pickle(filename):
    """
    Load data from pickle file
    """
    with open(filename, 'rb') as file:
        loaded_data = pickle.load(file)
    print(f"loaded from {filename} ")
    return loaded_data

def flatten_list(nested_list):
    if isinstance(nested_list, str):
        return [nested_list]
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, (list, tuple)) else [sublist])]

def reorganize_data(data, link_type):
    group_24 = []
    group_32 = []
    group_36 = []
    group_144 = []

    for city in ['boston', 'charlotte']:
        city_data = data[link_type][f'att_{city}']
        group_24.extend(city_data['forward'])
        group_24.extend(city_data['backward'])
        group_24.extend(city_data['lateral'])

    for city in ['charlotte', 'miami']:
        city_data = data[link_type][f'verizon_{city}']
        group_36.extend(city_data['forward'])
        group_36.extend(city_data['backward'])
        group_36.extend(city_data['lateral'])

    # verizon_boston is a separate group
    boston_data = data[link_type]['verizon_boston']
    group_144.extend(boston_data['forward'])
    group_144.extend(boston_data['backward'])
    group_144.extend(boston_data['lateral'])

    vegas_data = data[link_type]['att_vegas']
    group_32.extend(vegas_data['forward'])
    group_32.extend(vegas_data['backward'])
    group_32.extend(vegas_data['lateral'])

    return group_24, group_32, group_36, group_144

def data_to_box(group_24, group_32, group_36, group_144, link_type, save_flag, show_flag):
    
    group_24 = flatten_list(group_24)
    group_32 = flatten_list(group_32)
    group_36 = flatten_list(group_36)
    group_144 = flatten_list(group_144)

    # Calculate statistics
    means = [np.mean(group_24), np.mean(group_32), np.mean(group_36), np.mean(group_144)]
    medians = [np.median(group_24), np.median(group_32), np.median(group_36), np.median(group_144)]
    percentiles_75 = [np.percentile(group_24, 75), np.percentile(group_32, 75), np.percentile(group_36, 75), np.percentile(group_144, 75)]

    # Print statistics
    print(f'{link_type} Statistics:')
    for i, label in enumerate(['24', '32', '36', '144']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    fig, ax = plt.subplots()
    
    positions = [1, 2, 3, 4]
    labels = ['24', '32', '36', '144']
    bp = ax.boxplot([group_24, group_32, group_36, group_144], 
                    positions=positions, patch_artist=True, widths=0.6)
    
    for box in bp['boxes']:
        box.set_facecolor('lightgray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)
    
    ax.set_xticks(positions)
    ax.set_xlabel('# beams per gNB')
    ax.set_xticklabels(labels)
    
    ylim = (-0.05, 2)
    ax.set_ylim(*ylim)

    ax.set_ylabel('Reporting interval (s)')

    ax.axvline(x=3.5, color='black', linestyle='--')

    outliers = {'24': [], '32': [], '36': [], '144': []}
    for group, label in zip([group_24, group_32, group_36, group_144], ['24', '32', '36', '144']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)
    
    print(f"Outliers beyond ylim={ylim} for {link_type}:")
    for label in ['24', '32', '36', '144']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    
    # ax.set_title(f'{link_type}')
    
    
    if save_flag:

        plt.savefig(f'D:/git/plots/box_report_interval_{link_type.lower()}.pdf', 
                    bbox_inches='tight', dpi=300)
    
    
    if show_flag:
        plt.show()
    
    plt.close()

loaded_data = load_data_from_pickle('D:/git/pkl/report_interval.pkl')

dl_group_24, dl_group_32, dl_group_36, dl_group_144 = reorganize_data(loaded_data, 'Downlink')

ul_group_24, ul_group_32, ul_group_36, ul_group_144 = reorganize_data(loaded_data, 'Uplink')


save_flag = 1
show_flag = 0


data_to_box(dl_group_24, dl_group_32, dl_group_36, dl_group_144, 'Downlink', save_flag, show_flag)

data_to_box(ul_group_24, ul_group_32, ul_group_36, ul_group_144, 'Uplink', save_flag, show_flag)
