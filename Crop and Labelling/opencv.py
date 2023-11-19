import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread('a.png')

# Grayscale conversion
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Grid Removal - Example: Using GaussianBlur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge Detection - Example: Canny edge detector
edges = cv2.Canny(blurred, 50, 150)

# Contour Detection
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter and approximate rectangles
rectangles = []
for contour in contours:
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4 and cv2.contourArea(approx) > 1000:  # Adjust area threshold as needed
        rectangles.append(approx)

# Draw rectangles on the original image
cv2.drawContours(image, rectangles, -1, (0, 255, 0), 3)

# OCR - Example using pytesseract
for i, rectangle in enumerate(rectangles):
    x, y, w, h = cv2.boundingRect(rectangle)
    roi = image[y:y + h, x:x + w]
    text = pytesseract.image_to_string(roi, lang='kan')  # Adjust language code as needed
    print(f"Rectangle {i + 1} Coordinates: ({x}, {y}), Text: {text}")

# Display the result
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
