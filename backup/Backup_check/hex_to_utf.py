import pandas as pd
import tools
from tqdm import tqdm
import concurrent.futures
import os


def convert_hex_str2str(filename):
    filename = f'{tools.get_today_hex_path()}\\{filename}'
    df = pd.read_csv(filename)
    if len(df) > 0:
        df.columns = ['id', 'timestamp', 'values']
        df = df.drop(df[df.id == tools.CAPTURED_PHOTOS_ID].index)  # removing photos data source

        df['values'] = df['values'].apply(lambda x: bytes.fromhex(x.split('0x')[1]).decode('utf-8'))
    else:
        df = pd.DataFrame(columns=['timestamp', 'values'])
    return df


def hex_to_csv(hex_filename):
    user_id = hex_filename.split('_usr')[1].split('.')[0]
    campaign_id = hex_filename.split('_cmp')[1].split('_')[0]
    user_directory = f'{tools.get_today_utf_path()}\\{campaign_id}-{user_id}'
    tools.create_dir_if_not_exist(user_directory)

    for data_source_id in tqdm(tools.DATA_SOURCE_ID_LIST):
        output_filename = f'{user_directory}\\{user_id}_{data_source_id}.csv'

        df = convert_hex_str2str(hex_filename)
        if len(df) > 0:
            df_source = df[df.id == data_source_id]
            df_source.drop('id', axis=1).to_csv(output_filename, index=False)
        else:
            df.to_csv(output_filename, index=False)  # empty df


def parallel_hex_to_csv(directory):
    user_hex_file_list = os.listdir(directory)
    user_hex_file_list = tools.remove_cqlsh_from_list(user_hex_file_list)
    # for filename in user_hex_file_list:
    #     hex_to_csv(filename)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for filename in tqdm(user_hex_file_list):
            executor.submit(hex_to_csv, filename)

