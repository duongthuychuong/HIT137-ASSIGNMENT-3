"""
Test script for ImageProcessor module.
Verifies image loading, display, click detection, coordinate conversion,
and circle drawing functionality.
"""

import tkinter as tk
from tkinter import filedialog
from image_processor import ImageProcessor


def main():
    # Create main window
    root = tk.Tk()
    root.title("ImageProcessor Test")

    # Create processor instance
    processor = ImageProcessor()

    # Create two side-by-side canvases (simulating final layout)
    canvas_left = tk.Canvas(
        root, width=500, height=500, bg="lightgray"
    )
    canvas_left.pack(side="left", padx=5, pady=5)

    canvas_right = tk.Canvas(
        root, width=500, height=500, bg="lightgray"
    )
    canvas_right.pack(side="right", padx=5, pady=5)

    def load():
        """Open file dialog and load selected image."""
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if path and processor.load_image(path):
            processor.display_on_canvas(
                canvas_left, processor.get_original_image(), tag="left"
            )
            processor.display_on_canvas(
                canvas_right, processor.get_modified_image(), tag="right"
            )
            print(f"Loaded successfully. Original size: {processor.get_original_size()}")

    def on_click(event):
        """Handle click on right canvas: convert coordinates and draw red circle."""
        if not processor.is_loaded():
            print("No image loaded yet.")
            return

        # Convert canvas coordinates to image coordinates
        img_x, img_y = processor.canvas_to_image_coords(event.x, event.y)
        print(f"Canvas click ({event.x},{event.y}) -> Image coords ({img_x},{img_y})")

        # Draw red circle on both images at the same point
        new_orig = processor.draw_circle(
            processor.get_original_image(), (img_x, img_y), 30, "red"
        )
        new_mod = processor.draw_circle(
            processor.get_modified_image(), (img_x, img_y), 30, "red"
        )
        processor.display_on_canvas(canvas_left, new_orig, tag="left")
        processor.display_on_canvas(canvas_right, new_mod, tag="right")

    # Bind click event to right canvas only
    canvas_right.bind("<Button-1>", on_click)

    # Load button at the bottom
    load_btn = tk.Button(root, text="Load Image", command=load)
    load_btn.pack(side="bottom", pady=10)

    # Start GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
  test: Add test script for ImageProcessor in tests/ folder (Person 1)
