import os
import shutil
import subprocess
from tkinter import Tk, Label, PhotoImage
import sys

def cleanup_(files_to_remove : list = [], dir_to_remove: list=[] , file_end_with=[])->None :  
    """
    Cleans the given directories and files
    """
    for root, dirs, files in os.walk(os.getcwd()):
        # Remove files based on extensions or specific filenames
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(ext) for ext in file_end_with) or file in files_to_remove:
                try:
                    os.remove(file_path)
                    print(f"clean : {file_path}")
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")

        # Remove directories
        for dir_ in dirs:
            if dir_ in dir_to_remove:
                dir_path = os.path.join(root, dir_)
                try:
                    shutil.rmtree(dir_path)
                    print(f"clean dir: {dir_path}")
                except OSError as e:
                    print(f"Error removing directory {dir_path}: {e}")


def create_executable(script_path="main.py", resource_dir="resources/images"):
    """
    Creates a standalone executable from a given Python script using pyinstaller, including all resources from a directory.

    Parameters:
    script_path (str): The path to the Python script to be converted into an executable.
    resource_dir (str): The path to the resources directory to be included in the executable.
    """
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"The script file '{script_path}' does not exist.")
    
    if not os.path.isdir(resource_dir):
        raise FileNotFoundError(f"The resource directory '{resource_dir}' does not exist.")
    
    # Construct the pyinstaller command
    command = ['pyinstaller', '--onefile', script_path, '--add-data', f'{resource_dir}{os.pathsep}resources/images']

    try:
        # Run pyinstaller with the constructed command
        subprocess.run(command, check=True)
        print(f"Executable created successfully for {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the executable: {e}")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)