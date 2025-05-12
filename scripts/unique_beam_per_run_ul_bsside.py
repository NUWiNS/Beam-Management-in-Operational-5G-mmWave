# Fig. 4(a)
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

def reorganize_data(data, link_type):
    group_24 = []
    group_32 = []
    group_36 = []
    group_144 = []

    for city in ['boston', 'charlotte']: # 8 * 3
        city_data = data[link_type][f'att_{city}']
        group_24.extend(city_data['forward'])
        group_24.extend(city_data['backward'])
        group_24.extend(city_data['lateral'])

    for city in ['charlotte', 'miami']: # 12 * 3
        city_data = data[link_type][f'verizon_{city}']
        group_36.extend(city_data['forward'])
        group_36.extend(city_data['backward'])
        group_36.extend(city_data['lateral'])

    # verizon_boston as a separate group
    boston_data = data[link_type]['verizon_boston'] # 48 * 3
    group_144.extend(boston_data['forward'])
    group_144.extend(boston_data['backward'])
    group_144.extend(boston_data['lateral'])

    vegas_data = data[link_type]['att_vegas'] # 8 * 4
    group_32.extend(vegas_data['forward'])
    group_32.extend(vegas_data['backward'])
    group_32.extend(vegas_data['lateral'])

    return group_24, group_32, group_36, group_144

def data_to_bar(group_24, group_32, group_36, group_144, link_type, save_flag, show_flag):
    # Calculate statistics for each group
    means = [np.mean(group_24), np.mean(group_32), np.mean(group_36), np.mean(group_144)]
    medians = [np.median(group_24), np.median(group_32), np.median(group_36), np.median(group_144)]
    percentiles_75 = [np.percentile(group_24, 75), np.percentile(group_32, 75), np.percentile(group_36, 75), np.percentile(group_144, 75)]
    stds = [np.std(group_24), np.std(group_32), np.std(group_36), np.std(group_144)]

    # Print statistics
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
    ax.set_ylim(0, 15)

    # Set y-axis label
    ax.set_ylabel('Unique beams per run')

    ax.axvline(x=3.5, color='black', linestyle='--')
    # Add legend
    # ax.legend([link_type])

    # plt.title(f'{link_type}')

    if save_flag:
        save_path = f'../plots/bar_unique_beam_{link_type.lower()}_bsside.pdf'
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()

loaded_data = load_data_from_pickle('../pkl/unique_beam_per_run_bsside.pkl')

ul_group_24, ul_group_32, ul_group_36, ul_group_144 = reorganize_data(loaded_data, 'Uplink')

save_flag = 1
show_flag = 0

data_to_bar(ul_group_24, ul_group_32, ul_group_36, ul_group_144, 'Uplink', save_flag, show_flag)
