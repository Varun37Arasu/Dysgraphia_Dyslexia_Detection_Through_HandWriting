from PIL import Image
import os
import random
import shutil

def crop_image(input_image_path, output_folder, positions, class_type, image_name):
    # Load the input image
    target_resolution = (1136, 1600)
    actual_image_path = os.path.join(input_image_path,image_name)
    input_image = Image.open(actual_image_path)
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
        print("Image saved -> ", output_path)

def split_images(input_folder, output_folder, split_ratios, positions):
    # Traverse through the input directory structure
    print("\nInput folder: ", input_folder)
    print("\nOutput folder: ", output_folder)

    image_files = [f for f in os.listdir(input_folder)]

    for file in image_files:
        # Construct the full path to the image file
        image_path = os.path.join(input_folder,file)
        print("\nInput Image Path: ", image_path)
        try:
            # Load the input image
            input_image = Image.open(image_path)

        except Exception as e:
            print(f"Error opening image: {image_path}\n{e}")
            continue

        # Perform cropping and save to the respective Class{$i} folder
        image_name = os.path.splitext(file)[0]
        process_images_in_folder(input_folder, output_folder, split_ratios, positions, image_name)

def process_images_in_folder(input_folder, base_output_folder, split_ratios, positions,c_d_name,class_name):
    # Calculate the number of images for each split
    print("\n",input_folder)

    image_files = [f for f in os.listdir(input_folder)]
    print(image_files)

    total_images = len(image_files)
    train_count = int(split_ratios["Train"] * total_images)
    test_count = max(1,int(split_ratios["Test"] * total_images))
    validation_count = total_images - train_count - test_count

    print("Number of total images : ",total_images)
    print("Number of train images : ",train_count)
    print("Number of test images : ",test_count)
    print("Number of validation images : ",validation_count)

    # Shuffle the split types randomly
    split_types = ["Train"] * train_count + ["Test"] * test_count + ["Validation"] * validation_count
    random.shuffle(split_types)
    print("split_types : ",split_types)

    # Determine the output folder for each split
    i = 0
    for dtype in split_types:
        # Step 3: Image Cropping
        output_folder = os.path.join(base_output_folder, dtype, c_d_name, class_name)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Perform cropping for each class type
        print("\n\n i - image_files[i%total_images] : ",i, image_files[i%total_images])
        crop_image(input_folder, output_folder, positions, c_d_name, image_files[i%total_images])
        i = i + 1


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


if __name__ == "__main__":
    # Specify the input folder for the entire dataset
    # input_folder = "Dataset_Input"
    output_folder = "Dataset"

    input_folders_cp = {
        "Above_Average": "Umang_Input\Copywriting\Above_Average",
        "Average": "Umang_Input\Copywriting\Average",
        "Below_Average": "Umang_Input\Copywriting\Below_Average",
    }

    input_folders_dc = {
        "Above_Average": "Dataset_Input\Dictation\Above_Average",
        "Average": "Dataset_Input\Dictation\Average",
        "Below_Average": "Dataset_Input\Dictation\Below_Average",
    }

    # Example positions, replace it with your logic to get positions
    positions = calc_positions(100,290,145,320)

    # Specify the split ratios
    split_ratios = {"Train": 0.7, "Test": 0.15, "Validation": 0.15}
    # split_ratios = {"Train": 0.8, "Test": 0.1, "Validation": 0.1}

    # Split and process images
    # split_images(input_folder, output_folder, split_ratios, positions)
    for class_name, input_folder in input_folders_cp.items():
        print("\n\nclass_name: " + class_name)
        print("input_folder " + input_folder)
        # process_images_in_folder(input_folder, class_name)
        process_images_in_folder(input_folder, output_folder, split_ratios, positions, "Copywriting",class_name)
        # split_images(input_folder, output_folder, split_ratios, positions)
