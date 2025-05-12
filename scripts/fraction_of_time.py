# Fig. 10(a)(b)
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
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

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

def data_to_bar(group_24, group_32, group_36, group_144, link_type, save_flag, show_flag):
    # Calculate the mean and standard deviation of each group
    group_24 = flatten_list(group_24)
    group_32 = flatten_list(group_32)
    group_36 = flatten_list(group_36)
    group_144 = flatten_list(group_144)
    
    means = [np.mean(group_24), np.mean(group_32), np.mean(group_36), np.mean(group_144)]
    medians = [np.median(group_24), np.median(group_32), np.median(group_36), np.median(group_144)]
    percentiles_75 = [np.percentile(group_24, 75), np.percentile(group_32, 75), np.percentile(group_36, 75), np.percentile(group_144, 75)]
    stds = [np.std(group_24), np.std(group_32), np.std(group_36), np.std(group_144)]

    # Print the statistics
    print(f'{link_type} Statistics:')
    for i, label in enumerate(['24', '32', '36', '144']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    labels = ['24', '32', '36', '144']
    positions = [1, 2, 3, 4]

    fig, ax = plt.subplots()
    bars = ax.bar(positions, means, width=0.6, yerr=stds, capsize=5, 
                  color='lightgray', 
                  edgecolor='black')

    # Set x-axis ticks and labels
    ax.set_xticks(positions)
    ax.set_xlabel('# beams per gNB')
    ax.set_xticklabels(labels)

    # Set y-axis range
    ax.set_ylim(0, 100)

    # Set y-axis label
    ax.set_ylabel('Fraction of time (%)')

    ax.axvline(x=3.5, color='black', linestyle='--')

    # Print outliers
    outliers = {'24': [], '32': [], '36': [], '144': []}
    ylim = ax.get_ylim()
    for group, label in zip([group_24, group_32, group_36, group_144], labels):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers beyond ylim={ylim} for {link_type}:")
    for label in labels:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    if save_flag:
        save_path = f'../plots/bar_fraction_of_time_{link_type.lower()}.pdf'
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()

loaded_data = load_data_from_pickle('../pkl/fraction_of_time.pkl')

dl_group_24, dl_group_32, dl_group_36, dl_group_144 = reorganize_data(loaded_data, 'Downlink')
ul_group_24, ul_group_32, ul_group_36, ul_group_144 = reorganize_data(loaded_data, 'Uplink')

save_flag = 1
show_flag = 0

data_to_bar(dl_group_24, dl_group_32, dl_group_36, dl_group_144, 'Downlink', save_flag, show_flag)
data_to_bar(ul_group_24, ul_group_32, ul_group_36, ul_group_144, 'Uplink', save_flag, show_flag)
