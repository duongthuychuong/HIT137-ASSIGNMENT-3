import tkinter as tk
from tkinter import messagebox

class GameDisplay:
    def __init__(self, root, original_image, modified_image, controller):
        self.root = root
        self.root.title("Spot the Difference")
        self.original_image = original_image
        self.modified_image = modified_image
        self.controller = controller

        # Store PhotoImages so they aren't garbage collected
        self.tk_orig = self.convert_cv_to_tk(self.original_image)
        self.tk_mod = self.convert_cv_to_tk(self.modified_image)

        # UI Components 
        self.setup_ui()

    def setup_ui(self):
        """Layout the labels and images."""
        # Labels for stats
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side="top", fill="x")

        self.score_label = tk.Label(self.info_frame, text=f"Score: {self.controller.score}")
        self.score_label.pack(side="left", padx=10)

        self.mistake_label = tk.Label(self.info_frame, text=f"Mistakes: {self.controller.mistakes}/3")
        self.mistake_label.pack(side="left", padx=10)

        self.message_label = tk.Label(self.info_frame, text="Find 5 differences!", fg="blue")
        self.message_label.pack(side="left", padx=20)

        # Canvas for side-by-side images 
        self.canvas = tk.Canvas(self.root, width=self.tk_orig.width() * 2, height=self.tk_orig.height())
        self.canvas.pack()

        # Place images on canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_orig)
        self.canvas.create_image(self.tk_orig.width(), 0, anchor="nw", image=self.tk_mod)

        # Buttons 
        self.reveal_btn = tk.Button(self.root, text="Reveal All", command=self.reveal_differences)
        self.reveal_btn.pack(side="bottom", pady=5)

        # Bind click event to the modified image (right side) 
        self.canvas.bind("<Button-1>", self.handle_image_click)

    def convert_cv_to_tk(self, image):
        """Person 1 Task: Logic goes here. For now, we assume a placeholder. """
        # This will eventually return a ImageTk.PhotoImage object
        pass

    def handle_image_click(self, event):
        """Handles mouse click events. """
        # Adjust X if clicking the right image
        offset_x = self.tk_orig.width()
        if event.x < offset_x:
            return # Ignore clicks on the original image
        
        rel_x = event.x - offset_x
        rel_y = event.y

        result = self.controller.check_click(rel_x, rel_y) 

        if result == "correct":
            self.draw_found_marker(rel_x, rel_y, color="red")
            if self.controller.is_game_complete():
                self.message_label.config(text="You Win!", fg="green")
        elif result == "wrong":
            self.message_label.config(text="Wrong! Try again.", fg="orange")
        elif result == "locked":
            self.message_label.config(text="GAME OVER: Too many mistakes", fg="red")
            messagebox.showinfo("Locked", "Too many mistakes! Game Over.") 

        self.update_labels() 

    def draw_found_marker(self, x, y, color="red"):
        """Draws circles on BOTH images for found differences."""
        r = 15
        # Draw on original
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, width=3)
        # Draw on modified
        self.canvas.create_oval((x+self.tk_orig.width())-r, y-r, (x+self.tk_orig.width())+r, y+r, outline=color, width=3)

    def reveal_differences(self):
        """Reveals all unfound differences in blue. """
        for diff in self.controller.differences:
            if not diff["found"]:
                cx, cy = diff["center"]
                self.draw_found_marker(cx, cy, color="blue") 
        
        self.message_label.config(text="Differences Revealed", fg="blue")
        self.reveal_btn.config(state="disabled")

    def update_labels(self):
        """Updates the text on screen. """
        self.score_label.config(text=f"Score: {self.controller.score}")
        self.mistake_label.config(text=f"Mistakes: {self.controller.mistakes}/3")
