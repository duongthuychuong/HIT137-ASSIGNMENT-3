import cv2


class ImageProcessor:
    """
    Handles image loading, resizing, and preparation.

    Attributes:
        max_width (int): Maximum width of display window
        max_height (int): Maximum height of display window
    """

    def __init__(self, max_width=700, max_height=500):
        """
        Constructor for ImageProcessor.
        """
        self.max_width = max_width
        self.max_height = max_height

    def load_image(self, image_path):
        """
        Loads an image from file.

        Parameters:
            image_path (str): Path to image file

        Returns:
            image: Loaded image
        """
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        return image

    def resize_to_window(self, image):
        """
        Resizes image while keeping aspect ratio.

        Parameters:
            image: Input image

        Returns:
            resized image
        """
        if image is None:
            raise ValueError("Cannot resize image because image is None")

        height, width = image.shape[:2]

        width_ratio = self.max_width / width
        height_ratio = self.max_height / height

        scale = min(width_ratio, height_ratio)

        new_width = int(width * scale)
        new_height = int(height * scale)

        resized_image = cv2.resize(image, (new_width, new_height))

        return resized_image

    def create_copy(self, image):
        """
        Creates a copy of the image for modification.

        Parameters:
            image: Original image

        Returns:
            copied image
        """
        if image is None:
            raise ValueError("Cannot copy image because image is None")

        return image.copy()