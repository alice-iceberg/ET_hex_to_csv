#  region imports and constants
import os
from datetime import datetime
import zipfile
from pathlib import Path
from bytesize import ByteSize

BACKUP_HEX_PATH = "D:\\IITP\\Data\\Backup\\Hex"
BACKUP_UTF_PATH = "D:\\IITP\\Data\\Backup\\Utf"
BACKUP_SIZE_CSV_PATH = "tools\\backup_size.csv"

CQLSH_FILENAME = "_mnt_storage_ET_data_query.cqlsh"

PARTICIPANTS_NUM = 774
CAPTURED_PHOTOS_ID = 25

DATA_SOURCE_ID_LIST = [1, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 80, 81]


#  endregion

# region general utils

def get_today_date(format='%Y-%m-%d'):
    return datetime.today().strftime(format)


# endregion

# region file management utils

def get_today_zip_hex_path():
    zip_hex_path_list = []
    today_date = get_today_date()
    subdir_list = os.listdir(BACKUP_HEX_PATH)
    for _dir in subdir_list:
        if _dir.__contains__(today_date):
            zip_hex_path_list.append(f'{BACKUP_HEX_PATH}\\{_dir}')
    return zip_hex_path_list


def get_today_hex_path():
    today_date = get_today_date()
    subdir_list = os.listdir(BACKUP_HEX_PATH)
    return f'{BACKUP_HEX_PATH}\\{[_dir for _dir in subdir_list if _dir.__contains__(today_date) and not _dir.__contains__(".zip")][0]}'


def get_today_utf_path():
    today_date = get_today_date()
    subdir_list = os.listdir(BACKUP_HEX_PATH)
    return f'{BACKUP_UTF_PATH}\\{[_dir for _dir in subdir_list if _dir.__contains__(today_date) and not _dir.__contains__(".zip")][0]}'


def unzip_hex_dir(input_dir, output_dir):
    print('Unzipping directory: ', input_dir)
    with zipfile.ZipFile(input_dir, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


def path_exist(path):
    return True if os.path.exists(path) else False


def get_dir_num_files(directory):
    path = f'{directory}'
    return len(os.listdir(path))


def get_folder_size(folder):
    return ByteSize(sum(file.stat().st_size for file in Path(folder).rglob('*')))


def create_dir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_cqlsh_from_list(filename_list):
    if CQLSH_FILENAME in filename_list:
        filename_list.remove(CQLSH_FILENAME)
    return filename_list
#  endregion
