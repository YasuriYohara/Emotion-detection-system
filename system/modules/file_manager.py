"""
File Manager Module
Handles temporary file operations with security best practices.
"""

import os
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    """
    Validate if the uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_temp(file, temp_dir='temp'):
    """
    Save uploaded file to temporary directory with secure filename.
    
    Args:
        file: FileStorage object from Flask request
        temp_dir (str): Temporary directory path
        
    Returns:
        str: Path to saved temporary file
        
    Raises:
        ValueError: If file is invalid or too large
    """
    if not file or not allowed_file(file.filename):
        raise ValueError("Invalid file type. Only JPEG and PNG are allowed.")
    
    # Create temp directory if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Generate unique filename to avoid conflicts
    import time
    unique_filename = f"{int(time.time() * 1000)}_{filename}"
    filepath = os.path.join(temp_dir, unique_filename)
    
    # Save file
    file.save(filepath)
    
    # Validate file size after saving
    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        os.remove(filepath)
        raise ValueError(f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024*1024)}MB")
    
    return filepath


def delete_temp(filepath):
    """
    Delete temporary file with error handling.
    
    Args:
        filepath (str): Path to file to be deleted
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting temporary file {filepath}: {str(e)}")
        return False


def cleanup_temp_directory(temp_dir='temp', max_age_seconds=3600):
    """
    Clean up old files from temporary directory.
    
    Args:
        temp_dir (str): Temporary directory path
        max_age_seconds (int): Maximum age of files in seconds (default 1 hour)
    """
    import time
    
    if not os.path.exists(temp_dir):
        return
    
    current_time = time.time()
    
    for filename in os.listdir(temp_dir):
        filepath = os.path.join(temp_dir, filename)
        
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    print(f"Cleaned up old temporary file: {filename}")
                except Exception as e:
                    print(f"Error cleaning up {filename}: {str(e)}")
