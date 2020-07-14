# import json
# import pathlib
# import plotly.graph_objects as go
# import tqdm
#
# length_for_each_episode = []
#
# for a_json_archive in tqdm.tqdm(sorted(pathlib.Path("../RECORD_LOAD_DIR").glob("*.json.gz"))):
#     os.system(f"gunzip {a_json_archive}")
#     # find length of every episode
#     with a_json.open() as f:
#         data = json.load(f)
#         for game in data["BatchOfPositions"]:
#             length_for_each_episode.append(len(game))
#
# print(len(length_for_each_episode))
#
# fig = go.Figure()
# fig.add_trace(go.Histogram(x=length_for_each_episode, marker={'color': '#666666'}))
# fig.show()
