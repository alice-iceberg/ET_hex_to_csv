import concurrent.futures
import os

import pandas as pd
from tqdm import tqdm
import tools

import data_check
from process import process_raw_data


def accuracy_results(filename):
    df = pd.read_csv(filename)
    # df.sort_values(by=['ACC', 'ACC_BAL', 'WIN'], inplace=True)
    # df.to_csv(filename)
    df = df.query('ACC_BAL<=0.05')
    count = df['pid'].value_counts()
    count = count.sort_values(ascending=False)
    count.to_csv('test.csv')


def correlation_with_label(filename):
    output_filename = filename.split('.')[0] + '_corr.csv'
    df = pd.read_csv(filename)
    df_corr = df.corr(method='spearman')
    df_corr_columns = list(df_corr.columns)
    df_corr_columns.remove('depressed')
    df_corr.drop(columns=df_corr_columns, inplace=True)
    df_corr.sort_values(by=['depressed'], ascending=False, inplace=True)
    df_corr.to_csv(output_filename)


def create_feature_names_file(filename):
    df = pd.read_csv(filename)
    cols = df.columns
    print(cols)


def get_missing_values_percentage(filename):
    df = pd.read_csv(filename)
    df_miss = df.isnull().sum() / len(df)
    df_miss = df_miss.sort_values(ascending=False)
    df_miss.to_csv('FS_missing_campaign_4_5-WIN_2.csv')


def main():
    pid_list = tools.IOS_PID_LIST
    pid_list.extend(tools.ANDROID_PID_LIST)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pid in tqdm(pid_list):
            filename = f'_mnt_storage_ET_data_cmp5_usr{pid}.csv'
            executor.submit(process_raw_data, [f'campaign5_rawdata-01_07/{filename}', '01-07-2022'])


if __name__ == '__main__':
    main()
