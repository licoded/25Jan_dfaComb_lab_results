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


def get_key(item):
    """Generates a unique key based on 'Folder' and 'Filename' fields."""
    return f"{item['Folder']},{item['Filename']}"


def is_not_tpg(folder_name, folder_patterns):
    """Checks if a folder name does not match any pattern in folder_patterns."""
    return all(not re.search(pattern['regex'], folder_name) for pattern in folder_patterns)


def main():
    # Parse command-line arguments
    itself = sys.argv[0]
    args = sys.argv[1:]

    one_sub_af_csv_path = "./only_one_subAf/all_oneSubAf.csv"
    if (not os.path.isfile(one_sub_af_csv_path)):
        print(f"File {one_sub_af_csv_path} does not exist!")
        print(f"Extra: please use in root of git folder, as this script use relative path to find `all_oneSubAf.csv` ")
        sys.exit(1)
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

    # Two-player-games folder patterns
    two_player_games_folders = [
        {'name': 'Single-Counter', 'regex': r'Single-Counter'},
        {'name': 'Double-Counter', 'regex': r'Double-Counter'},
        {'name': 'Nim', 'regex': r'nim_\d+'},
    ]

    # Read the oneSubAf CSV file
    parse_one_sub_af = read_file(one_sub_af_csv_path)

    parse_one_sub_af_keys = {get_key(item) for item in parse_one_sub_af}

    # Filter random data
    random_data = [item for item in parse_data if is_not_tpg(item['Folder'], two_player_games_folders)]
    random_data1 = [item for item in random_data if get_key(item) in parse_one_sub_af_keys]
    random_data2 = [item for item in random_data if get_key(item) not in parse_one_sub_af_keys]

    for random_group_data, label in [(random_data1, 'Random  one_subAf'), (random_data2, 'Random mult_subAf')]:
        grouped = {}
        for item in random_group_data:
            grouped[item['Result']] = grouped.get(item['Result'], 0) + 1
        for result_type in result_types:
            print(f"{label} {result_type}:\t", grouped.get(result_type, 0))

    # Two-player-games
    for folder_item in two_player_games_folders:
        regex = re.compile(folder_item['regex'])
        two_player_games_data = [item for item in parse_data if regex.search(item['Folder'])]
        two_player_games_solved_data = [item for item in two_player_games_data if item['Result'] in result_types]
        pad_space_str = '\t' if len(folder_item['name']) < 8 else ''
        print(f"{folder_item['name']} Solved:{pad_space_str}\t", len(two_player_games_solved_data))


if __name__ == "__main__":
    main()
