# Fig. 9(a)(b)(c)(d)
import numpy as np
import pickle
import matplotlib.pyplot as plt


def load_data_from_pickle(filename):
    """
    Load data from a pickle file
    """
    with open(filename, 'rb') as file:
        loaded_data = pickle.load(file)
    print(f"loaded from {filename} ")
    return loaded_data

def reorganize_data(data, link_type):
    groups = {
        'group_24': {'Best': [], 'Top_1': [], 'Top_2': [], 'Top_3': []},
        'group_32': {'Best': [], 'Top_1': [], 'Top_2': [], 'Top_3': []},
        'group_36': {'Best': [], 'Top_1': [], 'Top_2': [], 'Top_3': []},
        'group_144': {'Best': [], 'Top_1': [], 'Top_2': [], 'Top_3': []}
    }
    
    def extend_group(group, city_data):
        for direction in ['forward', 'backward', 'lateral']:
            for key in ['Best', 'Top_1', 'Top_2', 'Top_3']:
                group[key].extend(city_data[direction][key])

    # Group 24: AT&T Boston and Charlotte
    for city in ['boston', 'charlotte']:
        extend_group(groups['group_24'], data[link_type][f'att_{city}'])

    # Group 36: Verizon Charlotte and Miami
    for city in ['charlotte', 'miami']:
        extend_group(groups['group_36'], data[link_type][f'verizon_{city}'])
    
    # Group 32: Att Vegas
    extend_group(groups['group_32'], data[link_type]['att_vegas'])
    
    # Group 144: Verizon Boston
    extend_group(groups['group_144'], data[link_type]['verizon_boston'])
    
    return groups['group_24'], groups['group_32'], groups['group_36'], groups['group_144']

def data_to_cdf(group, group_name, link_type, save_flag, show_flag, use_colors=False):
    # Create a figure
    fig, ax = plt.subplots()
    
    # Print statistical information
    print(f'\n{link_type} {group_name} Statistics:')
    for key, label in zip(['Best', 'Top_1', 'Top_2', 'Top_3'],
                         ['Best', 'Top 1', 'Top 2', 'Top 3']):
        data = group[key]
        print(f'{label}: Max={max(data):.2f}, Min={min(data):.2f}, Median={np.median(data):.2f}')
    
    # Calculate the CDF for each dataset
    line_styles = ['-', '--', ':', '-.']
    colors = ['black', 'red', 'blue', 'green']
    
    for i, (key, label) in enumerate(zip(['Best', 'Top_1', 'Top_2', 'Top_3'],
                                       ['Best', 'Top 1', 'Top 2', 'Top 3'])):
        data = sorted(group[key])
        n = len(data)
        y = np.arange(1, n + 1) / n
        
        if use_colors:
            ax.plot(data, y, color=colors[i], linestyle='-', label=label, linewidth=2)
        else:
            ax.plot(data, y, color='black', linestyle=line_styles[i], label=label, linewidth=2)
    
    ax.legend()
    
    ax.set_xlabel('RSRP Difference (dB)')
    ax.set_ylabel('CDF')
    
    # Set the X-axis range to -10 to 0
    # ax.set_xlim(-11, 1)
    
    # Save the image
    if save_flag:
        plt.savefig(f'D:/git/plots/cdf_pcell_rsrp_top_diff_{link_type.lower()}_{group_name}.pdf',
                    bbox_inches='tight', dpi=300)
    
    # Display the image  
    if show_flag:
        plt.show()
    plt.close()

loaded_data = load_data_from_pickle('D:/git/pkl/rsrp_s_b_top_diff.pkl')

group_24_dl, group_32_dl, group_36_dl, group_144_dl = reorganize_data(loaded_data, 'Downlink')
group_24_ul, group_32_ul, group_36_ul, group_144_ul = reorganize_data(loaded_data, 'Uplink')

save_flag = 1
show_flag = 0

data_to_cdf(group_24_dl, 'group_24_dl', 'Downlink', save_flag, show_flag)
data_to_cdf(group_32_dl, 'group_32_dl', 'Downlink', save_flag, show_flag)
data_to_cdf(group_36_dl, 'group_36_dl', 'Downlink', save_flag, show_flag)
data_to_cdf(group_144_dl, 'group_144_dl', 'Downlink', save_flag, show_flag)



