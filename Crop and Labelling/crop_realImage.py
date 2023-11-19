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


def crop_image(input_image_path, output_folder, positions):
    # Load the input image
    target_resolution = (1136, 1600)
    print(input_image_path)

    input_image = Image.open(input_image_path)
    resized_image = input_image.resize(target_resolution, Image.ANTIALIAS)

    # Iterate over user-specified positions and crop the input image
    for i, pos in enumerate(positions):
        x1, y1, x2, y2 = pos
        region = (x1, y1, x2, y2)

        # Crop the input image using the current rectangle
        cropped_image = resized_image.crop(region)

        # Save the cropped image
        output_path = os.path.join(output_folder, f"class{i + 1}.png")
        cropped_image.save(output_path)

if __name__ == "__main__":
    # Step 1: User Mark Positions
    input_image_path = "10.jpg"  # Provide the path to your input image
    # positions = mark_positions(input_image_path)
    # positions = calc_positions(50,150,83,173)
    positions = calc_positions(100,290,145,320)

    print(positions)

    # Step 2: Input Image and Output Folder
    output_folder = "output_images"

    # Step 3: Image Cropping
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crop_image(input_image_path, output_folder, positions)


#     Dataset
# ├── Train
# │   ├── Dictation
# │   │   ├── Below Average
# │   │   ├── Average
# │   │   └── Above Average
# │   └── Copywriting
# │       ├── Below Average
# │       ├── Average
# │       └── Above Average
# ├── Test
# │   ├── Dictation
# │   │   ├── Below Average
# │   │   ├── Average
# │   │   └── Above Average
# │   └── Copywriting
# │       ├── Below Average
# │       ├── Average
# │       └── Above Average
# └── Validation
#     ├── Dictation
#     │   ├── Below Average
#     │   ├── Average
#     │   └── Above Average
#     └── Copywriting
#         ├── Below Average
#         ├── Average
#         └── Above Average


#   Input  Dataset
# │   ├── Dictation
# │   │   ├── Below Average 
# │   │   ├── Average
# │   │   └── Above Average
# │   └── Copywriting
# │       ├── Below Average
# │       ├── Average
# │       └── Above Average






#     Dataset - (70:15:15 of 180 images)
# ├── Train - 126
# │   ├── Dictation - 63
# │   │   ├── Below Average - 21
# │   │   ├── Average - 14
# │   │   └── Above Average - 28
# │   └── Copywriting - 63
# │       ├── Below Average - 21
# │       ├── Average - 14
# │       └── Above Average - 28
# ├── Test - 26
# │   ├── Dictation - 13
# │   │   ├── Below Average - (4.5) 4 or 5
# │   │   ├── Average - 3
# │   │   └── Above Average - 6
# │   └── Copywriting - 13
# │       ├── Below Average - (4.5) 4 or 5
# |       ├── Average - 3
# │       └── Above Average - 6
# └── Validation - 27
#     ├── Dictation - 14
#     │   ├── Below Average - (4.5) 4 or 5
#     │   ├── Average - 3
#     │   └── Above Average - 6
#     └── Copywriting - 14
#         ├── Below Average - (4.5) 4 or 5
#         ├── Average - 3
#         └── Above Average - 6


#   Input  Dataset - (180 Images)
# │   ├── Dictation - 90
# │   │   ├── Below Average - 30
# │   │   ├── Average       - 20
# │   │   └── Above Average - 40 
# |   |
# │   └── Copywriting - 90
# │       ├── Below Average - 30
# │       ├── Average       - 20
# │       └── Above Average - 40