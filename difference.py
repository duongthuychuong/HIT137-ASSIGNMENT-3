class Difference:
    """
    Base class for all image differences.
    """

    def apply(self, image, box):
        """
        Applies a difference to the image.

        Parameters:
            image: Image to modify
            box: Region of interest (x, y, w, h)
        """
        pass


class BlurDifference(Difference):
    """Applies blur effect to a region."""

    def apply(self, image, box):
        pass


class ColorDifference(Difference):
    """Applies color change to a region."""

    def apply(self, image, box):
        pass


class BrightnessDifference(Difference):
    """Applies brightness change to a region."""

    def apply(self, image, box):
        pass


class AddObjectDifference(Difference):
    """Adds a small object to a region."""

    def apply(self, image, box):
        pass