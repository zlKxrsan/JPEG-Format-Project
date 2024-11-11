from pathlib import Path

FILE_NAME = "bird1"

MAIN_FOLDER_PATH = Path("JPEG-Format-Project/code/file_path").parents[2].absolute()

FILE_PATH = MAIN_FOLDER_PATH / ("jpegs/" + FILE_NAME + ".jpg")

RESTORE_FILE_PATH = MAIN_FOLDER_PATH / ("restored_jpegs/" + FILE_NAME + "_restored.jpg")