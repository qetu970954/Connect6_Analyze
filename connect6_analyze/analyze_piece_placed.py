import json
import pathlib
import plotly.figure_factory as ff
from tqdm import tqdm
import gzip
import numpy as np


visit_count_for_each_grid = np.zeros(shape=(19, 19))

game_count = 0


def create_figure():
    text = np.around(visit_count_for_each_grid / visit_count_for_each_grid.sum(), decimals=4)
    result = ff.create_annotated_heatmap(visit_count_for_each_grid, annotation_text=text, hoverinfo='z')
    result.update_layout(width=1000, height=1000)
    # Make text size smaller
    for i in range(len(result.layout.annotations)):
        result.layout.annotations[i].font.size = 12
    return result


for a_json_archive_path in tqdm(sorted(pathlib.Path("../RECORD_LOAD_DIR/").glob("*.json.gz"))):
    with gzip.open(a_json_archive_path, "r") as f:
        try:
            data = json.loads(f.read().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            continue
        for game in data["BatchOfPositions"]:
            for position in game:
                x, y = position % 19, position // 19
                visit_count_for_each_grid[x, y] += 1
            game_count += 1

    if game_count % 500000 == 0:
        fig = create_figure()
        fig.write_html(f"visit_map_when_games_reach_{game_count}.html")

fig = create_figure()
fig.update_layout(title_text=f"There're {game_count} games been calculated!")
fig.write_html(f"visit_map_final.html")
