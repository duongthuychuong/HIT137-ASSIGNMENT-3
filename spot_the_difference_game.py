import cv2
import numpy as np

def load_and_resize(path, width=600):
    img = cv2.imread(path)
    h, w = img.shape[:2]
    scale = width / w
    img = cv2.resize(img, (width, int(h * scale)))
    return img

img = load_and_resize("images.jpeg")

combined = np.hstack((img, img))
cv2.imshow("Game", combined)
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Clicked at:", x, y)

cv2.setMouseCallback("Game", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()