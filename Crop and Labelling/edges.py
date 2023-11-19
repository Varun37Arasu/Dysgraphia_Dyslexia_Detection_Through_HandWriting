import cv2
import os

# IMG_PATH = os.path.join('data','images', 'bike.jpg')
img = cv2.imread("Test1.png")


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img, (3,3),0)
canny = cv2.Canny(blurred, threshold1=180, threshold2=200)

resized = cv2.resize(canny, (int(2190/2), int(2738/2)))
cv2.imshow("Canny", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

