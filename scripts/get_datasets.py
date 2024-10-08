import os
import sys
import yaml
import checksumdir
import wget
import multiprocessing
import time
import gdown
import wget
import shutil


class FolderToDownload(multiprocessing.Process):
    def __init__(self, raw_yaml_folder_to_download, path_where_to_save, my_manager):
        super().__init__()
        self.download_link = raw_yaml_folder_to_download["download_link"]
        self.folder_name = raw_yaml_folder_to_download["folder_name"]
        self.google_drive = raw_yaml_folder_to_download["google_drive"]
        self.hash = raw_yaml_folder_to_download["hash"]
        self.size_in_GB = raw_yaml_folder_to_download["size_in_GB"]
        self.path_where_to_save = path_where_to_save
        self.manager = my_manager
        self.downloaded_kb = self.manager.Value('i', 0)
        self.all_kb = self.manager.Value('i', 0)

    def save_download_files(self, downloaded_kb, all_kb, _):
        self.downloaded_kb.value = downloaded_kb
        self.all_kb.value = all_kb

    @staticmethod
    def download_from_google_drive(url, destination):
        gdown.download_folder(url, output=destination, quiet=True)

    def download_with_wget(self, url, destination):
        wget.download(url, out=destination, bar=self.save_download_files)

    def run(self):
        if self.google_drive:
            self.download_from_google_drive(self.download_link, self.path_where_to_save)
        else:
            self.download_with_wget(self.download_link, self.path_where_to_save)


class Dataset:
    def __init__(self, raw_yaml_dataset, my_dataset_folder_path, my_manager):
        self.name = raw_yaml_dataset["name"]
        self.folders_to_download = []
        self.dataset_folder_path = os.path.join(my_dataset_folder_path, self.name)
        self.manager = my_manager
        for raw_folder_to_download in raw_yaml_dataset["folders_to_download"]:
            self.folders_to_download.append(FolderToDownload(raw_folder_to_download,
                                                             self.dataset_folder_path,
                                                             self.manager))

    def download(self):
        if os.path.exists(self.dataset_folder_path):
            shutil.rmtree(self.dataset_folder_path)
        os.mkdir(self.dataset_folder_path)
        for folder in self.folders_to_download:
            folder.start()
        if not self.folders_to_download[0].google_drive:
            while True:
                for folder in self.folders_to_download:
                    print(f"{folder.downloaded_kb.value}/{folder.all_kb.value}", end="#")
                all_done = True
                for folder in self.folders_to_download:
                    if folder.is_alive():
                        all_done = False
                if all_done:
                    break
                print()
        for folder in self.folders_to_download:
            folder.join()


if __name__ == "__main__":
    nut_stereo_event_root_folder = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(nut_stereo_event_root_folder)
    from nut_stereo_event.utils import check_python_version, green, red, yellow

    # Let's check python version
    check_python_version()
    # Let's check if a dataset folder is there
    dataset_folder_path = os.path.join(nut_stereo_event_root_folder, "dataset")
    if not os.path.exists(dataset_folder_path):
        print(red(f"ERROR: The dataset folder does not exist. Had you manually removed that after cloning?"))
        print(red("Get it there: https://github.com/Noce99/NutStereoEvent and try again!"))
        exit()
    # Let's check what is inside the dataset folder
    content_of_dataset_folder = os.listdir(dataset_folder_path)
    datasets_metadata = [
        {
            "name": "DSEC",
            "folders_to_download": [
                {
                    "folder_name": "train_events",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/train_coarse/train_events.zip",
                    "google_drive": False,
                    "size_in_GB": "125.0",
                    "hash": "??"  # md5hash = dirhash(directory, 'md5')
                },
                {
                    "folder_name": "train_images",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/train_coarse/train_images.zip",
                    "google_drive": False,
                    "size_in_GB": "216.0",
                    "hash": "??"
                },
                {
                    "folder_name": "train_disparity",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/train_coarse/train_disparity.zip",
                    "google_drive": False,
                    "size_in_GB": "12.0",
                    "hash": "??"
                },
                {
                    "folder_name": "train_optical_flow",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/train_coarse/train_optical_flow.zip",
                    "google_drive": False,
                    "size_in_GB": "3.7",
                    "hash": "??"
                },
                {
                    "folder_name": "train_semantic_segmentation",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/semantic/train_semantic_segmentation.zip",
                    "google_drive": False,
                    "size_in_GB": "0.1",
                    "hash": "??"
                },
                {
                    "folder_name": "train_calibration",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/train_coarse/train_calibration.zip",
                    "google_drive": False,
                    "size_in_GB": "0.0",
                    "hash": "??"
                },
                {
                    "folder_name": "test_events",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/test_coarse/test_events.zip",
                    "google_drive": False,
                    "size_in_GB": "27.0",
                    "hash": "??"
                },
                {
                    "folder_name": "test_images",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/test_coarse/test_images.zip",
                    "google_drive": False,
                    "size_in_GB": "43.0",
                    "hash": "??"
                },
                {
                    "folder_name": "test_semantic_segmentation",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/semantic/test_semantic_segmentation.zip",
                    "google_drive": False,
                    "size_in_GB": "0.0",
                    "hash": "??"
                },
                {
                    "folder_name": "test_calibration",
                    "download_link": "https://download.ifi.uzh.ch/rpg/DSEC/test_coarse/test_calibration.zip",
                    "google_drive": False,
                    "size_in_GB": "0.0",
                    "hash": "??"
                },
            ]
        },
        {
            "name": "MVSEC",
            "folders_to_download": [
                {
                    "folder_name": "outdoor_night",
                    "download_link": "https://drive.google.com/drive/folders/1SV6nQ-ONQmLnCo3aVQFtO6NJ7yXfSmvT?usp=drive_link",
                    "google_drive": True,
                    "size_in_GB": "??",
                    "hash": "??"
                },
                {
                    "folder_name": "indoor_flying",
                    "download_link": "https://drive.google.com/drive/folders/1CEuvvahWQntNIqXWZhXu_WknsTLm4Sum?usp=drive_link",
                    "google_drive": True,
                    "size_in_GB": "??",
                    "hash": "??"
                },
                {
                    "folder_name": "outdoor_day",
                    "download_link": "https://drive.google.com/drive/folders/1WUapfrd2DNQNuxPt9IqUHCcPCPKLiNvT?usp=drive_link",
                    "google_drive": True,
                    "size_in_GB": "??",
                    "hash": "??"
                },
                {
                    "folder_name": "motorcycle",
                    "download_link": "https://drive.google.com/drive/folders/1z9DfyFLVhkksJAP9h-pfr8ByewhYeRnu?usp=drive_link",
                    "google_drive": True,
                    "size_in_GB": "??",
                    "hash": "??"
                },
            ]
        }
    ]
    datasets_metadata_path = os.path.join(dataset_folder_path, "datasets_metadata.yaml")
    with open(datasets_metadata_path, 'w') as file:
        yaml.dump(datasets_metadata, file)

    with open(datasets_metadata_path, 'r') as file:
        datasets_metadata = yaml.safe_load(file)

    # From there is real code

    datasets = []
    manager = multiprocessing.Manager()
    for dataset_metadata in datasets_metadata:
        datasets.append(Dataset(dataset_metadata, dataset_folder_path, manager))

    datasets[0].download()

