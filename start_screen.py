import tkinter as tk
from tkinter import filedialog, messagebox

from image_processor import ImageProcessor
from difference_generator import DifferenceGenerator
from game_controller import GameController
from game_display import GameDisplay


class StartScreen:
    """
    Shows the start screen and launches the game.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference")

        self.processor = self.create_image_processor()
        self.generator = DifferenceGenerator()

        self.setup_ui()

    def create_image_processor(self):
        """
        Creates ImageProcessor using screen size.
        """

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        image_width = (screen_width // 2) - 120
        image_height = screen_height - 320

        return ImageProcessor(
            max_width=image_width,
            max_height=image_height
        )

    def setup_ui(self):
        """
        Creates the start screen UI.
        """

        self.center_window(900, 550)

        self.create_title()
        self.create_description()
        self.create_choose_button()

    def center_window(self, width, height):
        """
        Centers a window on screen.
        """

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_pos = (screen_width - width) // 2
        y_pos = (screen_height - height) // 2

        self.root.geometry(
            f"{width}x{height}+{x_pos}+{y_pos}"
        )

    def create_title(self):
        """
        Creates game title.
        """

        title = tk.Label(
            self.root,
            text="Spot the Difference Game",
            font=("Arial", 32, "bold")
        )

        title.pack(pady=60)

    def create_description(self):
        """
        Creates description label.
        """

        description = tk.Label(
            self.root,
            text="Choose an image to start the game.",
            font=("Arial", 18)
        )

        description.pack(pady=20)

    def create_choose_button(self):
        """
        Creates image selection button.
        """

        choose_button = tk.Button(
            self.root,
            text="Choose Image",
            font=("Arial", 18),
            width=18,
            height=2,
            command=self.choose_image
        )

        choose_button.pack(pady=40)

    def choose_image(self):
        """
        Opens file dialog and starts the game.
        """

        image_path = self.open_file_dialog()

        if image_path == "":
            return

        try:

            original_image = self.prepare_original_image(
                image_path
            )

            modified_image, difference_locations = (
                self.create_modified_image(original_image)
            )

            controller = GameController(
                difference_locations
            )

            self.clear_start_screen()

            self.start_game(
                original_image,
                modified_image,
                controller
            )

            self.center_game_window()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def open_file_dialog(self):
        """
        Opens image file chooser.
        """

        return filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

    def prepare_original_image(self, image_path):
        """
        Loads and resizes image.
        """

        original_image = self.processor.load_image(
            image_path
        )

        original_image = self.processor.resize_to_window(
            original_image
        )

        return original_image

    def create_modified_image(self, original_image):
        """
        Creates modified image and difference locations.
        """

        return self.generator.generate(
            self.processor.create_copy(original_image)
        )

    def clear_start_screen(self):
        """
        Removes all start screen widgets.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

    def center_game_window(self):
        """
        Centers game window after images are loaded.
        """

        self.root.update_idletasks()

        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        self.root.geometry(
            f"{window_width}x{window_height}+{x_pos}+{y_pos}"
        )

    def start_game(self, original_image, modified_image, controller):
        """
        Creates and shows the game display.
        """

        display = GameDisplay(
            self.root,
            original_image,
            modified_image,
            controller
        )

        display.show()