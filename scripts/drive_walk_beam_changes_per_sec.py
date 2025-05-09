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

def data_to_box(DL_W, UL_W, DL_D, UL_D, side, save_flag, show_flag):
    # Create the figure
    DL_W = flatten_list(DL_W)
    UL_W = flatten_list(UL_W)
    DL_D = flatten_list(DL_D)
    UL_D = flatten_list(UL_D)

    # Calculate statistics
    means = [np.mean(DL_W), np.mean(UL_W), np.mean(DL_D), np.mean(UL_D)]
    medians = [np.median(DL_W), np.median(UL_W), np.median(DL_D), np.median(UL_D)]
    percentiles_75 = [np.percentile(DL_W, 75), np.percentile(UL_W, 75), np.percentile(DL_D, 75), np.percentile(UL_D, 75)]

    # Print statistics
    print(f'Beam changes per sec Statistics ({side}):')
    for i, label in enumerate(['Walk DL', 'Walk UL', 'Drive DL', 'Drive UL']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    fig, ax = plt.subplots()

    positions = [1, 2, 3, 4]
    labels = ['DL', 'UL', 'DL', 'UL']
    bp = ax.boxplot([DL_W, UL_W, DL_D, UL_D],
                    positions=positions, patch_artist=True, widths=0.6)

    for box in bp['boxes']:
        box.set_facecolor('lightgray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)

    # Set different y-axis limits based on side
    if side == 'BSside':
        ylim = (0, 2.6)
        ax.set_yticks(np.arange(0, 2.6, 0.5))
    elif side == 'UEside':
        ylim = (0, 4.6)  # Adjust this value to fit the data range of UEside
        ax.set_yticks(np.arange(0, 4.6, 0.5))

    ax.set_ylim(*ylim)

    # Add Walk and Drive labels on top of the image
    ax.text((positions[0] + positions[1])/2, ylim[1] + 0.03, 'Walk', 
            horizontalalignment='center', verticalalignment='bottom', fontsize=24)
    ax.text((positions[2] + positions[3])/2, ylim[1] + 0.03, 'Drive',
            horizontalalignment='center', verticalalignment='bottom', fontsize=24)

    ax.set_ylabel(f'Beam changes per sec')

    # Print out outliers beyond ylim
    outliers = {'Walk DL': [], 'Walk UL': [], 'Drive DL': [], 'Drive UL': []}
    for group, label in zip([DL_W, UL_W, DL_D, UL_D], ['Walk DL', 'Walk UL', 'Drive DL', 'Drive UL']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers ({side}):")
    for label in ['Walk DL', 'Walk UL', 'Drive DL', 'Drive UL']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    # Save the image
    if save_flag:
        plt.savefig(f'D:/git/plots/box_drive_walk_beam_changes_per_sec_{side.lower()}_full.pdf',
                    bbox_inches='tight', dpi=300)

    # Show the image
    if show_flag:
        plt.show()

    plt.close()

# Main program
loaded_data = load_data_from_pickle('D:/git/pkl/drive_walk_beam_changes_per_sec_30S_full.pkl')

save_flag = 1
show_flag = 0

data_to_box(loaded_data['BSside']['Downlink']['Walk'], loaded_data['BSside']['Uplink']['Walk'],
            loaded_data['BSside']['Downlink']['Drive'], loaded_data['BSside']['Uplink']['Drive'], 
            'BSside', save_flag, show_flag)

data_to_box(loaded_data['UEside']['Downlink']['Walk'], loaded_data['UEside']['Uplink']['Walk'],
            loaded_data['UEside']['Downlink']['Drive'], loaded_data['UEside']['Uplink']['Drive'], 
            'UEside', save_flag, show_flag)