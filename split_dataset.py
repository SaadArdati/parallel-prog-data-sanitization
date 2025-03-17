import os
import shutil
import random
from pathlib import Path

SOURCE_DIR = "after_processing/non_screenshot_256x256"
TRAIN_DIR = "split_data/non_screenshot_256x256/train"
TEST_DIR = "split_data/non_screenshot_256x256/test"
TEST_RATIO = 0.2
RANDOM_SEED = 42

def split_dataset(source_folder, train_folder, test_folder, test_ratio=0.2, random_seed=42):
    # Create output directories if they don't exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')
    
    # Get all image files from source directory
    image_files = [f for f in os.listdir(source_folder) 
                  if os.path.isfile(os.path.join(source_folder, f)) 
                  and f.lower().endswith(supported_formats)]
    
    # Set random seed for reproducibility
    random.seed(random_seed)
    
    # Shuffle the file list
    random.shuffle(image_files)
    
    # Calculate split point
    test_size = int(len(image_files) * test_ratio)
    
    # Split the dataset
    test_files = image_files[:test_size]
    train_files = image_files[test_size:]
    
    # Copy files to respective directories
    for filename in train_files:
        src = os.path.join(source_folder, filename)
        dst = os.path.join(train_folder, filename)
        shutil.copy2(src, dst)
        
    for filename in test_files:
        src = os.path.join(source_folder, filename)
        dst = os.path.join(test_folder, filename)
        shutil.copy2(src, dst)
    
    print(f"Dataset split complete:")
    print(f"  • Source directory: {source_folder}")
    print(f"  • Training set: {len(train_files)} images saved to {train_folder}")
    print(f"  • Test set: {len(test_files)} images saved to {test_folder}")
    print(f"  • Split ratio: {1-test_ratio:.0%}/{test_ratio:.0%} (train/test)")


if __name__ == "__main__":
    # Use constants defined at the top of the file
    split_dataset(SOURCE_DIR, TRAIN_DIR, TEST_DIR, TEST_RATIO, RANDOM_SEED) 