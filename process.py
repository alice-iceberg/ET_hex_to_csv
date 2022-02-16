import os

import pandas as pd
from tqdm import tqdm

import tools


def convert_hex_str2str(filename):
    df = pd.read_csv(filename)
    if len(df) > 0:
        df.columns = ['id', 'timestamp', 'values']
        df = df.drop(df[df.id == tools.CAPTURED_PHOTOS_ID].index)  # removing photos data source

        df['values'] = df['values'].apply(lambda x: bytes.fromhex(x.split('0x')[1]).decode('utf-8'))
    else:
        df = pd.DataFrame(columns=['timestamp', 'values'])
    return df


def process_raw_data(args):
    input_filename = args[0]
    date = args[1]
    user_id = input_filename.split('data_')[2].split('_usr')[1].split('.')[0]
    device_os = 'Android' if int(user_id) in tools.ANDROID_PID_LIST else 'iOS'
    for data_source_id in tqdm(tools.DATA_SOURCE_ID_LIST):
        if not os.path.exists(f'campaign5_{date}/{device_os}/5-{user_id}'):
            os.makedirs(f'campaign5_{date}/{device_os}/5-{user_id}')

        output_filename = f'campaign5_{date}/{device_os}/5-{user_id}/{user_id}_{data_source_id}.csv'
        df = convert_hex_str2str(input_filename)
        if len(df) > 0:
            df_source = df[df.id == data_source_id]
            df_source.drop('id', axis=1).to_csv(output_filename, index=False)
        else:
            df.to_csv(output_filename, index=False)  # empty df


def convert_raw_data_to_image(input_filename):
    df = pd.read_csv(input_filename)
    df_source = df[df.id == 25]
    df_source = df_source.drop('id', axis=1)
