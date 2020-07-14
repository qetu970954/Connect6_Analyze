import json
import pathlib
import plotly.graph_objects as go
from tqdm import tqdm
import os

length_for_each_episode = []

for a_json_archive_path in tqdm(sorted(pathlib.Path("../TEST/").glob("*.json.gz"))):
    os.system(f"gunzip {a_json_archive_path}")
    a_json_path = pathlib.Path(f"{a_json_archive_path.parent}/{a_json_archive_path.stem}")

    # find length of every episode
    with a_json_path.open() as f:
        data = json.load(f)
        for game in data["BatchOfPositions"]:
            length_for_each_episode.append(len(game))

    os.system(f"gzip {a_json_path}")

    if len(length_for_each_episode) % 10000 == 0:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=length_for_each_episode[-10000:], marker={'color': '#666666'}))
        fig.write_html(f"histogram_{len(length_for_each_episode) - 10000}-{len(length_for_each_episode)}.html")

fig = go.Figure()
fig.add_trace(go.Histogram(x=length_for_each_episode, marker={'color': '#666666'}))
fig.write_html(f"histogram_all.html")
