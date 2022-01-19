import pandas as pd

from tools import ANDROID_PID_LIST, IOS_PID_LIST
from tools import DATA_SOURCE_SAMPLING_RATES

pid_list = []


def get_expected_number_of_samples(df, sampling_rate):
    if not len(df) > 0:
        return 0
    start_timestamp = df['timestamp'].iloc[0]
    end_timestamp = df['timestamp'].iloc[-1]  # todo check timestamp

    filled_timestamps = []
    timestamp = start_timestamp
    while timestamp < end_timestamp:
        filled_timestamps.append(timestamp)
        timestamp = timestamp + sampling_rate

    return len(filled_timestamps)

from tqdm import tqdm
def missing_data_check():
    df_out = pd.DataFrame()
    df_out['PID'] = pid_list

    for name, value in tqdm(DATA_SOURCE_SAMPLING_RATES.items()):
        output_filename = f'missing_data/{name}.csv'
        df_missing = pd.DataFrame()
        missing_rate_list = []
        for pid in pid_list:
            df = pd.read_csv(f'campaign5_12-24-2021/5-{pid}/{pid}_{value[0]}.csv')
            expected_number =get_expected_number_of_samples(df, value[1])
            if expected_number!=0:
                missing_rate_list.append(round(len(df) / expected_number, 2))
            else:
                missing_rate_list.append('N/A')
        df_missing['pid'] = pid_list
        df_missing[f'{name}_missing'] = missing_rate_list
        df_missing.to_csv(output_filename, index=False)



