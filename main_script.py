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
df.info()
