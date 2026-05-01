import tkinter as tk


class GameDisplay:
    """
    GameDisplay class is responsible for handling the graphical user interface (GUI)
    of the Spot the Difference game using Tkinter.

    Attributes:
        root: Tkinter main window
        original_image: Original image (OpenCV format)
        modified_image: Modified image (OpenCV format)
        controller: GameController object to manage game logic
    """

    def __init__(self, root, original_image, modified_image, controller):
        """
        Constructor method to initialize the GameDisplay object.

        Parameters:
            root: Tkinter root window
            original_image: Original image
            modified_image: Modified image
            controller: GameController instance
        """
        # Instance variables (attributes)
        self.root = root
        self.original_image = original_image
        self.modified_image = modified_image
        self.controller = controller

        # UI components (will be created later)
        self.original_label = None
        self.modified_label = None
        self.score_label = None
        self.mistake_label = None
        self.message_label = None

    def convert_cv_to_tk(self, image):
        """
        Converts an OpenCV image into a Tkinter-compatible format.

        Parameters:
            image: OpenCV image

        Returns:
            Tkinter-compatible image
        """
        pass

    def show(self):
        """
        Creates and displays all GUI components including images,
        labels, and buttons.
        """
        pass

    def handle_image_click(self, event):
        """
        Handles mouse click events on the modified image.

        Parameters:
            event: Tkinter mouse event containing click coordinates
        """
        pass

    def draw_found_marker(self, x, y):
        """
        Draws a visual marker on the image when a correct difference is found.

        Parameters:
            x (int): x-coordinate of click
            y (int): y-coordinate of click
        """
        pass

    def reveal_differences(self):
        """
        Reveals all remaining differences to the player.
        """
        pass

    def update_labels(self):
        """
        Updates score and mistake labels in the GUI.
        """
        pass

    def open_new_image(self):
        """
        Opens a file dialog so the player can choose a new image.
        Resets the game round after loading.
        """
        pass