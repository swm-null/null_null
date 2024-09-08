import os

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("[logger.utils.create_directory] Failed to create the directory.")
