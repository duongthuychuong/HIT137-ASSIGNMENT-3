import random
import cv2

from difference import (
    BlurDifference,
    ColorDifference,
    BrightnessDifference,
    AddObjectDifference,
)


class DifferenceGenerator:
    """
    Generates random non-overlapping differences on an image.
    """

    def __init__(self, difference_count=5, padding=10, min_size=30, max_size=80):
        """
        Constructor for DifferenceGenerator.

        Parameters:
            difference_count (int): number of differences to generate
            padding (int): minimum spacing between boxes
            min_size (int): minimum width/height of a box
            max_size (int): maximum width/height of a box
        """
        self.difference_count = difference_count
        self.padding = padding
        self.min_size = min_size
        self.max_size = max_size

    def is_overlapping(self, new_box, existing_boxes):
        """
        Checks if a new box overlaps with existing boxes.

        Returns:
            True if overlapping, False otherwise
        """
        x, y, w, h = new_box

        for ex, ey, ew, eh in existing_boxes:
            if not (
                x + w + self.padding < ex
                or ex + ew + self.padding < x
                or y + h + self.padding < ey
                or ey + eh + self.padding < y
            ):
                return True

        return False

    def choose_random_positions(self, image, existing_boxes=None):
        """
        Selects a random position.

        Returns:
            one box as (x, y, w, h)
        """
        if image is None:
            return None

        h, w = image.shape[:2]
        existing_boxes = existing_boxes or []

        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            box_w = random.randint(self.min_size, min(self.max_size, max(self.min_size, w - 20)))
            box_h = random.randint(self.min_size, min(self.max_size, max(self.min_size, h - 20)))

            x = random.randint(10, max(10, w - box_w - 10))
            y = random.randint(10, max(10, h - box_h - 10))

            new_box = (x, y, box_w, box_h)

            if not self.is_overlapping(new_box, existing_boxes):
                return new_box

            attempts += 1

        return None

    def generate(self, original_image):
        """
        Applies differences to image.

        Returns:
            modified_image, difference_locations
        """
        if original_image is None:
            raise ValueError("original_image is None")

        modified = original_image.copy()

        difference_classes = [BlurDifference, ColorDifference, BrightnessDifference, AddObjectDifference]

        difference_locations = []
        
        attempt = 0

        # Try several random difference types until one succeeds
        boxes = []

        while attempt < self.difference_count:
            box = self.choose_random_positions(original_image, boxes)
            if box is None:
                break

            DiffClass = random.choice(difference_classes)
            diff = DiffClass()
            diff.apply(modified, box)
            chosen = diff.__class__.__name__
            attempt += 1
            boxes.append(box)
            x, y, bw, bh = box

            difference_locations.append({
                "x": x,
                "y": y,
                "width": bw,
                "height": bh,
                "center": (x + bw // 2, y + bh // 2),
                "type": chosen,
                "found": False
            })

        return modified, difference_locations