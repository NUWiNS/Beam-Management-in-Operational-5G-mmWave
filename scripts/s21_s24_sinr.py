# Fig. 18(a)
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

def reorganize_data_drive(data):
    s21_dl = []
    s24_dl = []

    # Process s21 data
    s21_dl.extend(data['s21']['Downlink']['Drive'])

    # Process s24 data 
    s24_dl.extend(data['s24']['Downlink']['Drive'])

    return s21_dl, s24_dl

def reorganize_data_walk(data):
    s21_dl = []
    s24_dl = []

    # Process s21 data
    s21_data_dl = data['Downlink']['s21']
    s21_dl.extend(s21_data_dl['forward'])
    s21_dl.extend(s21_data_dl['backward']) 
    s21_dl.extend(s21_data_dl['lateral'])

    # Process s24 data
    s24_data_dl = data['Downlink']['s24']
    s24_dl.extend(s24_data_dl['forward'])
    s24_dl.extend(s24_data_dl['backward'])
    s24_dl.extend(s24_data_dl['lateral'])

    return s21_dl, s24_dl

def data_to_box(s21_walk, s21_drive, s24_walk, s24_drive, save_flag, show_flag):
    # Create figure
    s21_walk = flatten_list(s21_walk)
    s21_drive = flatten_list(s21_drive)
    s24_walk = flatten_list(s24_walk)
    s24_drive = flatten_list(s24_drive)

    # Calculate statistics
    means = [np.mean(s21_walk), np.mean(s21_drive), np.mean(s24_walk), np.mean(s24_drive)]
    medians = [np.median(s21_walk), np.median(s21_drive), np.median(s24_walk), np.median(s24_drive)]
    percentiles_75 = [np.percentile(s21_walk, 75), np.percentile(s21_drive, 75), np.percentile(s24_walk, 75), np.percentile(s24_drive, 75)]

    # Print statistics
    print(f'SINR Statistics (Downlink):')
    for i, label in enumerate(['S21 Walk', 'S21 Drive', 'S24 Walk', 'S24 Drive']):
        print(f'Group {label}: Mean={means[i]:.2f}, Median={medians[i]:.2f}, 75th Percentile={percentiles_75[i]:.2f}')

    fig, ax = plt.subplots()

    positions = [1, 2, 3, 4]
    labels = ['Walk', 'Drive', 'Walk', 'Drive']  # Modified labels
    bp = ax.boxplot([s21_walk, s21_drive, s24_walk, s24_drive],
                    positions=positions, patch_artist=True, widths=0.6)

    for box in bp['boxes']:
        box.set_facecolor('lightgray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)

    ylim = (-33, 32)
    ax.set_ylim(*ylim)

    # Add S21 and S24 labels above the figure
    ax.text((positions[0] + positions[1])/2, ylim[1] + 0.5, 'S21', 
            horizontalalignment='center', verticalalignment='bottom', fontsize=25)
    ax.text((positions[2] + positions[3])/2, ylim[1] + 0.5, 'S24',
            horizontalalignment='center', verticalalignment='bottom', fontsize=25)

    ax.set_ylabel('SINR (dB)')

    # Print outliers that exceed ylim
    outliers = {'S21 Walk': [], 'S21 Drive': [], 'S24 Walk': [], 'S24 Drive': []}
    for group, label in zip([s21_walk, s21_drive, s24_walk, s24_drive], ['S21 Walk', 'S21 Drive', 'S24 Walk', 'S24 Drive']):
        for value in group:
            if value < ylim[0] or value > ylim[1]:
                outliers[label].append(value)

    print(f"Outliers :")
    for label in ['S21 Walk', 'S21 Drive', 'S24 Walk', 'S24 Drive']:
        if outliers[label]:
            print(f"Group {label}: {outliers[label]}")

    # Save figure
    if save_flag:
        plt.savefig(f'D:/git/plots/box_s21_s24_sinr_dl.pdf',
                    bbox_inches='tight', dpi=300)

    # Show figure
    if show_flag:
        plt.show()

    plt.close()

# Main program
loaded_walk_data = load_data_from_pickle('D:/git/pkl/s21_s24_walk_sinr.pkl')
loaded_drive_data = load_data_from_pickle('D:/git/pkl/s21_s24_drive_sinr.pkl')

save_flag = 1
show_flag = 0

s21_walk_dl, s24_walk_dl = reorganize_data_walk(loaded_walk_data)
s21_drive_dl, s24_drive_dl = reorganize_data_drive(loaded_drive_data)
data_to_box(s21_walk_dl, s21_drive_dl, s24_walk_dl, s24_drive_dl, save_flag, show_flag)
