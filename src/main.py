from pathlib import Path
import os

# Modules import
from src import COCO, czi_to_jpg

if __name__ == '__main__':

    # Loading .czi annotations
    path_annotations = Path(
        r"H:\BP\data\testovaci\czi_files_train"
    )  # path to main directory, that is where .czi files are

    # Creating .jpg dataset
    czi_to_jpg.export_czi_to_jpg(path_annotations, "images")
    czi_to_jpg.define_category(["cell nucleus"])

    # Creating COCO
    data = COCO.create_COCO_dataset(path_annotations, os.path.join(Path(__file__).parent, "../images"), "COCO")
    print()