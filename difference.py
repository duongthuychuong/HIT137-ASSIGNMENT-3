import cv2
import numpy as np

class Difference:
    """
    Base class for all image differences.
    """

    def apply(self, image, box):
        raise NotImplementedError("Subclasses must implement this method")

    def get_roi(self, image, box):
        x, y, w, h = box
        return image[y:y+h, x:x+w].copy()

    def set_roi(self, image, box, roi):
        x, y, w, h = box
        image[y:y+h, x:x+w] = roi


class BlurDifference(Difference):
    """Applies blur effect to a region."""

    def apply(self, image, box):
        roi = self.get_roi(image, box)

        blurred = cv2.GaussianBlur(roi, (15, 15), 0)

        self.set_roi(image, box, blurred)
        return image


class ColorDifference(Difference):
    """Applies color change to a region."""

    def apply(self, image, box):
        roi = self.get_roi(image, box)
        # Shift color (add red tint)
        roi = roi.copy()
        shift = np.random.randint(30, 70)
        roi[:, :, 2] = np.clip(roi[:, :, 2] + shift, 0, 255)
        self.set_roi(image, box, roi)
        return image


class BrightnessDifference(Difference):
    """Applies brightness change to a region."""

    def apply(self, image, box):
        roi = self.get_roi(image, box)

        roi = cv2.convertScaleAbs(roi, alpha=1.0, beta=40)

        self.set_roi(image, box, roi)
        return image


class AddObjectDifference(Difference):
    """Flips the region horizontally to simulate an added object."""
    def apply(self, image, box):
        roi = self.get_roi(image, box)

        flipped = cv2.flip(roi, 1)  # horizontal flip

        self.set_roi(image, box, flipped)
        return image