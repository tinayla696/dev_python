import argparse
import os
from pathlib import Path
import shutil
import sys

import cv2
import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt

# Parge argument
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", "-c",
        type=str,
        required=True,
        help="[--config][-c] config file path."
    )
    args = parser.parse_args()
    return args


# Read config file
def load_config(yaml_file_path):
    with open(yaml_file_path, 'r') as yml:
        config = yaml.safe_load(yml)
    return config


# Re: Generater
def regenerater(folder_path):
    if Path(folder_path).is_dir():
        shutil.rmtree(
            path=folder_path,
            ignore_errors=False,
        )
        
    os.makedirs(
        name=folder_path,
        exist_ok=True
    )
    return


# Convert csv -> image(png or jpg)
def csvToimage(config):
    # config.camera entries
    for topview, info_dict in config['camera'].items():
        csvFolderPath = config['postproc']['csv_dir']
        csvList = [Path(csvFolderPath, f'{mac_addr}.csv') for mac_addr in info_dict['camera_meta'] if Path(csvFolderPath, f'{mac_addr}.csv').is_file()]

        # Non .csv
        if len(csvList) == 0:
            continue

        # Generate map_frame_image
        generate_iamges(
            topView=topview,
            csvList=csvList,
            config=config
        )
    return


# Generate map_frame_image
def generate_iamges(topView, csvList, config):
    csvDataList = []
    for csvFile in csvList:
        macAddr = csvFile.stem
        csvData = pd.read_csv(
            filepath_or_buffer=csvFile
        )

        csvData['mac_address'] = macAddr
        csvDataList.append(csvData)

    resultCsvData = pd.concat(csvDataList, axis=0, sort=True)
    del csvData

    # Extraction frame data
    frameList = list(resultCsvData['frame_index'].uniqure())
    for frameIndex in frameList:
        outputFile = Path(config['postproc']['video_images_dir'], f'{topView}{str(frameIndex).zfill(8)}.jpeg')

        # Select temp_file
        if outputFile.is_file():
            topview_image_file = str(outputFile)
        else:
            topview_image_file = config['camera'][topView]['top_view_image']['image_path']

        topview_image_data = cv2.imread(
            filename=topview_image_file,
        )
        data = resultCsvData[resultCsvData['frame_index'] == frameIndex]

        draw_image(
            data=data,
            topview_image_data=topview_image_data,
            topview=topView,
            output_image_file_path=outputFile,
            config=conifig,
        )
    return


# draw_image func
def draw_image(data, topview_image_data, topview, output_image_file_path, config):
    # TODO：ここに算出ロジックを描く

    return


# Callback
# Pythonってコールバック最後に書かないといけないのか
if __name__ == '__main__':
    args = parser()
    config = load_config(
        yaml_file_path=args.config,
    )

    regenerater(
        folder_path=config['postproc']['video_images_dir'],
    )

    csvToimage(
        config=config,
    )