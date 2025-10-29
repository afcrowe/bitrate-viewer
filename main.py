from argparse import ArgumentParser, RawTextHelpFormatter
import os
from pathlib import Path
import sys

from _bitrate_analyzer import analyze_bitrate
from _plotter import plot_results, plot_comparison


def main():
    if len(sys.argv) == 1:
        print("To see more details about the available arguments, "
              "enter 'python main.py -h'")

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input-video-path', type=str, nargs='+', required=True,
                    help='Enter one or more paths of input videos. '
                        'Relative or absolute paths are supported.')
    parser.add_argument('-f', '--output-format',
                        type=str, default='xml', choices=['xml', 'json'],
                        help='Specify the output format for the file written\n'
                             'by FFProbe. (default: \'xml\')')
    parser.add_argument('-o', '--output-filename', type=str, default=None,
                    help='Optional output image filename without extension.\n'
                        'If not provided, for single input the video stem is used;\n'
                        'for multiple inputs, a combined name like comparison.png is used.')
    parser.add_argument('-t', '--title', type=str, default=None,
                    help='Optional custom title for the graph. If omitted,\n'
                        'uses the filename(s) by default.')

    arguments = parser.parse_args()

    video_files = arguments.input_video_path
    output_format = arguments.output_format
    output_filename = arguments.output_filename
    custom_title = arguments.title

    # validate files
    missing = [vf for vf in video_files if not os.path.exists(vf)]
    if missing:
        print(f'The following input files could not be found: {missing}. Exiting.')
        sys.exit()

    if len(video_files) == 1:
        video_file = video_files[0]
        results = analyze_bitrate(video_file, output_format)
        print('Done. Now plotting results ...')

        graph_title = custom_title or Path(video_file).name
        graph_filename = output_filename or Path(video_file).stem

        plot_results(results, graph_title, graph_filename)
        print(f'Done. Check {graph_filename}.png and '
              f'{Path(video_file).stem}.{output_format}!')
    else:
        # Multiple files: analyze each and plot comparison
        all_results = []
        labels = []
        written_sidecars = []
        for vf in video_files:
            res = analyze_bitrate(vf, output_format)
            all_results.append(res)
            labels.append(Path(vf).name)
            written_sidecars.append(f"{Path(vf).stem}.{output_format}")

        print('Done. Now plotting comparison results ...')

        title_default = 'Bitrate Comparison: ' + ', '.join([Path(vf).name for vf in video_files])
        graph_title = custom_title or title_default
        graph_filename = output_filename or 'comparison'

    plot_comparison(all_results, labels, graph_title, graph_filename)
    sidecars_str = ', '.join(written_sidecars)
    print(f'Done. Check {graph_filename}.png and sidecar files: {sidecars_str}')


if __name__ == "__main__":
    main()
