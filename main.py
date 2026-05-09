import tkinter as tk

from image_processor import ImageProcessor
from difference_generator import DifferenceGenerator
from game_controller import GameController
from game_display import GameDisplay


def main():
    """
    Main function that coordinates all components of the game.

    This function:
    1. Creates the GUI window
    2. Loads and processes the image
    3. Generates differences
    4. Initializes game logic
    5. Displays the GUI
    """

    # Step 1: Create main window
    root = tk.Tk()

    # Step 2: Create objects (instances)
    processor = ImageProcessor()
    generator = DifferenceGenerator()

    # Step 3: Load and prepare image
    loaded = processor.load_image("assets/sample.jpg")
    if not loaded:
        raise RuntimeError("Failed to load image: assets/sample.jpg")

    original_image = processor.get_original_image()

    # Step 4: Generate modified image and differences
    modified_image, difference_locations = generator.generate(original_image)

    # Step 5: Create game controller
    controller = GameController(difference_locations)

    # Step 6: Create GUI display
    display = GameDisplay(root, original_image, modified_image, controller)

    # Step 7: Show GUI
    display.show()

    # Step 8: Run application
    root.mainloop()


if __name__ == "__main__":
    main()