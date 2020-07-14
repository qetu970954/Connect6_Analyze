import yaml
import os
import pathlib
import json
import argparse

def yaml2json(zipped_yaml):
    os.system(f"gunzip {zipped_yaml}")
    unzipped_yaml_path = pathlib.Path(f"{zipped_yaml.parent}/{zipped_yaml.stem}")
    json_out_path = pathlib.Path(unzipped_yaml_path.as_posix()[:-3] + "json")

    with unzipped_yaml_path.open() as yaml_in:
        data = yaml.safe_load(yaml_in)
        json.dump(data, json_out_path.open("w"))

    os.system(f"gzip {unzipped_yaml_path}")
    return json_out_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert zipped yaml to json")
    parser.add_argument("yaml_file")
    args = parser.parse_args()
    yaml2json(pathlib.Path(args.yaml_file))
