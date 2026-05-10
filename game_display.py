import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import cv2

from image_processor import ImageProcessor
from difference_generator import DifferenceGenerator
from game_controller import GameController


class GameDisplay:
    GAME_TOP_HEIGHT = 120

    def __init__(self, root, original_image, modified_image, controller):
        self.root = root
        self.root.title("Spot the Difference")

        self.original_image = original_image
        self.modified_image = modified_image
        self.controller = controller

        self.processor = ImageProcessor()
        self.generator = DifferenceGenerator()

        self.image_gap = 30

        self.tk_original = self.convert_cv_to_tk(self.original_image)
        self.tk_modified = self.convert_cv_to_tk(self.modified_image)

        self.canvas = None
        self.score_label = None
        self.mistake_label = None
        self.message_label = None
        self.remaining_label = None
        self.differences_revealed = False

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.score_label = tk.Label(top_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="left", padx=10)

        self.mistake_label = tk.Label(top_frame, text="Mistakes: 0/3", font=("Arial", 14))
        self.mistake_label.pack(side="left", padx=10)

        self.remaining_label = tk.Label(top_frame, text="Remaining: 5", font=("Arial", 14))
        self.remaining_label.pack(side="left", padx=10)

        self.message_label = tk.Label(
            top_frame,
            text="Find the differences!",
            font=("Arial", 14),
            fg="blue"
        )
        self.message_label.pack(side="left", padx=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        upload_button = tk.Button(
            button_frame,
            text="Upload Image",
            command=self.open_new_image
        )
        upload_button.pack(side="left", padx=10)

        reveal_button = tk.Button(
            button_frame,
            text="Reveal Differences",
            command=self.reveal_differences
        )
        reveal_button.pack(side="left", padx=10)

        self.draw_images()

    def draw_images(self):
        self.tk_original = self.convert_cv_to_tk(self.original_image)
        self.tk_modified = self.convert_cv_to_tk(self.modified_image)

        canvas_width = self.tk_original.width() * 2 + self.image_gap
        canvas_height = self.tk_original.height()

        if self.canvas is not None:
            self.canvas.destroy()

        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_original)

        self.canvas.create_image(
            self.tk_original.width() + self.image_gap,
            0,
            anchor="nw",
            image=self.tk_modified
        )

        self.canvas.bind("<Button-1>", self.handle_image_click)

    def convert_cv_to_tk(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)

    def handle_image_click(self, event):
        if self.differences_revealed:
            return

        offset_x = self.tk_original.width() + self.image_gap

        if event.x < offset_x:
            return

        click_x = event.x - offset_x
        click_y = event.y

        result = self.controller.check_click(click_x, click_y)

        if result == "correct":
            self.draw_found_marker(click_x, click_y, "red")
            self.message_label.config(text="Correct!", fg="green")

            if self.controller.is_game_complete():
                self.message_label.config(text="You found all differences!", fg="green")

        elif result == "wrong":
            self.message_label.config(text="Wrong click!", fg="orange")

        elif result == "locked":
            self.message_label.config(text="Game Over!", fg="red")
            found = self.controller.score
            total = len(self.controller.differences)
            messagebox.showinfo("Game Over", f"Game Over!\nToo many mistakes!\nDifferences found: {found}/{total}")

        self.update_labels()

    def draw_found_marker(self, x, y, color="red"):
        radius = 15
        offset_x = self.tk_original.width() + self.image_gap

        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            outline=color,
            width=3
        )

        self.canvas.create_oval(
            x + offset_x - radius, y - radius,
            x + offset_x + radius, y + radius,
            outline=color,
            width=3
        )

    def reveal_differences(self):
        for diff in self.controller.differences:
            if not diff["found"]:
                x, y = diff["center"]
                self.draw_found_marker(x, y, "blue")
                diff["found"] = True

        self.differences_revealed = True
        self.message_label.config(text="Differences revealed!", fg="blue")
        self.update_labels()

    def update_labels(self):
        self.score_label.config(text=f"Score: {self.controller.score}")
        self.mistake_label.config(text=f"Mistakes: {self.controller.mistakes}/3")
        self.remaining_label.config(text=f"Remaining: {self.controller.get_remaining()}")

    def open_new_image(self):
        image_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if image_path == "":
            return

        try:
            original_image = self.processor.load_image(image_path)
            original_image = self.processor.resize_to_window(original_image)

            modified_image, difference_locations = self.generator.generate(
                self.processor.create_copy(original_image)
            )

            self.original_image = original_image
            self.modified_image = modified_image
            self.controller = GameController(difference_locations)
            self.differences_revealed = False

            self.draw_images()
            self.update_labels()
            self.resize_window_to_image(original_image)

            self.message_label.config(
                text="New image loaded. Find the differences!",
                fg="blue"
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def show(self):
        self.root.deiconify()

    def resize_window_to_image(self, image):
        """Resize the window to fit the image and top controls."""
        image_height = image.shape[0]
        total_height = image_height + self.GAME_TOP_HEIGHT
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{total_height}")
