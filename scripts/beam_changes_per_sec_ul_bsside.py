# Fig. 4(b)
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

def flatten_list(nested_list):
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

def reorganize_data(data, link_type, side):
    group_24 = []
    group_32 = []
    group_36 = []
    group_144 = []

    for city in ['boston', 'charlotte']:
        city_data = data[link_type][side][f'att_{city}']
        group_24.extend(city_data['forward'])
        group_24.extend(city_data['backward'])
        group_24.extend(city_data['lateral'])

    for city in ['charlotte', 'miami']:
        city_data = data[link_type][side][f'verizon_{city}']
        group_36.extend(city_data['forward'])
        group_36.extend(city_data['backward'])
        group_36.extend(city_data['lateral'])

    # verizon_boston as a separate group
    boston_data = data[link_type][side]['verizon_boston']
    group_144.extend(boston_data['forward'])
    group_144.extend(boston_data['backward'])
    group_144.extend(boston_data['lateral'])

    vegas_data = data[link_type][side]['att_vegas']
    group_32.extend(vegas_data['forward'])
    group_32.extend(vegas_data['backward'])
    group_32.extend(vegas_data['lateral'])

    return group_24, group_32, group_36, group_144


def data_to_bar(group_24, group_32, group_36, group_144, link_type, side, save_flag, show_flag):
    # Calculate mean, median, 75th percentile and standard deviation for each group
    means = [np.mean(group_24), np.mean(group_32), np.mean(group_36), np.mean(group_144)]
    medians = [np.median(group_24), np.median(group_32), np.median(group_36), np.median(group_144)]
    percentiles_75 = [np.percentile(group_24, 75), np.percentile(group_32, 75), np.percentile(group_36, 75), np.percentile(group_144, 75)]
    stds = [np.std(group_24), np.std(group_32), np.std(group_36), np.std(group_144)]

    # Print statistics
    print(f'{link_type} {side} Statistics:')
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

    ax.axvline(x=3.5, color='black', linestyle='--')
    # Set y-axis range
    ax.set_ylim(0, 2)

    # Set y-axis label
    ax.set_ylabel('Beam changes per sec')

    if save_flag:
        save_path = f'../plots/bar_beam_changes_per_sec_{link_type.lower()}_{side.lower()}.pdf'
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()


loaded_data = load_data_from_pickle('../pkl/beam_changes_per_sec.pkl')

ul_bs_group_24, ul_bs_group_32, ul_bs_group_36, ul_bs_group_144 = reorganize_data(loaded_data, 'Uplink', 'BSside')

save_flag = 1
show_flag = 0

data_to_bar(ul_bs_group_24, ul_bs_group_32, ul_bs_group_36, ul_bs_group_144, 'Uplink', 'BSside', save_flag, show_flag)
