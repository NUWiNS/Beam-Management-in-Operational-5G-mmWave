# Fig. 6(a)(b)(c)
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

def load_data(graph_type):
    # Load data from a pickle file based on the graph type
    with open(f'D:/git/pkl/{graph_type}.pkl', 'rb') as f:
        return pickle.load(f)
    
def flatten_list(nested_list):
    # Flatten a nested list into a single list
    return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

def reorganize_data(data, link_type):
    # Reorganize data based on link type and city
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

def plot_box(group_24, group_32, group_36, group_144, graph_type, link_type, save_flag, show_flag):
    # Flatten the groups before plotting
    group_24 = flatten_list(group_24)
    group_32 = flatten_list(group_32)
    group_36 = flatten_list(group_36)
    group_144 = flatten_list(group_144)

    # Calculate statistics
    means = [np.mean(group_24), np.mean(group_32), np.mean(group_36), np.mean(group_144)]
    medians = [np.median(group_24), np.median(group_32), np.median(group_36), np.median(group_144)]
    percentiles_75 = [np.percentile(group_24, 75), np.percentile(group_32, 75), np.percentile(group_36, 75), np.percentile(group_144, 75)]

    # Print statistics
    print(f'{graph_type} {link_type} Statistics:')
    for i, label in enumerate(['24', '32', '36', '144']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    # Create box plot
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
    ax.set_ylabel(get_ylabel(graph_type))
    ax.axvline(x=3.5, color='black', linestyle='--')
    ylim = get_ylim(graph_type)
    ax.set_ylim(*ylim)
    
    # Print out outliers beyond ylim
    outliers = {'24': [], '32': [], '36': [], '144': []}
    for group, label in zip([group_24, group_32, group_36, group_144], ['24', '32', '36', '144']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers beyond ylim={ylim} for {graph_type} {link_type}:")
    for label in ['24', '32', '36', '144']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    if save_flag:
        plt.savefig(f'D:/git/plots/box_{graph_type}_{link_type.lower()}.pdf', 
                    bbox_inches='tight', dpi=300)
    if show_flag:
        plt.show()
    plt.close()

def get_ylabel(graph_type):
    # Return the y-axis label based on the graph type
    ylabels = {
        'mcs': 'MCS',
        'sinr': 'SINR (dB)',
        'pcell_tput': 'Throughput (Mbps)'
    }
    return ylabels[graph_type]

def get_ylim(graph_type):
    # Return the y-axis limits based on the graph type
    ylim = {
        'mcs': (-1, 30),
        'sinr': (-32, 32),
        'pcell_tput': (-20, 750)
    }
    return ylim[graph_type]

def plot_all_graphs(save_flag, show_flag):
    # Plot all graphs for different graph types
    graph_types = ['mcs', 'sinr', 'pcell_tput']
    for graph_type in graph_types:
        data = load_data(graph_type)
        
        link_types = ['Downlink']

        for link_type in link_types:
            group_24, group_32, group_36, group_144 = reorganize_data(data, link_type)
            plot_box(group_24, group_32, group_36, group_144, graph_type, link_type, save_flag, show_flag)

if __name__ == "__main__":
    save_flag = 1
    show_flag = 0
    plot_all_graphs(save_flag, show_flag)
