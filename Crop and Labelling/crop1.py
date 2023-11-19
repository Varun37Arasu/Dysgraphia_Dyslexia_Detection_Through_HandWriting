from PIL import Image, ImageDraw
import os

def read_stencil(stencil_path):
    stencil = Image.open(stencil_path)
    positions = []

    # Iterate over the cells in the stencil
    num_rows, num_columns = 7, 3
    for row in range(num_rows):
        for col in range(num_columns):
            # Calculate the coordinates of each cell
            x1 = col * (stencil.width // num_columns)
            y1 = row * (stencil.height // num_rows)
            x2 = (col + 1) * (stencil.width // num_columns)
            y2 = (row + 1) * (stencil.height // num_rows)

            positions.append((x1, y1, x2, y2))

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
    # Step 1: Read Stencil
    stencil_path = "Stencil.png"  # Provide the path to your stencil image
    positions = read_stencil(stencil_path)

    # Step 2: Input Image and Output Folder
    input_image_path = "input.png"  # Provide the path to your input image
    output_folder = "output_images"

    # Step 3: Image Cropping
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crop_image(input_image_path, output_folder, positions)
