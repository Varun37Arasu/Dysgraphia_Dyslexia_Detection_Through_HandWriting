from PIL import Image, ImageDraw
import os


def calc_positions():
    positions = []
    for i in range(7):
        sx, sy = 23, 133
        h, w = 69, 169
        for j in range(3):
            x1 = sx
            y1 = sy
            x2 = x1 + w
            y2 = y1 + h

            positions.append((x1, y1, x2, y2))
            # for the next cell to the right
            sx = sx + 180

        sy = sy + 100
    
    return positions


def read_stencil(stencil_path):
    stencil = Image.open(stencil_path)
    positions = []

    # Convert the image to grayscale
    stencil_gray = stencil.convert("L")

    # Get the coordinates of the marked areas
    width, height = stencil_gray.size
    for x in range(width):
        for y in range(height):
            # Check if the pixel is marked (assuming marked areas are not white)
            if stencil_gray.getpixel((x, y)) < 255:
                positions.append((x, y))

    return positions

def crop_image(input_image_path, output_folder, positions, crop_size):
    # Load the input image
    input_image = Image.open(input_image_path)

    # Crop the input image based on the marked positions
    for i, pos in enumerate(positions):
        x, y = pos
        region = (x - crop_size // 2, y - crop_size // 2, x + crop_size // 2, y + crop_size // 2)

        # Crop the input image using the current region
        cropped_image = input_image.crop(region)

        # Save the cropped image
        output_path = os.path.join(output_folder, f"cropped-image{i + 1}.png")
        cropped_image.save(output_path)

if __name__ == "__main__":
    # Step 1: Read Stencil
    stencil_path = "Stencil.png"  # Provide the path to your stencil image
    positions = read_stencil(stencil_path)
    # positions = calc_positions()

    # Step 2: Input Image and Output Folder
    input_image_path = "input.png"  # Provide the path to your input image
    output_folder = "output_images"

    # Step 3: Image Cropping
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set the desired crop size (adjust as needed)
    crop_size = 50

    crop_image(input_image_path, output_folder, positions, crop_size)
