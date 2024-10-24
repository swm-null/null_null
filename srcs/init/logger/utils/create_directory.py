import os

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print(e)
        print("[logger.utils.create_directory] Failed to create the directory.")
