import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

from _utils import get_mbit_str, get_pretty_codec_name


def plot_results(results, graph_title, graph_filename):
    seconds, bitrates, keyframes, encoder = results

    number_of_keyframes = len(keyframes)
    if number_of_keyframes > 75:
        print(f'Warning:\n{str(number_of_keyframes)} I-Frames detected.\n'
              'I-Frames are not shown on the graph for a video with more '
              'than 75 I-Frames as this results in a cluttered graph.\n'
              'Plotting the bitrate graph without I-frame markings...')
        # drop keyframes
        keyframes = []

    avg_bitrate = get_mbit_str(round(np.mean(bitrates), 2))
    min_bitrate = get_mbit_str(round(min(bitrates), 2))
    max_bitrate = get_mbit_str(round(max(bitrates), 2))
    std_bitrate = get_mbit_str(round(np.std(bitrates), 2))
    encoder = get_pretty_codec_name(encoder)

    # init the plot
    plt.figure(figsize=(19.20, 10.80))
    plt.suptitle(f'{graph_title} | Codec: {encoder}\n\
                Min: {min_bitrate} | Max: {max_bitrate} | Standard Deviation: '
                 f'{std_bitrate}')
    plt.xlabel('Seconds')
    plt.ylabel('Video Bitrate (Mbps)')
    plt.grid(True)

    # actually plot the data
    bitrate_line, = plt.plot(seconds, bitrates,
                             label=f'Bitrate (Average: {avg_bitrate})')
    # plot vertical lines for keyframes
    for frame in keyframes:
        plt.axvline(frame, color='r', linestyle='--', linewidth=1)

    # create legend for I-frame-lines
    label_text = 'I-Frames' if number_of_keyframes <= 75 else \
                 'Too many I-Frames'
    i_frame_legend = mlines.Line2D([], [], color='red', linestyle='--',
                                   markersize=10, label=label_text)
    # setup plot legend
    plt.legend(handles=[bitrate_line, i_frame_legend],
               labels=[bitrate_line.get_label(),
                       i_frame_legend.get_label()],
               loc='lower right')

    # save the plot
    plt.savefig(f'{graph_filename}.png')
    plt.close()


def plot_comparison(results_list, labels, graph_title, graph_filename):
    """
    Plot multiple bitrate series on a single graph for comparison.

    results_list: list of tuples like (seconds, bitrates, keyframes, encoder)
    labels: list of strings to identify each series (e.g., filenames)
    graph_title: title of the graph
    graph_filename: output filename without extension
    """
    if not results_list:
        raise ValueError('No results provided to plot_comparison')

    # init the plot
    plt.figure(figsize=(19.20, 10.80))
    plt.suptitle(graph_title)
    plt.xlabel('Seconds')
    plt.ylabel('Video Bitrate (Mbps)')
    plt.grid(True)

    # plot each series with its own label
    handles = []
    handle_labels = []
    for idx, results in enumerate(results_list):
        seconds, bitrates, keyframes, encoder = results
        avg_bitrate = get_mbit_str(round(np.mean(bitrates), 2))
        encoder_pretty = get_pretty_codec_name(encoder)

        series_label = labels[idx] if idx < len(labels) else f'Series {idx+1}'
        label_text = f'{series_label} ({encoder_pretty}, Avg: {avg_bitrate})'

        line, = plt.plot(seconds, bitrates, label=label_text)
        handles.append(line)
        handle_labels.append(label_text)

    # For comparisons, skip plotting I-Frame markers to avoid clutter
    plt.legend(handles=handles, labels=handle_labels, loc='lower right')

    # save the plot
    plt.savefig(f'{graph_filename}.png')
    plt.close()
