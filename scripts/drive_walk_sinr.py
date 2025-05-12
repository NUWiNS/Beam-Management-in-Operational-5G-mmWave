# Fig. 13(a)
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

def data_to_box(DL_W, DL_D, save_flag, show_flag):
    # Create the figure
    DL_W = flatten_list(DL_W)
    DL_D = flatten_list(DL_D)

    # Calculate statistics
    means = [np.mean(DL_W), np.mean(DL_D)]
    medians = [np.median(DL_W), np.median(DL_D)]
    percentiles_75 = [np.percentile(DL_W, 75), np.percentile(DL_D, 75)]

    # Print statistics
    print(f'SINR Statistics:')
    for i, label in enumerate(['Walk DL', 'Drive DL']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    fig, ax = plt.subplots()

    positions = [1, 2]
    labels = ['Walk DL', 'Drive DL']
    bp = ax.boxplot([DL_W, DL_D],
                    positions=positions, patch_artist=True, widths=0.6)

    for box in bp['boxes']:
        box.set_facecolor('lightgray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)

    ylim = (-32, 32)  # Adjust this value to fit the range of SINR
    ax.set_ylim(*ylim)

    ax.set_ylabel('SINR (dB)')

    # Print out outliers beyond ylim
    outliers = {'Walk DL': [], 'Drive DL': []}
    for group, label in zip([DL_W, DL_D], ['Walk DL', 'Drive DL']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers :")
    for label in ['Walk DL', 'Drive DL']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    # Save the image
    if save_flag:
        plt.savefig(f'../plots/box_drive_walk_sinr.pdf',
                    bbox_inches='tight', dpi=300)

    # Show the image
    if show_flag:
        plt.show()

    plt.close()

# Main program
loaded_data = load_data_from_pickle('../pkl/drive_walk_sinr.pkl')

save_flag = 1
show_flag = 0

data_to_box(loaded_data['Downlink']['Walk'],
            loaded_data['Downlink']['Drive'], 
            save_flag, show_flag)
