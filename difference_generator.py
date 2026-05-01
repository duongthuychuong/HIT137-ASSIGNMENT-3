class DifferenceGenerator:
    """
    Generates random non-overlapping differences on an image.
    """

    def __init__(self, difference_count=5):
        """
        Constructor for DifferenceGenerator.
        """
        pass

    def is_overlapping(self, new_box, existing_boxes):
        """
        Checks if a new box overlaps with existing boxes.

        Returns:
            True if overlapping, False otherwise
        """
        pass

    def choose_random_positions(self, image):
        """
        Selects random non-overlapping positions.

        Returns:
            list of boxes
        """
        pass

    def generate(self, original_image):
        """
        Applies differences to image.

        Returns:
            modified_image, difference_locations
        """
        pass