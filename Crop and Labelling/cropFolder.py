from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os

positions = []

def on_rectangle_select(eclick, erelease):
    global positions
    positions.append((eclick.xdata, eclick.ydata, erelease.xdata, erelease.ydata))

def mark_positions(input_image_path):
    global positions
    # Load the input image
    input_image = Image.open(input_image_path)

    fig, ax = plt.subplots(1)
    ax.imshow(input_image)

    def toggle_selector(event):
        if event.key in ['enter', ' ']:
            rect_selector.set_active(False)
            plt.close()

    rect_selector = RectangleSelector(ax, on_rectangle_select, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    fig.canvas.mpl_connect('key_press_event', toggle_selector)

    plt.show()

    return positions


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


def calc_positions_gen(image_width, image_height, num_rows, num_columns, gap_size_percent, cell_width_percent,cell_height_percent):
    positions = []

    for i in range(num_rows):
        for j in range(num_columns):
            # Calculate the coordinates based on percentages
            x1 = int(j * (1 + gap_size_percent) * image_width / num_columns)
            y1 = int(i * (1 + gap_size_percent) * image_height / num_rows)
            x2 = int((j + 1) * (1 + gap_size_percent) * image_width / num_columns)
            y2 = int((i + 1) * (1 + gap_size_percent) * image_height / num_rows)

            positions.append((x1, y1, x2, y2))

    return positions

def create_directory_structure(base_folder, classes, subfolders):
    for class_name in classes:
        class_folder = os.path.join(base_folder, class_name)
        if not os.path.exists(class_folder):
            os.makedirs(class_folder)
            for subfolder in subfolders:
                subfolder_path = os.path.join(class_folder, subfolder)
                os.makedirs(subfolder_path)


def crop_image(input_image_path, output_folder, positions, class_index):
    # Load the input image
    target_resolution = (1136, 1600)
    # print(input_image_path)
    input_image = Image.open(input_image_path)
    # resized_image = input_image.resize(target_resolution, Image.ANTIALIAS)
    resized_image = input_image.resize(target_resolution, Image.Resampling.LANCZOS)

    # Get the base name of the image (without extension)
    image_name = os.path.splitext(os.path.basename(input_image_path))[0]
    # print("image_name no ext = " , image_name)

    # Iterate over user-specified positions and crop the input image
    for i, pos in enumerate(positions):
        x1, y1, x2, y2 = pos
        region = (x1, y1, x2, y2)

        # Crop the input image using the current rectangle
        cropped_image = resized_image.crop(region)

        # Save the cropped image
        # output_path = os.path.join(output_folder, f"Class{i + 1}",f"ImageClass{i + 1}.png")
        output_path = os.path.join(output_folder, f"Class{i + 1}", f"{image_name}_ImageClass{i + 1}.png")

        # output_path = os.path.join(output_folder, f"class{i + 1}.png")
        print("output_path in crop : ",output_path)
        cropped_image.save(output_path)


# def process_images_in_folder(input_folder, class_name):
    # List all files in the input folder
    # image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # output_folder = "output_images"
    # base_output_folder = "Dataset"
    # classes = ["Dictation", "Copywriting"]
    # subfolders = ["Below Average", "Average", "Above Average"]
    # class_type = class_name

    # for image_file in image_files:
    #     # Construct the full path to the image file
    #     image_path = os.path.join(input_folder, image_file)
    #     print(" Input Image Path : ",image_path)

    #     try:
    #         # Load the input image
    #         input_image = Image.open(image_path)
    #         # print(" Input Image : ",input_image)

    #     except Exception as e:
    #         print(f"Error opening image: {image_path}\n{e}")
    #         continue

    #     # Iterate over classes and perform cropping
    #     for class_index, class_name in enumerate(classes):
    #         # Step 3: Image Cropping
    #         output_folder = os.path.join(base_output_folder, "Train" if class_index == 0 else "Test" if class_index == 1 else "Validation", class_name)
    #         # print("base_output_folder folder : ", base_output_folder)
    #         # print("Output folder : ", output_folder)
    #         crop_image(image_path, output_folder, positions,class_type, class_index + 1)

def process_images_in_folder(input_folder, class_name):
    # List all files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    output_folder = "output_images"
    base_output_folder = "Dataset"
    dataset_type = ["Train","Test","Validation"]
    classes = ["Dictation", "Copywriting"]
    subfolders = ["Below_Average", "Average", "Above_Average"]
    class_type = class_name

    for dtype in dataset_type:
        for class_name in classes:
            # Step 3: Image Cropping
            output_folder = os.path.join(base_output_folder, dtype, class_name, class_type)

            for image_file in image_files:
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
                crop_image(image_path, output_folder, positions, class_type)

if __name__ == "__main__":
    # Specify the input folders for each class
    input_folders = {
        "Above_Average": "Dataset_Input\Above_Average",
        "Average": "Dataset_Input\Average",
        "Below_Average": "Dataset_Input\Below_Average",
    }

    positions = calc_positions(100,290,145,320)

    # Process images in each input folder
    for class_name, input_folder in input_folders.items():
        print("class_name: " + class_name)
        print("input_folder " + input_folder)
        process_images_in_folder(input_folder, class_name)