"""
ImageProcessor Module
Handles image loading, scaling, display, circle drawing, and coordinate conversion.
Author: Sihao Cui (Person 1)
"""

import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageProcessor:
    """
    Image processing class.
    Other team members interact with images through this class's methods.
    """

    # Class constants: fixed Canvas dimensions
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 500
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp')

    def __init__(self):
        """Constructor: initialise all internal attributes."""
        self._original_image = None      # Original image (BGR numpy array)
        self._modified_image = None      # Modified image
        self._scale_ratio = 1.0          # Scale ratio for display
        self._display_size = (0, 0)      # Size after scaling
        self._original_size = (0, 0)     # Original image dimensions
        # PhotoImage references must be kept, otherwise Python's garbage
        # collector will discard them and images will disappear from the GUI.
        self._photo_refs = {}

    # ---------- Image Loading ----------

    def load_image(self, file_path: str) -> bool:
        """
        Load an image from disk.
        Returns True on success, False otherwise.
        """
        if not file_path.lower().endswith(self.SUPPORTED_FORMATS):
            print(f"Unsupported file format: {file_path}")
            return False

        # OpenCV reads images in BGR format
        img = cv2.imread(file_path)
        if img is None:
            print(f"Failed to read image: {file_path}")
            return False

        self._original_image = img
        self._modified_image = img.copy()  # Clone for difference generation

        # Store original dimensions as (width, height)
        h, w = img.shape[:2]
        self._original_size = (w, h)
        self._compute_scale()
        return True

    def _compute_scale(self):
        """Compute scale ratio based on Canvas size while preserving aspect ratio."""
        w, h = self._original_size
        ratio_w = self.CANVAS_WIDTH / w
        ratio_h = self.CANVAS_HEIGHT / h
        # Use the smaller ratio to ensure the entire image fits in the Canvas
        self._scale_ratio = min(ratio_w, ratio_h)
        self._display_size = (
            int(w * self._scale_ratio),
            int(h * self._scale_ratio)
        )

    # ---------- Data Access Interface (used by other team members) ----------

    def get_original_image(self) -> np.ndarray:
        """Return the original image. Used by Person 3 to generate differences."""
        return self._original_image

    def get_modified_image(self) -> np.ndarray:
        """Return the modified image."""
        return self._modified_image

    def set_modified_image(self, img: np.ndarray) -> None:
        """Person 3 calls this to write back the image with differences applied."""
        self._modified_image = img

    def is_loaded(self) -> bool:
        """Check whether an image has been loaded."""
        return self._original_image is not None

    def get_original_size(self) -> tuple:
        """Return original image size as (width, height). Person 3 needs this."""
        return self._original_size

    # ---------- Display on Canvas ----------

    def display_on_canvas(self, canvas, image: np.ndarray, tag: str = "default"):
        """
        Render an image onto a Tkinter Canvas.
        tag: distinguishes original vs modified canvas to prevent reference overwrite.
        """
        # OpenCV uses BGR, Tkinter requires RGB - conversion is mandatory
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize to Canvas dimensions
        resized = cv2.resize(rgb, self._display_size, interpolation=cv2.INTER_AREA)
        pil_img = Image.fromarray(resized)
        photo = ImageTk.PhotoImage(pil_img)

        # Critical: keep a reference, otherwise the image will disappear
        self._photo_refs[tag] = photo

        canvas.delete("all")
        # Centre the image within the Canvas
        x_offset = (self.CANVAS_WIDTH - self._display_size[0]) // 2
        y_offset = (self.CANVAS_HEIGHT - self._display_size[1]) // 2
        canvas.create_image(x_offset, y_offset, anchor="nw", image=photo)

    # ---------- Draw Circle on Image (used by Person 4) ----------

    def draw_circle(self, image: np.ndarray, center: tuple,
                    radius: int = 30, color: str = "red") -> np.ndarray:
        """
        Draw a circle on the image and return the new image.
        center: (x, y) in original image coordinates
        color: 'red' for found differences, 'blue' for revealed unfound differences
        """
        # OpenCV uses BGR: red=(0,0,255), blue=(255,0,0)
        color_map = {
            "red":  (0, 0, 255),
            "blue": (255, 0, 0),
        }
        bgr = color_map.get(color, (0, 0, 255))
        result = image.copy()
        cv2.circle(result, center, radius, bgr, thickness=3)
        return result

    # ---------- Coordinate Conversion (used by Person 4) ----------

    def canvas_to_image_coords(self, canvas_x: int, canvas_y: int) -> tuple:
        """
        Convert Canvas click coordinates to original image pixel coordinates.
        Person 4 calls this on click events to match against difference regions.
        """
        x_offset = (self.CANVAS_WIDTH - self._display_size[0]) // 2
        y_offset = (self.CANVAS_HEIGHT - self._display_size[1]) // 2
        x = (canvas_x - x_offset) / self._scale_ratio
        y = (canvas_y - y_offset) / self._scale_ratio
        return (int(x), int(y))

    def image_to_canvas_coords(self, img_x: int, img_y: int) -> tuple:
        """Convert original image coordinates to Canvas coordinates (auxiliary)."""
        x_offset = (self.CANVAS_WIDTH - self._display_size[0]) // 2
        y_offset = (self.CANVAS_HEIGHT - self._display_size[1]) // 2
        x = img_x * self._scale_ratio + x_offset
        y = img_y * self._scale_ratio + y_offset
        return (int(x), int(y))

    # ---------- State Reset ----------

    def reset(self):
        """Clear state before loading a new image."""
        self._original_image = None
        self._modified_image = None
        self._photo_refs.clear()
