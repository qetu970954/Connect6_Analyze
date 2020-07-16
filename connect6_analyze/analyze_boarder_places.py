import json
import pathlib
import gzip
import plotly.graph_objects as go
from tqdm import tqdm
from collections import Counter

game_count = 0
EAST_BOARDER, east_counter = list(range(18, 361, 19)), Counter({i: 0 for i in range(19)})
WEST_BOARDER, west_counter = list(range(0, 361, 19)), Counter({i: 0 for i in range(19)})
SOUTH_BOARDER, south_counter = list(range(19 * 18, 361)), Counter({i: 0 for i in range(19)})
NORTH_BOARDER, north_counter = list(range(19)), Counter({i: 0 for i in range(19)})

for a_json_archive_path in tqdm(sorted(pathlib.Path("../RECORD_LOAD_DIR/").glob("*.json.gz"))):
    with gzip.open(a_json_archive_path, "r") as f:
        try:
            data = json.loads(f.read().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            continue

        for game in data["BatchOfPositions"]:
            piece_count = sum([1 for _ in game if _ in EAST_BOARDER])
            east_counter[piece_count] += 1

            piece_count = sum([1 for _ in game if _ in WEST_BOARDER])
            west_counter[piece_count] += 1

            piece_count = sum([1 for _ in game if _ in SOUTH_BOARDER])
            south_counter[piece_count] += 1

            piece_count = sum([1 for _ in game if _ in NORTH_BOARDER])
            north_counter[piece_count] += 1

            game_count += 1

fig = go.Figure()
fig.add_trace(go.Bar(x=list(east_counter.keys()), y=list(east_counter.values()), name="East Boarder"))
fig.add_trace(go.Bar(x=list(west_counter.keys()), y=list(west_counter.values()), name="West Boarder"))
fig.add_trace(go.Bar(x=list(south_counter.keys()), y=list(south_counter.values()), name="South Boarder"))
fig.add_trace(go.Bar(x=list(north_counter.keys()), y=list(north_counter.values()), name="North Boarder"))
fig.update_layout(title_text=f"There're {game_count} games been calculated!")
fig.write_html(f"boader_piece.html")
