import os

import bytesize
from bcolors import Bcolors
import tools
import pandas as pd


def issues_check_pipeline(directory):
    today_date = tools.get_today_date()
    files_num = tools.get_dir_num_files(directory)
    dir_size = tools.get_folder_size(directory)

    today_stats_row = {'date': today_date, 'files_num': files_num, 'total_size': dir_size}

    # checking number of backed-up participants
    if files_num != tools.PARTICIPANTS_NUM+1:
        print(f'{Bcolors.WARNING}WARNING: Backed up {files_num}/{tools.PARTICIPANTS_NUM + 1} participants {Bcolors.ENDC}')
    else:
        print(f'{Bcolors.OKGREEN}SUCCESS: Backed up {files_num}/{tools.PARTICIPANTS_NUM + 1} participants {Bcolors.ENDC}')

    # checking and recording total directory size
    if tools.path_exist(tools.BACKUP_SIZE_CSV_PATH):
        df_size = pd.read_csv(tools.BACKUP_SIZE_CSV_PATH)
        prev_size = df_size['total_size'].iloc[-1]
    else:
        df_size = pd.DataFrame(columns=['date', 'files_num', 'total_size'])
        prev_size = 0

    df_size = df_size.append(today_stats_row, ignore_index=True)
    df_size.to_csv(tools.BACKUP_SIZE_CSV_PATH, index=False)

    if dir_size <= prev_size:
        print(f'{Bcolors.WARNING}WARNING: Please check the file sizes.The total size changed from {prev_size} to {dir_size} {Bcolors.ENDC}')
    else:
        print(f'{Bcolors.OKGREEN}SUCCESS: The total size changed from {prev_size} to {dir_size} {Bcolors.ENDC}')



