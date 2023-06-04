import os

def backend_folder_path():
    return os.getcwd()


def keypoints_dataset_path():
    return backend_folder_path() + '/data/datasets/keypoints.csv'


def keypoints_tflite_model_path():
    return backend_folder_path() + '/data/models/keypoints.tflite'