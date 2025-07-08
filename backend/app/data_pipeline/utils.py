import shutil


def save_binary_to_file(file: bytes, save_path: str):
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)
