import src.czi_to_jpg
import pytest
from pathlib import Path

def test_read_reticular_fibers():
    src.czi_to_jpg.export_czi_to_jpg(r"H:\reticular_fibers_testovaci", "images")
    assert len(list(Path("src/images").glob("*"))) > 0