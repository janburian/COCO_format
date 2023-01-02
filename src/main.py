from pathlib import Path
import os
import argparse

# Modules import
import COCO, czi_to_jpg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='COCO format',
        description='Creates COCO from .czi files',
        epilog='Write a path to directory, where .czi files with annotations are saved.'
     )

    parser.add_argument('-p', '--path_czi', metavar='path_czi', type=str,
                        help='a path to directory, where .czi files with annotations are saved')

    parser.add_argument('-s', '--path_COCO', metavar='path_COCO', type=str,
                        help='a path to directory, where COCO will be saved')

    args = parser.parse_args()
    
    # From CMD
    path_annotations = args.path_czi
    path_COCO = args.path_COCO

    # Loading .czi annotations
    #path_annotations = Path(
        #r"H:\reticular_fibers_testovaci"
    #)  # path to main directory, that is where .czi files are
    #path_COCO = r"C:\Users\janbu\Desktop\moje_COCO"


    if os.path.exists(path_annotations):
        # Creating .jpg dataset
        czi_to_jpg.export_czi_to_jpg(path_annotations, "images")
        czi_to_jpg.define_category(["cell nucleus"])

        # Creating COCO
        data = COCO.create_COCO_dataset(path_annotations, os.path.join(Path(__file__).parent, "images"), "COCO_dataset")
        COCO.create_zip_directory(os.path.join(Path(__file__).parent, "COCO"), "COCO_dataset.zip")
        COCO.move_directory(os.path.join(Path(__file__).parent, "COCO_dataset"), path_COCO)

    else:
        print(f" Path: {path_annotations} does not exist.")