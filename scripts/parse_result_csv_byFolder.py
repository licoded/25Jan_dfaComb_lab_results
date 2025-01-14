#!/usr/bin/env python3
import csv
import re
import os
import sys


def read_file(file_path):
    """Reads a file and returns its content as a list of rows."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            result = []
            for row in csv.DictReader(f):
                # print(row)
                modified_row = {key.strip(): value.strip() for key, value in row.items()}
                # print(modified_row)
                result.append(modified_row)
            return result
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")


def filter_and_group_by_folder(data, folder_prefix, result_types):
    """Filters data by folder prefix and groups by 'Result'."""
    filtered_data = [item for item in data if item['Folder'].startswith(folder_prefix)]
    grouped_data = {}
    for item in filtered_data:
        grouped_data[item['Result']] = grouped_data.get(item['Result'], []) + [item]
    for result_type in result_types:
        print(f"{folder_prefix.capitalize()} {result_type}:\t", len(grouped_data.get(result_type, [])))

def filter_and_group_by_regex(data, regex_pattern, result_types):
    """Filters data by regex pattern and groups by 'Result'."""
    import re
    filtered_data = [item for item in data if re.match(regex_pattern, item['Folder'])]
    grouped_data = {}
    for item in filtered_data:
        grouped_data[item['Result']] = grouped_data.get(item['Result'], []) + [item]
    for result_type in result_types:
        print(f"Ascending {result_type}:\t", len(grouped_data.get(result_type, [])))


def main():
    # Parse command-line arguments
    itself = sys.argv[0]
    args = sys.argv[1:]

    if '-h' in args or '--help' in args or len(args) < 2:
        print(f"Usage: {itself} --path <path to main CSV file> [--copyFlag]")
        sys.exit(1)

    if '--path' not in args:
        print("Error: --path argument is required.")
        sys.exit(1)

    path_index = args.index('--path') + 1
    if path_index >= len(args):
        print("Error: Missing value for --path argument.")
        sys.exit(1)

    path = args[path_index]
    if (not os.path.isfile(path)):
        print(f"File {path} does not exist!")
        sys.exit(1)
    copy_flag = '--copyFlag' in args

    # Custom logging if --copyFlag is set
    if copy_flag:
        import builtins
        original_print = builtins.print
        builtins.print = lambda *args, **kwargs: original_print(args[-1], **kwargs)

    # Read and parse the main CSV file
    parse_data = read_file(path)

    result_types = ['Realizable', 'Unrealizable']
    total_solved_data = [item for item in parse_data if item['Result'] in result_types]
    print('Total Solved:\t', len(total_solved_data))
    print('')  # Blank line

    filter_and_group_by_folder(parse_data, 'case', result_types)
    filter_and_group_by_folder(parse_data, 'syft', result_types)
    filter_and_group_by_regex(parse_data, r'^t\d+$', result_types)

    # Two-player-games folder patterns
    two_player_games_folders = [
        {'name': 'Single-Counter', 'regex': r'Single-Counter'},
        {'name': 'Double-Counter', 'regex': r'Double-Counter'},
        {'name': 'Nim', 'regex': r'nim_\d+'},
    ]

    # Two-player-games
    for folder_item in two_player_games_folders:
        regex = re.compile(folder_item['regex'])
        two_player_games_data = [item for item in parse_data if regex.search(item['Folder'])]
        two_player_games_solved_data = [item for item in two_player_games_data if item['Result'] in result_types]
        pad_space_str = '\t' if len(folder_item['name']) < 8 else ''
        print(f"{folder_item['name']} Solved:{pad_space_str}\t", len(two_player_games_solved_data))


if __name__ == "__main__":
    main()
