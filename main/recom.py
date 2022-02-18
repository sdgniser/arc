import os
import pandas as pd
import fasteners


# Function to check if the file to store the data already exist or not
# if not then create one.
def start():
    if not os.path.exists('recom_data.csv'):
        with open('recom_data.csv', 'a') as fp:
            fp.write("Files")


lock = fasteners.InterProcessLock('recom_data.csv')
start()


# Function to get the list of recommended files for a user
def get_recom(user_id):
    user_id = str(user_id)
    df = pd.read_csv('recom_data.csv', index_col='Files')
    
    if user_id in df.columns:
        if len(df)>0:
            corr = df.corr()[user_id]
            wght = df*corr
            wght = wght.loc[:, wght.columns != user_id]

            wght['mean'] = wght.mean(axis=1)

            final = wght[['mean']]
            final = final.sort_values(by=['mean'], ascending=False)[:10]

            return final.index.tolist()   
        
        return []
        
    else:
        lock.acquire()
        
        df = pd.read_csv('recom_data.csv', index_col='Files')
        df[user_id] = [0]*len(df)
        df.to_csv('recom_data.csv')
        
        lock.release()
        return []


def change(value):
    value = round((value*0.8), 2)
    return value


# Function to update the list of files accessed by user
def update(file, user_id):
    lock.acquire()
    
    user_id = str(user_id)
    df = pd.read_csv('recom_data.csv', index_col='Files')
    
    if file in df.index:
        if user_id in df.columns:
            df[user_id] = df[user_id].apply(change)
            df.loc[[file],[user_id]] = 10
        else:
            df[user_id] = [0]*len(df)
            df.loc[[file],[user_id]] = 10
    else:
        if user_id in df.columns:
            df.loc[file] = [0]*len(df.columns)
            df[user_id] = df[user_id].apply(change)
            df.loc[[file],[user_id]] = 10
        else:
            df[user_id] = [0]*len(df)
            df.loc[file] = [0]*len(df.columns)
            df.loc[[file],[user_id]] = 10

    df.to_csv('recom_data.csv')

    lock.release()
    return 'updated successfully'
