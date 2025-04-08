
import os
from pathlib import Path
from huggingface_hub import HfApi
from huggingface_hub.utils import RepositoryNotFoundError
from datetime import datetime
import time
import shutil
from fastapi import HTTPException

from .models import Model

from inferadmin.config.loader import config_manager

def check_hf_model_exists(model_path):
    """
    Check if a complete Hugging Face model exists at the given path.
    
    Returns:
        bool: True if valid model, False otherwise
    """
    path = Path(model_path)
    
    # Check if the directory exists
    if not path.exists() or not path.is_dir():
        return False
    # Check if the directory is empty
    if not any(path.iterdir()):
        return False
        
    # Required files to check
    required_files = [
        "*.safetensors",  # At least one safetensors file
        "generation_config.json",
        "config.json",
        "tokenizer.json",
        "special_tokens_map.json",
        "tokenizer_config.json",
        "vocab.json"
    ]
    
    # Check each required file
    for file_pattern in required_files:
        if "*" in file_pattern:
            # Handle wildcard pattern (for safetensors)
            if not list(path.glob(file_pattern)):
                return False
        else:
            # Handle exact filename
            if not (path / file_pattern).exists():
                return False
                
    return True

def get_folder_size_gb(folder_path):
    """
    Calculate the total size of all files in a folder and its subfolders in GB.
    
    Args:
        folder_path (str): Path to the folder
        
    Returns:
        float: Size in gigabytes
    """
    path = Path(folder_path)
    
    if not path.exists() or not path.is_dir():
        return 0.0
    
    total_size = 0
    
    # Walk through all files in the directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Skip if it's a symlink
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    
    # Convert bytes to GB
    size_gb = total_size / (1024 ** 3)
    
    return round(size_gb, 2)

def get_most_recent_modified_date(folder_path):
    """
    Get the most recent modification date of any file in the directory.
    
    Args:
        folder_path (str): Path to the folder
        
    Returns:
        datetime
    """
    most_recent_time = 0
    
    # Walk through all files in the directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                file_mtime = os.path.getmtime(file_path)
                if file_mtime > most_recent_time:
                    most_recent_time = file_mtime
    
    # If no files were found, return current time
    if most_recent_time == 0:
        most_recent_time = time.time()
    
    # Convert to datetime
    modified_date = datetime.fromtimestamp(most_recent_time)
    
    return modified_date

def scan_hf_models_directory():
    """
    Scan a directory for Hugging Face models and collect info about each valid model.

    Returns:
        list: List of dictionaries with model info (repo_id, path, size_gb, last_updated)
    """
    volume_path = Path(config_manager.get_config().model_storage_path)
    
    if not volume_path.exists() or not volume_path.is_dir():
        return []
    
    model_info_list = []
    
    # Get all subdirectories in the base path
    subdirs = [d for d in volume_path.iterdir() if d.is_dir()]
    
    for folder in subdirs:
        # Get folder name
        folder_name = folder.name
        folder_path = str(folder)
        
        # Check if it's a valid HF model
        is_valid_model = check_hf_model_exists(folder_path)
        
        # Get folder size
        size_gb = get_folder_size_gb(folder_path)
        
        # Get the most recent modification date of any file in the directory
        last_updated = get_most_recent_modified_date(folder_path)
        
        # create Model object
        model_info = Model(
            repo_id=folder_name.replace('_', '/'),
            path=folder_path,
            size_gb=size_gb,
            last_updated=last_updated
        )

        if is_valid_model:
            model_info_list.append(model_info)

    return model_info_list

def delete_model(repo_id:str):
    """
    Delete a model from the storage path and all its contents.
    
    Args:
        model_name (str): hf_model name
    """
    folder_name = repo_id.replace("/", "_")
    folder_path = f"{config_manager.get_config().model_storage_path}/{folder_name}"

    path = Path(folder_path)
    
    # Check if the path exists and is a directory
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Path does not exist: {folder_path}"
        )
    
    if not path.is_dir():
        raise HTTPException(
            status_code=404,
            detail=f"Path is not a directory: {folder_path}"
        )
    
    try:
        # Remove the directory and all its contents
        shutil.rmtree(folder_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting model: {str(e)}"
        )
    
def download_hf_model(repo_id:str):
    """
    Downloads the given model to the local directory from huggingface.

    Args:
        repo_id (str): the HF repo name of thing to download
    """
    hf = HfApi(
        token=config_manager.get_config().hf_token
    )

    volume_path = config_manager.get_config().model_storage_path
    file_name = repo_id.replace('/', '_')
    target_path = f"{volume_path}/{file_name}"

    try:
        hf.snapshot_download(
            repo_id=repo_id,
            repo_type='model',
            local_dir=target_path
        )

    except RepositoryNotFoundError as _:
        raise HTTPException(
            status_code=404,
            detail=f"HuggingFace Repository not found: {repo_id}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading model: {str(e)}"
        )