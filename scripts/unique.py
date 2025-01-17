import sys
import csv
import os

def print_usages():
    print("Usage: python3 unique.py [options] file1 file2 ...")
    print("Options:")
    print("\t--filter=<csv_file>,0: print unique results not in <csv_file>")
    print("\t--filter=<csv_file>,1: print unique results in <csv_file>")
    sys.exit(0)


def assrt_file_exist(file):
    if (not os.path.isfile(file)):
        print(f"File {file} does not exist!")
        sys.exit(1)


def csv_to_list_of_dict(csv_file):
    result = []
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            modified_row = {key.strip(): value.strip() for key, value in row.items()}
            result.append(modified_row)
    
    return result


def parseFilename_inner(filename):
    # 定义关键字到结果的映射
    key_map = {
        "dfaComb_m1": "dfaComb_m1",
        "dfaComb_m2": "dfaComb_m2",
        "lydiasyft": "lydiasyft",
        "tople_m0e0": "tople_m0e0",
        "tople_m0e1": "tople_m0e1",
        "tople_m1e0": "tople_m1e0",
        "tople_m1e1": "tople_m1e1",
        "tople": "tople",
        "synthesis": "on-the-fly_new",
        "on-the-fly_new": "on-the-fly_new",
        "nowholeDFA": "nowholeDFA",
        "lisa": "lisa",
        "nike": "nike",
        "cynthia": "cynthia",
        "lydia": "lydia",
    }

    # 遍历字典检查关键字是否出现在文件名中
    for key, value in key_map.items():
        if key in filename:
            return value

    # 默认返回文件名
    return filename


def parseFilename(filename):
    foldername = filename.split('/')[-2]
    last_hashId = foldername.split('_')[-1]
    return parseFilename_inner(filename) + '_' + last_hashId


if len(sys.argv) < 3:
    print("Please input two or more files!")
    sys.exit(1)

files = []
filter_csv = None
filter_idx = -1
filter_key_list = []
def getKey(item):
    return item['Folder'] + ', ' + item['Filename']
for arg_str in sys.argv[1:]:
    if (arg_str == "-h" or arg_str == "--help"):
        print_usages()
    if (arg_str.startswith("--filter")):
        if arg_str.endswith(",0"):
            filter_idx = 0
        elif arg_str.endswith(",1"):
            filter_idx = 1
        else:
            print("Invalid filter index!")
            print_usages()
        filter_csv = arg_str.split("=")[1].split(",")[0]
        assrt_file_exist(filter_csv)
        filter_data = csv_to_list_of_dict(filter_csv)
        for filter_item in filter_data:
            filter_key_list.append(getKey(filter_item))
        continue
    file = arg_str
    assrt_file_exist(file)
    files.append(file)
data_arr = []

file_num = len(files)
base_len = len(csv_to_list_of_dict(files[0]))

uni_solved = {}
for file in files:
    uni_solved[parseFilename(file)]=[]
    data = csv_to_list_of_dict(file)
    if len(data) != base_len:
        raise ValueError(file + ":\t lines of this file is not the same as others!")
    data_arr.append(data)


print("Folder", "Filename", "Result", sep=", ")
for i in range(base_len):
    solved_num = 0
    _solved_file = ''
    _result = data[i]['Result']
    _folder = data[i]['Folder']
    _filename = data[i]['Filename']
    _key = getKey(data[i])
    if filter_idx == 0 and _key in filter_key_list:
        continue
    if filter_idx == 1 and _key not in filter_key_list:
        continue
    for j in range(file_num):
        data = data_arr[j]
        result = data[i]['Result']
        folder = data[i]['Folder']
        filename = data[i]['Filename']
        if result == 'Unrealizable' or result == 'Realizable':
            solved_num += 1
            _solved_file = files[j]
            _result = result
            _folder = folder
            _filename = filename
    if solved_num == 1:
        _tmp_dict = {}
        _tmp_dict["result"]=_result
        _tmp_dict["folder"]=_folder
        _tmp_dict["filename"]=_filename
        uni_solved[parseFilename(_solved_file)].append(_tmp_dict)


for file in files:
    csv_id = parseFilename(file)
    uni_solved_num = len(uni_solved[parseFilename(file)])
    print(f"{csv_id:>24}:\t{uni_solved_num}")
print()
for file in files:
    print(parseFilename(file), ':')
    _uni_solved = uni_solved[parseFilename(file)]
    for item in _uni_solved:
        _result = item["result"]
        _folder = item["folder"]
        _filename = item["filename"]
        print("\t{:<36}{}".format(_folder+', '+_filename, _result))
