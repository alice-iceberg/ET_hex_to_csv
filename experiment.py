import os

import pandas as pd
from sklearn.cluster import KMeans

symptom_cols = ['lack_of_interest', 'depressed_feeling', 'sleep_trouble', 'fatigue', 'poor_appetite',
                'negative_self_image', 'difficulty_focusing', 'bad_physchomotor_activity', 'suicide_thoughts']


def kmeans_clustering(filename):
    df = pd.read_csv(filename)
    df = df[df['phq'].notna()]
    kmeans = KMeans(n_clusters=2, random_state=0, init='k-means++').fit(df[symptom_cols].values)
    df['cluster_questions_2'] = kmeans.labels_
    kmeans = KMeans(n_clusters=3, random_state=0, init='k-means++').fit(df[symptom_cols].values)
    df['cluster_questions_3'] = kmeans.labels_
    kmeans = KMeans(n_clusters=4, random_state=0, init='k-means++').fit(df[symptom_cols].values)
    df['cluster_questions_4'] = kmeans.labels_

    df.to_csv(filename, index=False)


def check_missing_music():
    filenames = os.listdir('campaign5_11-26-2021/Android')
    print(len(filenames))
    counter = 0
    for filename in filenames:
        user_id = filename.split('-')[-1]
        df = pd.read_csv(f'campaign5_11-26-2021/Android/{filename}/{user_id}_24.csv')
        if len(df) == 0:
            counter += 1
    print(f'counter:', counter)
    print(counter/len(filenames))