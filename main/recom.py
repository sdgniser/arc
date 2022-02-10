import os
import pandas as pd

if os.path.exists('recom_data.csv') == False:
    with open('recom_data.csv', 'w') as fp:
        fp.write("Files")

def get(user_id):
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
        
        else:
            return []
        
    else:
        df[user_id] = [0]*len(df)
        df.to_csv('recom_data.csv')
        return []
    
def change(value):
    value = round((value*0.8), 2)
    return value

def update(file, user_id):
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
    return 'updated successfully'