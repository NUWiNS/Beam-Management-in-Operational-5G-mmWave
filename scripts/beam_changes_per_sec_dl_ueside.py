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

def data_to_bar_ue(group_24_ue, group_24_ue_without_bs, 
                   group_32_ue, group_32_ue_without_bs,
                   group_36_ue, group_36_ue_without_bs,  
                   group_144_ue, group_144_ue_without_bs, 
                   link_type, side, save_flag, show_flag):
    # Calculate mean, median, 75th percentile and standard deviation for each group
    means = [np.mean(group_24_ue), np.mean(group_24_ue_without_bs),
             np.mean(group_32_ue), np.mean(group_32_ue_without_bs),
             np.mean(group_36_ue), np.mean(group_36_ue_without_bs),
             np.mean(group_144_ue), np.mean(group_144_ue_without_bs)]
    medians = [np.median(group_24_ue), np.median(group_24_ue_without_bs),
               np.median(group_32_ue), np.median(group_32_ue_without_bs),
               np.median(group_36_ue), np.median(group_36_ue_without_bs),
               np.median(group_144_ue), np.median(group_144_ue_without_bs)]
    percentiles_75 = [np.percentile(group_24_ue, 75), np.percentile(group_24_ue_without_bs, 75),
                      np.percentile(group_32_ue, 75), np.percentile(group_32_ue_without_bs, 75),
                      np.percentile(group_36_ue, 75), np.percentile(group_36_ue_without_bs, 75),
                      np.percentile(group_144_ue, 75), np.percentile(group_144_ue_without_bs, 75)]
    stds = [np.std(group_24_ue), np.std(group_24_ue_without_bs),
            np.std(group_32_ue), np.std(group_32_ue_without_bs),
            np.std(group_36_ue), np.std(group_36_ue_without_bs),
            np.std(group_144_ue), np.std(group_144_ue_without_bs)]
    
    # Print statistics
    print(f'{link_type} {side} Statistics:')
    for i, label in enumerate(['24', '24 w/o', '32', '32 w/o', '36', '36 w/o', '144', '144 w/o']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')
    
    labels = ['24', '32', '36', '144']
    
    # Manually defined positions for each group and gap
    positions = [1, 2, 4, 5, 7, 8, 10, 11]  # Adjust these values as needed for custom spacing

    fig, ax = plt.subplots()
    bar_width = 0.8  # Fixed bar width for all bars

    # Plot bars for data with beam switching (even indices)
    bars1 = ax.bar([positions[0], positions[2], positions[4], positions[6]], means[::2], width=bar_width, 
                   yerr=stds[::2], capsize=5, color='lightgray', edgecolor='black', label='Total')

    # Plot bars for data without beam switching (odd indices)
    bars2 = ax.bar([positions[1], positions[3], positions[5], positions[7]], means[1::2], width=bar_width, 
                   yerr=stds[1::2], capsize=5, color='white', edgecolor='black', label='w/o gNB change')

    # Set x-axis ticks and labels
    ax.set_xticks([(positions[i] + positions[i+1]) / 2 for i in range(0, len(positions), 2)])  # Middle point between each pair of bars
    ax.set_xticklabels(labels)
    ax.set_xlabel('# beams per gNB')

    # Manually set the vertical line between the third and fourth group
    ax.axvline(x=(positions[5] + positions[6]) / 2, color='black', linestyle='--')

    # Set y-axis range
    ax.set_ylim(0, 3.3)

    # Set y-axis label
    ax.set_ylabel('Beam changes per sec')

    # Add legend
    ax.legend()

    # Add title (optional)
    # ax.set_title(f'{link_type} {side} - Beam Changes per Second')

    if save_flag:
        save_path = f'D:/git/plots/bar_beam_changes_per_sec_{link_type.lower()}_{side.lower()}.pdf'
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()


loaded_data = load_data_from_pickle('D:/git/pkl/beam_changes_per_sec.pkl')

dl_ue_group_24, dl_ue_group_32, dl_ue_group_36, dl_ue_group_144 = reorganize_data(loaded_data, 'Downlink', 'UEside')
dl_ue_group_24_without_bs, dl_ue_group_32_without_bs, dl_ue_group_36_without_bs, dl_ue_group_144_without_bs = reorganize_data(loaded_data, 'Downlink', 'UE_switch_without_BS_switch')

save_flag = 1
show_flag = 0

data_to_bar_ue(dl_ue_group_24, dl_ue_group_24_without_bs, 
               dl_ue_group_32, dl_ue_group_32_without_bs,
               dl_ue_group_36, dl_ue_group_36_without_bs, 
               dl_ue_group_144, dl_ue_group_144_without_bs, 
               'Downlink', 'UEside', save_flag, show_flag)