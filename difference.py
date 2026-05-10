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
    """
    Adds a random transparent PNG object onto the image.
    """

    def apply(self, image, box):
        import random
        import cv2
        import os

        x, y, w, h = box

        object_files = [
            "ball.png",
            "banana.png",
            "bird.png",
            "cat.png",
            "leaf.png"
        ]

        chosen_file = random.choice(object_files)
        object_path = os.path.join("assets", chosen_file)

        sticker = cv2.imread(object_path, cv2.IMREAD_UNCHANGED)

        if sticker is None:
            print(f"Could not load object: {object_path}")
            return image

        if len(sticker.shape) < 3 or sticker.shape[2] != 4:
            print(f"Object has no transparent background: {object_path}")
            return image

        sticker_size = random.randint(
            max(20, min(w, h) // 2),
            min(w, h)
        )

        sticker = cv2.resize(sticker, (sticker_size, sticker_size))

        b, g, r, a = cv2.split(sticker)
        overlay_color = cv2.merge((b, g, r))
        mask = cv2.merge((a, a, a)) / 255.0

        pos_x = random.randint(x, x + max(1, w - sticker_size))
        pos_y = random.randint(y, y + max(1, h - sticker_size))

        roi = image[
            pos_y:pos_y + sticker_size,
            pos_x:pos_x + sticker_size
        ]

        blended = (
            roi * (1 - mask)
            + overlay_color * mask
        ).astype("uint8")

        image[
            pos_y:pos_y + sticker_size,
            pos_x:pos_x + sticker_size
        ] = blended

        return image