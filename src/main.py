from pathlib import Path
import os

# Modules import
import COCO, czi_to_jpg

if __name__ == '__main__':

    # Loading .czi annotations
    '''
     path_annotations = Path(
        r"G:\.shortcut-targets-by-id\1IVZeSnsqd_jKJBXN8-AfD6JqiQ14QWVX\Anicka - reticular fibers\J7_5"
    )  # path to main directory, that is where .czi files are

    '''

    path_annotations = Path(
        r"H:\BP\data\dataset_blue\czi_files_train"
    )  # path to main directory, that is where .czi files are

    if os.path.exists(path_annotations):
        # Creating .jpg dataset
        czi_to_jpg.export_czi_to_jpg(path_annotations, "images")
        czi_to_jpg.define_category(["cell nucleus"])

        # Creating COCO
        data = COCO.create_COCO_dataset(path_annotations, os.path.join(Path(__file__).parent, "images"), "COCO_dataset")
        COCO.create_zip_directory(os.path.join(Path(__file__).parent, "COCO"), ("COCO_dataset.zip"))
        print()
    else:
        print(f" Path: {path_annotations} does not exist.")