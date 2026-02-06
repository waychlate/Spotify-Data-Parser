import json
import os

songList = {}

def addSpotifyData(list):
    for dataItem in list:
        exists = False

        for song in songList: 
            if song['trackName'] == dataItem['master_metadata_track_name']:
                song['plays'] += 1
                exists = True
                break

        if not exists:
            songList.append({'trackName' : dataItem['master_metadata_track_name'], 'plays' : 1})

directory = './data'

for x in os.listdir('./data/'):
    if x.endswith(".json"):
        fullPath = os.path.join(directory, x)        

        with open(fullPath, 'r') as file:
            spotifyData = json.load(file) 

            for item in spotifyData:
                name = item.get('master_metadata_track_name')

                if name:
                    songList[name] = songList.get(name, 0) + 1 

# Convert to a list of tuples or dicts only when you need to sort
sorted_songs = sorted(songList.items(), key=lambda x: x[1], reverse=False)

print(sorted_songs)
