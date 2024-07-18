import os
import shutil
import click


def cleanup_(files_to_remove : list , dir_to_remove: list)->None :  


    
    for root, dirs, files in os.walk(os.getcwd()):
        # Delete .pyc files
        for file in files:
            if file.endswith(".pyc"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")
        
        # Delete 'pycache' directories
        for dir_ in dirs:
            if dir_ in dir_to_remove :
                dir_path = os.path.join(root, dir_)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")
                except OSError as e:
                    print(f"Error removing directory {dir_path}: {e}")
        
        # Delete files based on defined names
        for file_name in files_to_remove:
            file_path = os.path.join(root, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")
