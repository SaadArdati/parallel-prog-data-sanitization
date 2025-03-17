import os
from PIL import Image

INPUT_DIR = "before_processing/unsplash_400x"
OUTPUT_DIR = "after_processing/non_screenshot_256x256"
TARGET_SIZE = (256, 256)

def normalize_images(input_folder, output_folder, target_size=(256, 256)):
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Supported image formats
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

    # Process all images in the input folder
    processed_count = 0
    skipped_count = 0

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Skip directories and non-image files
        if not os.path.isfile(input_path) or not filename.lower().endswith(supported_formats):
            skipped_count += 1
            continue

        try:
            # Open the image
            with Image.open(input_path) as img:
                # Convert images with transparency to RGB
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGB')

                # Crop image to maintain aspect ratio then resize
                orig_width, orig_height = img.size
                target_width, target_height = target_size
                target_ratio = target_width / target_height
                orig_ratio = orig_width / orig_height

                if orig_ratio > target_ratio:
                    # Image is too wide, crop width
                    new_width = int(target_ratio * orig_height)
                    left = (orig_width - new_width) // 2
                    box = (left, 0, left + new_width, orig_height)
                else:
                    # Image is too tall, crop height
                    new_height = int(orig_width / target_ratio)
                    top = (orig_height - new_height) // 2
                    box = (0, top, orig_width, top + new_height)

                img_cropped = img.crop(box)
                img_resized = img_cropped.resize(target_size, Image.LANCZOS)

                # Save the image to the output folder with the same filename
                output_path = os.path.join(output_folder, filename)
                img_resized.save(output_path)

                processed_count += 1
                print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            skipped_count += 1

    print(f"\nNormalization complete: {processed_count} images processed, {skipped_count} files skipped")


if __name__ == "__main__":
    # Use constants defined at the top of the file
    normalize_images(INPUT_DIR, OUTPUT_DIR, TARGET_SIZE)
