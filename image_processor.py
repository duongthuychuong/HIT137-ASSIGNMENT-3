import cv2


class ImageProcessor:
    """
    Handles image loading, resizing, and copying.

    This class makes sure images:
    - load correctly
    - resize to fit inside the GUI window
    - keep the correct aspect ratio
    - do not become too large and push buttons off-screen
    """

    def __init__(self, max_width=600, max_height=420):
        """
        Constructor for ImageProcessor.

        Parameters:
            max_width (int): Maximum width for one displayed image
            max_height (int): Maximum height for one displayed image
        """
        self.max_width = max_width
        self.max_height = max_height

    def load_image(self, image_path):
        """
        Loads an image from a file path.

        Parameters:
            image_path (str): Path to the image file

        Returns:
            image: Loaded OpenCV image
        """
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        return image

    def resize_to_window(self, image):
        """
        Resizes the image to fit inside the allowed display area
        while keeping the correct aspect ratio.

        Returns:
            resized_image: Resized OpenCV image
        """
        if image is None:
            raise ValueError("Cannot resize image because image is None")

        height, width = image.shape[:2]

        if width == 0 or height == 0:
            raise ValueError("Invalid image size")

        width_ratio = self.max_width / width
        height_ratio = self.max_height / height

        # Use the smaller ratio so the image fits inside both width and height
        scale = min(width_ratio, height_ratio)

        new_width = int(width * scale)
        new_height = int(height * scale)

        # Prevent invalid resize values
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        resized_image = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

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

    def load_and_prepare_image(self, image_path):
        """
        Loads and resizes an image in one step.

        This is useful for the game because the image should be resized
        before generating differences.

        Parameters:
            image_path (str): Path to the image file

        Returns:
            resized_image: Loaded and resized image
        """
        image = self.load_image(image_path)
        resized_image = self.resize_to_window(image)

        return resized_image