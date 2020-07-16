import json
import pathlib
import gzip
import plotly.graph_objects as go
from tqdm import tqdm

length_for_each_game = []

for a_json_archive_path in tqdm(sorted(pathlib.Path("../RECORD_LOAD_DIR/").glob("*.json.gz"))):
    with gzip.open(a_json_archive_path, "r") as f:
        try:
            data = json.loads(f.read().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            continue

        for game in data["BatchOfPositions"]:
            length_for_each_game.append(len(game))

    if len(length_for_each_game) % 500000 == 0:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=length_for_each_game[-500000:], marker={'color': '#666666'}))
        fig.write_html(f"game_length_histogram_{len(length_for_each_game) - 500000}-{len(length_for_each_game)}.html")

fig = go.Figure()
fig.add_trace(go.Histogram(x=length_for_each_game, marker={'color': '#666666'}))
fig.update_layout(title_text=f"There're {len(length_for_each_game)} games been calculated!")
fig.write_html(f"game_length_histogram_all.html")
