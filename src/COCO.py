import os.path
from pathlib import Path
import sys
import skimage.io
import numpy as np
import math
import glob
import json
import shutil
import ntpath

path_to_script = Path("~/projects/scaffan/").expanduser()
sys.path.insert(0, str(path_to_script))
import scaffan.image
from datetime import date


def get_image_properties(jpg_dataset_directory: Path):
    """
    Returns the properties of the images (list of dictionaries) which are obligatory in COCO data format
    For example (properties of one image):
        image {
            "id": int,
            "width": int,
            "height": int,
            "file_name": str,
        }

    :param jpg_dataset_directory: path to .jpg images
    :return: list of dictionaries
    """
    image_name = 0
    list_image_dictionaries = []
    image_name_id = 0

    images_names = list(Path(jpg_dataset_directory).glob('*.jpg'))

    index = 0
    while index < len(images_names):
        filename_string = os.path.join(jpg_dataset_directory, images_names[index])
        filename_path = Path(filename_string)
        if not filename_path.exists():
            break
        image = skimage.io.imread(filename_string)
        height = image.shape[0]
        width = image.shape[1]

        image_dictionary = {
            "id": image_name_id,
            "width": width,
            "height": height,
            "file_name": ntpath.basename(images_names[index]),
        }
        list_image_dictionaries.append(image_dictionary)

        image_name += 1
        image_name_id += 1
        index += 1

    return list_image_dictionaries


def get_category_properties(dataset_directory: Path, filename: str):
    """
    Returns properties of category (list of dictionaries)
    It can read categories from .txt file, if each category is on a single line without commas
    For example (properties of one category):
        category {
            "id": int,
            "name": str,
            "supercategory": str,
        }

    :param dataset_directory: path to .jpg images
    :param filename: filename of .txt file
    :return: list of dictionaries
    """
    list_category_dictionaries = []
    with open(str(dataset_directory) + "\\" + filename) as f:
        lines = f.readlines()
    number_lines = len(lines)
    f.close()

    for i in range(number_lines):
        supercategory = lines[i].rstrip()
        category_dictionary = {
            "id": i + 1,
            "name": supercategory,
            "supercategory": supercategory,
        }
        list_category_dictionaries.append(category_dictionary)

    return list_category_dictionaries


def count_polygon_area(x, y):
    """
    Counts the area of an polygon
    :param x: np.array(x_px_list)
    :param y: np.array(y_px_list)

    :return: area
    """
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def get_annotations_properties(czi_files_directory: Path, pixelsize_mm: list):
    """
    Returns the properties of the annotations (list of dictionaries)
    One dictionary = object instance annotation
    For example (one annotation):
        annotation{
            "id": int,
            "image_id": int, (the ID of a picture where the annotation is located)
            "category_id": int,
            "segmentation": RLE or [polygon],
            "area": float,
            "bbox": [x,y,width,height],
            "iscrowd": 0 or 1,
        }

    :param czi_files_directory: path to .czi files directory
    :param pixelsize_mm: defines pixelsize in mm (e.g. pixelsize = [[0.0003, 0.0003])
    :return: list of dictionaries
    """

    index = 0
    annotation_id = 1
    category_id = 1  # only one category
    image_id = 0

    list_annotation_dictionaries = []

    annotation_names = os.listdir(czi_files_directory)

    while index < len(annotation_names):
        filename_string = os.path.join(czi_files_directory, annotation_names[index])
        filename_path = Path(filename_string)
        if not filename_path.exists():
            break

        anim = scaffan.image.AnnotatedImage(path=str(filename_path))
        view = anim.get_full_view(
            pixelsize_mm=[0.0003, 0.0003]
        )  # wanted pixelsize in mm in view
        annotations = view.annotations

        for j in range(len(annotations)):
            xy_px_list = []

            x_px_list = (np.asarray(annotations[j]["x_mm"]) / pixelsize_mm[0]).tolist()
            y_px_list = (np.asarray(annotations[j]["y_mm"]) / pixelsize_mm[1]).tolist()

            x_px_min = float(math.floor(np.min(x_px_list)))
            y_px_min = float(math.floor(np.min(y_px_list)))
            width = float(math.floor(np.max(x_px_list)) - x_px_min)
            height = float(math.floor(np.max(y_px_list)) - y_px_min)

            bbox = [x_px_min, y_px_min, width, height]

            # polygon_area = count_polygon_area(np.array(x_px_list) * 0.0003, np.array(y_px_list) * 0.0003) # in mm
            polygon_area = count_polygon_area(
                np.array(x_px_list), np.array(y_px_list)
            )  # in pixels
            x_px_list = np.asarray(x_px_list)
            for i in range(len(x_px_list)):
                xy_px_list.append(x_px_list[i])
                xy_px_list.append(y_px_list[i])

            segmentation = xy_px_list

            # segmentation[0::2]
            # segmentation[1::2]
            # np.max(x_px_list)

            annotation_dictionary = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": [segmentation],  # RLE or [polygon]
                "area": polygon_area,  # Shoelace formula
                "bbox": bbox,  # [x, y, width, height]
                "iscrowd": 0,
            }
            annotation_id += 1

            list_annotation_dictionaries.append(annotation_dictionary)

        image_id += 1
        index += 1

    return list_annotation_dictionaries


