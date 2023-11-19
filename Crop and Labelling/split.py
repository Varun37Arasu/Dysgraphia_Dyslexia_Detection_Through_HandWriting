from PIL import Image
import os
import random
import shutil

def calc_positions(sx, sy, h, w):
    positions = []

    for i in range(7):
        for j in range(3):
            x1 = sx
            y1 = sy
            x2 = x1 + w
            y2 = y1 + h

            positions.append((x1, y1, x2, y2))
            # for the next cell to the right
            sx = sx + 310

        # Reset sy for the next row

        # Resize the image through figma
        # sy = sy + 90
        # sx = 50 #59

        # Resizing image through code
        sy = sy + 170
        sx = 100

    return positions

def crop_image(input_image_path, output_folder, positions, class_type, image_name):
    # Load the input image
    target_resolution = (1136, 1600)
    input_image = Image.open(input_image_path)
    resized_image = input_image.resize(target_resolution, Image.Resampling.LANCZOS)

    # Iterate over user-specified positions and crop the input image
    for i, pos in enumerate(positions):
        x1, y1, x2, y2 = pos
        region = (x1, y1, x2, y2)

        # Crop the input image using the current rectangle
        cropped_image = resized_image.crop(region)

        # Save the cropped image
        output_path = os.path.join(output_folder, f"Class{i + 1}", f"{image_name}_ImageClass{i + 1}.png")
        cropped_image.save(output_path)

def split_images(input_folder, output_folder, split_ratios, positions):
    # List all files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Calculate the number of images for each split
    total_images = len(image_files)
    train_count = int(total_images * split_ratios["Train"])
    test_count = int(total_images * split_ratios["Test"])
    validation_count = total_images - train_count - test_count

    print("Number of total images : ",total_images)
    print("Number of train images : ",train_count)
    print("Number of test images : ",test_count)
    print("Number of validation images : ",validation_count)

    # Shuffle the image files randomly
    random.shuffle(image_files)

    # Split the images into Train, Test, and Validation sets
    train_images = image_files[:train_count]
    test_images = image_files[train_count:train_count + test_count]
    validation_images = image_files[train_count + test_count:]

    # Process images for each split
    for dtype, images in [("Train", train_images), ("Test", test_images), ("Validation", validation_images)]:
        for image_file in images:
            # Construct the full path to the image file
            image_path = os.path.join(input_folder, image_file)
            print("\nInput Image Path: ", image_path)
            try:
                # Load the input image
                input_image = Image.open(image_path)

            except Exception as e:
                print(f"Error opening image: {image_path}\n{e}")
                continue

            # Perform cropping and save to the respective Class{$i} folder
            image_name = os.path.splitext(image_file)[0]
            process_images_in_folder(input_image, output_folder, dtype, image_name, positions)

def process_images_in_folder(input_image, base_output_folder, dtype, image_name, positions):
    dataset_types = ["Dictation", "Copywriting"]
    subfolders = ["Below_Average", "Average", "Above_Average"]

    for class_name in dataset_types:
        for category_name in subfolders:
            # Step 3: Image Cropping
            output_folder = os.path.join(base_output_folder, dtype, class_name, category_name)

            # Ensure the output folder exists
            os.makedirs(output_folder, exist_ok=True)

            # Perform cropping for each class type
            crop_image(input_image, output_folder, positions, class_name, image_name)

if __name__ == "__main__":
    # Specify the input folders for each class
    input_folder = "Dataset_Input"
    output_folder = "Dataset"

    # Example positions, replace it with your logic to get positions
    positions = calc_positions(100,290,145,320)

    # Specify the split ratios
    split_ratios = {"Train": 0.7, "Test": 0.15}

    # Split and process images
    split_images(input_folder, output_folder, split_ratios, positions)
