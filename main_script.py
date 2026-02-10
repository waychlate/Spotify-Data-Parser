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
df['date'] = df['ts'].dt.date
df['track_artist'] = df['master_metadata_track_name'] + " by " + df['master_metadata_album_artist_name']

top_5_songs = df.groupby('track_artist').size().reset_index(name='plays').sort_values(by='plays', ascending=False).head(5)
top_5_artists = df.groupby('master_metadata_album_artist_name').size().reset_index(name='plays').sort_values(by='plays', ascending=False).head(5)


col1, col2 = st.columns(2)

with col1:
    st.markdown("### *most listened songs*")
    for index, row in top_5_songs.iterrows():
        st.markdown(f"{row['track_artist']} | **Plays** {row['plays']}")

with col2:
    st.markdown("### *most listened artists*")
    st.table(top_5_artists)


st.markdown("### over the years..")
song_selected = st.selectbox(label='', options=df['track_artist'].unique(), placeholder='pick a song...')

song_df = df[df['track_artist'] == song_selected].copy()

# Count occurrences per day
daily_counts = song_df.groupby('date').size().reset_index(name='plays')
# Create a range of every single day from your first listen to your last
all_days = pd.date_range(start=daily_counts['date'].min(), end=daily_counts['date'].max())
# Reindex and fill missing days with 0
daily_counts = daily_counts.set_index('date').reindex(all_days, fill_value=0)

st.line_chart(daily_counts)