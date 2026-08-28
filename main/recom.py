"""
Python file to handle the recommendation system.
"""

import os
import pandas as pd

# Dynamically get the directory where recom.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create an absolute path for the CSV file
CSV_PATH = os.path.join(BASE_DIR, "recom_data.csv")


def start():
    """
    Function to check if the file to store the user file access data
    already exists or not, if not then create one.
    """
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "a") as fp:
            fp.write("Files")

    global df, val_count
    val_count = 0
    df = pd.read_csv(CSV_PATH, index_col="Files")


start()  # Call the start function


def get_recom(user_id):
    """
    Function to get the list of recommended files for a given user.
    """
    user_id = str(user_id)

    if user_id in df.columns:
        if len(df) > 0:
            corr = df.corr()[user_id]
            wght = df * corr
            wght = wght.loc[:, wght.columns != user_id]

            wght["mean"] = wght.mean(axis=1)
            final = wght[["mean"]]
            final = final.sort_values(by=["mean"], ascending=False)[:10]

            return final.index.tolist()

        return []

    else:
        df[user_id] = [0] * len(df)
        return []


def update(file, user_id):
    """
    Function to update the list of files accessed by user.
    """
    user_id = str(user_id)

    if user_id in df.columns:
        df[user_id] = df[user_id].apply(lambda x: round((x * 0.8), 2))
    else:
        df[user_id] = [0] * len(df)

    if file not in df.index:
        df.loc[file] = [0] * len(df.columns)

    df.loc[[file], [user_id]] = 10

    global val_count
    val_count += 1

    if val_count >= 5:
        # Update to use the absolute path when saving!
        df.to_csv(CSV_PATH)
        val_count = 0