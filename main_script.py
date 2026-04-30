import streamlit as st
import pandas as pd
import os

directory = './data'
files = []

# Put the files in the directory in a list
for x in os.listdir('./data/'):
    if x.endswith(".json"):
        fullPath = os.path.join(directory, x) 
        files.append(fullPath)

# Connect each JSON file as a dataframe
df = pd.concat((pd.read_json(f) for f in files), ignore_index=True)
# Convert 'ts' to datetime 
df['ts'] = pd.to_datetime(df['ts'])
# df['date'] = df['ts'].dt.date
df['track_artist'] = df['master_metadata_track_name'] + " by " + df['master_metadata_album_artist_name']

df_artists = df.resample('W', on='ts')['master_metadata_album_artist_name'].agg(lambda x: x.mode().iloc[0] if not x.empty else None)

