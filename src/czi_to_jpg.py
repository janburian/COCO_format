from pathlib import Path
import sys
import skimage.io
import os


path_to_script = Path("~/projects/scaffan/").expanduser()
sys.path.insert(0, str(path_to_script))
import scaffan.image
import imma.image


def get_filenames(path: Path):
    """
    Returns list of filenames
    :param path: path to directory
    :return: list of filenames
    """
    filenames = os.listdir(path)

    return filenames


def create_directory(directory_name: str):
    """
    Creates directory with defined name
    :param directory_name: str
    :return:
    """
    files_directory = os.path.join(Path(__file__).parent, directory_name)
    if not os.path.exists(files_directory):
        os.makedirs(files_directory, exist_ok=True)
    return files_directory


def export_czi_to_jpg(czi_directory_path: Path, imgs_directory_name: str):
    """
    Exports .czi files to .jpgs
    :param czi_directory_path: Path to .czi files directory
    :param imgs_directory_name: Name of images directory
    :return: None
    """
    images_directory = create_directory(imgs_directory_name)

    czi_files_names = get_filenames(czi_directory_path)

    index = 0
    while index < len(czi_files_names):
        fn_path = Path(os.path.join(Path(__file__).parent, czi_directory_path, czi_files_names[index]))
        fn_str = str(fn_path)
        if not fn_path.exists():
            break
        print(f"filename: {fn_path} {fn_path.exists()}")

        anim = scaffan.image.AnnotatedImage(path=fn_str)

        view = anim.get_full_view(
            pixelsize_mm=[0.0003, 0.0003]
        )  # wanted pixelsize in mm in view
        img = view.get_raster_image()
        skimage.io.imsave(os.path.join(images_directory, str(index).zfill(4) + ".jpg"), img)
        index += 1


def define_category(categories: list):
    """
    Creates .txt file with categories
    :param categories:
    :return:
    """
    txt_file_path = os.path.join(Path(__file__).parent, "../images", "categories.txt")
    with open(txt_file_path, 'w') as f:
        f.write('\n'.join(categories))
    f.close()