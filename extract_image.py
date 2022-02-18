import base64
import os

import pandas as pd
from PIL import ImageFile

import tools

ImageFile.LOAD_TRUNCATED_IMAGES = True


def csv_to_image(user_folder):
    user_id = user_folder.split('-')[1]
    filename = f'campaign5_02-17-2022/iOS/{user_folder}/{user_id}_{tools.CAPTURED_PHOTOS_ID}.csv'

    if not os.path.exists(f'images/campaign5_02-17-2022/iOS/5-{user_id}'):
        os.makedirs(f'images/campaign5_02-17-2022/iOS/5-{user_id}')

    df = pd.read_csv(filename)
    df.columns = ['timestamp', 'values']

    M_smile = df['values'].str.contains('SMILE')
    M_position = df['values'].str.contains('POSITION')
    M_bytes_record = df['values'].str.contains('ByteString')
    df = df[~(M_smile | M_position | M_bytes_record)]

    for row in df.itertuples():
        image_encoded = row.values
        image_encoded = image_encoded.encode('utf-8')

        with open('encode.bin', "wb") as file:
            file.write(image_encoded)

        file = open('encode.bin', 'rb')
        byte = file.read()
        file.close()

        decodeit = open(f'images/campaign5_02-17-2022/iOS/5-{user_id}/{row.timestamp}.png', 'wb')
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()


def delete_csv_photo_files(directory):
    user_folder_list = os.listdir(directory)
    for user_folder in user_folder_list:
        user_id = user_folder.split('-')[1]
        filename = f'{directory}/{user_folder}/{user_id}_25.csv'
        os.remove(filename)