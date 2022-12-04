import os
import shutil
from pathlib import Path

def delete_content_folder(path_folder: Path):
    """
    Deletes content from folder
    :param path_folder: Path to folder in which the content will be deleted
    :return: None
    """
    if os.path.exists(path_folder):
        for filename in os.listdir(path_folder):
            file_path = os.path.join(path_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def delete_zip_files():
    """
    Deletes .zip files
    :return:
    """
    dir_name = os.path.join(Path(__file__).parent)
    files = os.listdir(dir_name)

    for file in files:
        if file.endswith(".zip"):
            os.remove(os.path.join(dir_name, file))