def get_info_dictionary(version: str, description: str, contributor: str):
    """
    Returns dictionary with the basic information related to COCO dataset

    :param version: str
    :param description: str
    :param contributor: str
    :return: info dictionary
    """

    info_dictionary = {
        "year": str(date.today().year),
        "version": version,
        "description": description,
        "contributor": contributor,
        "date_created": date.today().strftime("%d/%m/%Y"),
    }
    return info_dictionary



def create_COCO_json(czi_directory: Path, images_directory: Path):
    """
    Creates dictionary (json) which is obligatory for COCO dataset
    :param czi_directory: Path to .czi files directory
    :param images_directory: Path to .jpg files directory
    :return: Dictionary
    """

    data = {}

    """
    Info
    """
    version = "1.0"
    description = "COCO dataset for scaffan"
    contributor = "Jan Burian"

    info_dictionary = get_info_dictionary(version, description, contributor)
    data.update({"info": info_dictionary})

    """
    Images
    """
    list_image_dictionaries = get_image_properties(images_directory)
    data.update({"images": list_image_dictionaries})

    """
    Categories
    """
    list_category_dictionaries = get_category_properties(
        images_directory, "categories.txt"
    )  # directory and .txt file
    data.update({"categories": list_category_dictionaries})

    """
    Annotations
    """
    pixelsize_mm = [0.0003, 0.0003]
    list_annotation_dictionaries = get_annotations_properties(
        czi_directory, pixelsize_mm
    )
    if (len(list_annotation_dictionaries) == 0):
        print('Warning: no annotations in .czi files.')

    data.update({"annotations": list_annotation_dictionaries})

    return data

def create_directory(directory_name: str):
    """
    Creates directory with specified directory name
    :param directory_name:
    :return:
    """
    files_directory = os.path.join(Path(__file__).parent, directory_name)
    if not os.path.exists(files_directory):
        os.makedirs(files_directory, exist_ok=True)
    return files_directory

def copy_images(source_dir: Path, COCO_dir_name: str):
    """
    Copies images from source directory to COCO directory
    :param source_dir: Path to source directory (Path)
    :param COCO_dir_name: Name of COCO dataset directory
    :return:
    """
    os.mkdir(os.path.join(Path(__file__).parent, COCO_dir_name, "../images"))
    destination_dir = os.path.join(Path(__file__).parent, COCO_dir_name, "../images")

    images_names = list(Path(source_dir).glob('*.jpg'))

    index = 0
    while index < len(images_names):
        image_name = images_names[index]
        full_file_name = os.path.join(source_dir, image_name)
        if os.path.exists(full_file_name):
            shutil.copy(full_file_name, destination_dir)
            index += 1


def create_COCO_dataset(czi_files_directory: Path, images_directory: Path, COCO_name: str):
    """
    Creates COCO dataset
    :param czi_files_directory: Path to .czi files directory
    :param images_directory: Path to .jpg files directory
    :param COCO_name: Name of COCO dataset directory
    :return:
    """
    name_json = "trainval.json"
    json_COCO = create_COCO_json(czi_files_directory, images_directory)

    COCO_directory = create_directory(COCO_name)

    # Creating .json file
    with open(os.path.join(COCO_directory, name_json), "w", encoding="utf-8") as f:
        json.dump(json_COCO, f, ensure_ascii=False, indent=4)
        f.close()

    copy_images(images_directory, COCO_name)