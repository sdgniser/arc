"""
Python file to handle the recommendation system.
"""

import os
import pandas as pd


def start():
    """
    Start Function.

    Function to check if the file to store the user file access data
    already exists or not, if not then create one.

    Parameters:
    None

    Returns:
    None
    """
    if not os.path.exists("recom_data.csv"):
        with open("recom_data.csv", "a") as fp:
            fp.write("Files")

    global df, val_count
    val_count = 0
    df = pd.read_csv("recom_data.csv", index_col="Files")


start()  # Call the start function

def get_recom(user_id):
    """
    Get Recommendations Function.

    Function to get the list of recommended files for a given user.

    Parameters:
    user_id (int/str): Unique ID of the user

    Returns:
    list: A list of recommended files sorted in descending order of priority.
          With max length of list equals to 10.
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
    Update Funaction.

    Function to update the list of files accessed by user.

    Parameters:
    file (str): Name of the file being accessed by user.
    user_id (int/str): Unique ID of the user accessing the file.

    Returns:
    None

    """

    user_id = str(user_id)

    if user_id in df.columns:
        df[user_id] = df[user_id].apply(lambda x: round((x * 0.8), 2))
    else:
        df[user_id] = [0] * len(df)

    if file not in df.index:
        df.loc[file] = [0]*len(df.columns)

    df.loc[[file], [user_id]] = 10

    global val_count
    val_count += 1

    if val_count >= 5:
        df.to_csv("recom_data.csv")
        val_count = 0