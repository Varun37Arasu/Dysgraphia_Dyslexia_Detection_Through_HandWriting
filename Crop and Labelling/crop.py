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
            sx = sx + 180

        # Reset sy for the next row
        sy = sy + 100
        sx = 30

    return positions




def crop_image(input_image_path, output_folder, positions):
    # Load the input image
    input_image = Image.open(input_image_path)

    # Iterate over user-specified positions and crop the input image
    for i, pos in enumerate(positions):
        x1, y1, x2, y2 = pos
        region = (x1, y1, x2, y2)

        # Crop the input image using the current rectangle
        cropped_image = input_image.crop(region)

        # Save the cropped image
        output_path = os.path.join(output_folder, f"cropped-image{i + 1}.png")
        cropped_image.save(output_path)

if __name__ == "__main__":
    # Step 1: User Mark Positions
    input_image_path = "Stencil.png"  # Provide the path to your input image
    positions = mark_positions(input_image_path)
    # positions = calc_positions(23,133,69,169)
    # positions = calc_positions(30,126,83,183)
    # print(positions)

    # Step 2: Input Image and Output Folder
    output_folder = "output_images"

    # Step 3: Image Cropping
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crop_image("sample.jpg", output_folder, positions)