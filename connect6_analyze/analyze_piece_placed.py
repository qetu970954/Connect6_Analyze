import json
import pathlib
import plotly.figure_factory as ff
from tqdm import tqdm
import os
import numpy as np


def create_figure(visit_count_for_each_grid):
    text = np.around(visit_count_for_each_grid / visit_count_for_each_grid.sum(), decimals=4)
    fig = ff.create_annotated_heatmap(visit_count_for_each_grid, annotation_text=text, hoverinfo='z')
    fig.update_layout(width=1000, height=1000)
    # Make text size smaller
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 12
    return fig


visit_count_for_each_grid = np.zeros(shape=(19, 19))

games_complete = 0

for a_json_archive_path in tqdm(sorted(pathlib.Path("../TEST/").glob("*.json.gz"))):
    os.system(f"gunzip {a_json_archive_path}")
    a_json_path = pathlib.Path(f"{a_json_archive_path.parent}/{a_json_archive_path.stem}")

    # find length of every episode
    with a_json_path.open() as f:
        data = json.load(f)
        for episode in data["BatchOfPositions"]:
            for position in episode:
                x, y = position % 19, position // 19
                visit_count_for_each_grid[x, y] += 1
            games_complete += 1

    os.system(f"gzip {a_json_path}")

    if games_complete % 10000 == 0:
        fig = create_figure(visit_count_for_each_grid)
        fig.write_html(f"visit_map_when_games_reach_{games_complete}.html")

fig = create_figure(visit_count_for_each_grid)
fig.write_html(f"visit_map_final.html")
