import os, shutil

def clear_dest_dir(dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

def copy_files_recursive(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    files = os.listdir(source_path)
    for file in files:
        filepath = os.path.join(source_path, file)
        if os.path.isfile(filepath):
            shutil.copy(filepath, dest_path)
        else:
            new_dest_path = os.path.join(dest_path, file)
            copy_files_recursive(filepath, new_dest_path)