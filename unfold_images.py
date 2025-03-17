import os
import shutil

SOURCE_DIR = "before_processing/google_universal_256x256"
TARGET_DIR = "after_processing/non_screenshot_256x256"
RENAME_DUPLICATES = True

def unfold_images(source_dir, target_dir, rename_duplicates=True):
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
    
    # Track statistics
    total_images = 0
    renamed_images = 0
    
    # Track existing filenames to handle duplicates
    existing_filenames = set()
    
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(source_dir):
        for filename in files:
            # Check if file is an image
            if filename.lower().endswith(supported_formats):
                # Source file path
                src_path = os.path.join(root, filename)
                
                # Target file path
                dst_filename = filename
                
                # Handle duplicate filenames
                if rename_duplicates and dst_filename in existing_filenames:
                    # Get relative path from source directory to create a unique identifier
                    rel_path = os.path.relpath(root, source_dir)
                    # Replace directory separators with underscores
                    rel_path_str = rel_path.replace(os.sep, '_')
                    
                    # Split filename into name and extension
                    name, ext = os.path.splitext(dst_filename)
                    
                    # Create new filename with path information
                    if rel_path != '.':  # Not in the source directory itself
                        dst_filename = f"{name}_{rel_path_str}{ext}"
                    else:
                        # If in source dir itself, just add an incrementing number
                        counter = 1
                        while f"{name}_{counter}{ext}" in existing_filenames:
                            counter += 1
                        dst_filename = f"{name}_{counter}{ext}"
                    
                    renamed_images += 1
                
                # Final destination path
                dst_path = os.path.join(target_dir, dst_filename)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
                
                # Add to existing filenames set
                existing_filenames.add(dst_filename)
                
                # Increment counter
                total_images += 1
    
    print(f"Image unfolding complete:")
    print(f"  • Source directory: {source_dir}")
    print(f"  • Target directory: {target_dir}")
    print(f"  • Total images copied: {total_images}")
    if renamed_images > 0:
        print(f"  • Renamed files due to conflicts: {renamed_images}")


if __name__ == "__main__":
    # Use constants defined at the top of the file
    unfold_images(SOURCE_DIR, TARGET_DIR, RENAME_DUPLICATES) 