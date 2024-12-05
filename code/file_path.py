from pathlib import Path

MAIN_FOLDER_PATH = Path("JPEG-Format-Project/code/file_path").parents[2].absolute()

def get_path(file_name):

    return MAIN_FOLDER_PATH / ("jpegs/" + file_name + ".jpeg")


def get_restore_path(file_name, extra_name):
    return MAIN_FOLDER_PATH / ("restored_jpegs/" + file_name + "_" + extra_name + ".jpeg")