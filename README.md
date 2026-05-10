# Spot the Difference Game

A Python desktop game built with **Tkinter** and **OpenCV** for HIT137 Assignment 3.

The program loads an image, creates a modified copy with random visual differences, displays the original and modified images side by side, and lets the player click the differences.

---

## Features

- Load images using a file picker.
- Resize images to fit the game window while keeping the correct aspect ratio.
- Display the original and modified images side by side.
- Generate 5 random differences each round.
- Prevent difference areas from overlapping.
- Support multiple difference types:
    - Blur difference
    - Colour difference
    - Brightness difference
    - Added transparent object/sticker difference
- Detect player clicks on the modified image.
- Draw red circles on both images when a difference is found.
- Track score, remaining differences, and mistakes.
- Lock the game after 3 wrong clicks.
- Reveal remaining differences in blue.
- Upload a new image and restart the round.

---

## Requirements

Install Python 3.10 or later.

This project uses the following Python libraries:

```bash
opencv-python
numpy
Pillow
```

Tkinter is also required. It is included with most Python installations, but on some systems it may need to be installed separately.

---

## Project Structure

```text
spot-the-difference/
│
├── main.py
├── start_screen.py
├── image_processor.py
├── difference.py
├── difference_generator.py
├── game_controller.py
├── game_display.py
│
├── assets/
│   ├── ball.png
│   ├── banana.png
│   ├── bird.png
│   ├── cat.png
│   └── leaf.png
│
└── README.md
```

### File Explanation

#### `main.py`

Entry point of the application.

It creates the Tkinter root window, opens the start screen, and starts the main GUI event loop.

Run this file to start the game.

---

#### `start_screen.py`

Controls the first screen shown to the user.

Responsibilities:

- Show the game title.
- Let the user choose an image.
- Create the image processor.
- Generate the modified image.
- Create the game controller.
- Open the main game display.
- Centre the window on the screen.

---

#### `image_processor.py`

Handles image preparation.

Responsibilities:

- Load an image using OpenCV.
- Resize the image to fit the game window.
- Keep the original aspect ratio.
- Create a copy of the image before modification.

This keeps image-processing logic separate from GUI logic.

---

#### `difference.py`

Contains the difference classes.

This file uses inheritance and polymorphism.

The base class is:

```python
class Difference:
```

Each difference subclass inherits from `Difference` and implements the same method:

```python
apply(image, box)
```

Current subclasses:

```python
BlurDifference
ColorDifference
BrightnessDifference
AddObjectDifference
```

Because every difference class has the same `apply()` method, the generator can choose any difference type randomly and apply it without needing separate logic for each one.

---

#### `difference_generator.py`

Creates the modified image.

Responsibilities:

- Choose random locations for differences.
- Keep difference boxes inside the image.
- Prevent boxes from overlapping.
- Randomly choose a difference type.
- Apply each difference to the copied image.
- Return the modified image and the list of difference locations.

The returned location data is used later by the game controller to check whether a player clicked correctly.

---

#### `game_controller.py`

Controls the game rules.

Responsibilities:

- Store all difference locations.
- Check whether a click is correct or wrong.
- Track the score.
- Track mistakes.
- Stop the game after 3 mistakes.
- Check whether all differences have been found.
- Count remaining differences.

This file does not draw anything on the screen. It only handles the game logic.

---

#### `game_display.py`

Controls the main game screen.

Responsibilities:

- Display the original and modified images.
- Convert OpenCV images into Tkinter-compatible images.
- Handle mouse clicks.
- Draw markers for correct answers.
- Update labels for score, mistakes, and remaining differences.
- Show messages such as correct click, wrong click, game over, and completed game.
- Reveal remaining differences.
- Allow the user to upload a new image.

This file connects the visual interface to the game controller.

---

#### `assets/`

Stores transparent PNG objects used by `AddObjectDifference`.

The current code expects these files:

```text
ball.png
banana.png
bird.png
cat.png
leaf.png
```

These images should have transparent backgrounds. If they do not have an alpha channel, the object difference may not display correctly.

---

## How to Run the Project

### 1. Open the project folder

In Terminal or Command Prompt, go to the project folder:

```bash
cd path/to/spot-the-difference
```

Example:

```bash
cd "Assignment 3"
```

---

### 2. Create a virtual environment

Recommended:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install opencv-python numpy Pillow
```

---

### 4. Check the assets folder

Make sure the project has this folder:

```text
assets/
```

And make sure it contains:

```text
ball.png
banana.png
bird.png
cat.png
leaf.png
```

The app can still run without these files, but the added-object difference may not appear.

---

### 5. Run the game

```bash
python main.py
```

On macOS, if `python` does not work, use:

```bash
python3 main.py
```

---

## How to Play

1. Run `main.py`.
2. Click **Choose Image**.
3. Select an image file.
4. The game will show two images:
    - Left: original image
    - Right: modified image
5. Click on the differences in the right image.
6. Correct clicks are marked with red circles on both images.
7. Wrong clicks increase the mistake counter.
8. After 3 mistakes, the game is locked.
9. Click **Reveal Differences** to show remaining differences in blue.
10. Click **Upload Image** to start a new round.

---

## Supported Image Types

The file picker supports:

```text
.jpg
.jpeg
.png
.bmp
```

For best results, use clear images with enough detail. Very plain images with solid colours may make some differences hard to notice.

---

## OOP Design Explanation

This project follows an object-oriented structure.

### Encapsulation

Each class has a clear responsibility:

- `ImageProcessor` handles image loading and resizing.
- `DifferenceGenerator` creates random difference locations.
- `GameController` manages score and game rules.
- `GameDisplay` handles the GUI.
- `StartScreen` handles the first screen.

This makes the code easier to read, test, and maintain.

### Inheritance

The `Difference` class is the parent class.

The difference types inherit from it:

```python
class BlurDifference(Difference)
class ColorDifference(Difference)
class BrightnessDifference(Difference)
class AddObjectDifference(Difference)
```

This allows all difference types to share the same structure.

### Polymorphism

Every difference class has an `apply(image, box)` method.

Because the method name is the same, `DifferenceGenerator` can randomly choose a difference class and call:

```python
diff.apply(modified, box)
```

without needing to know exactly which difference type was selected.

This is a strong example of polymorphism.

---

## Common Problems and Fixes

### `ModuleNotFoundError: No module named 'cv2'`

OpenCV is not installed in the Python environment you are using.

Fix:

```bash
pip install opencv-python
```

If you are using PyCharm, make sure the package is installed in the same interpreter selected in PyCharm.

---

### `ModuleNotFoundError: No module named 'PIL'`

Pillow is not installed.

Fix:

```bash
pip install Pillow
```

---

### Added object does not appear

Check that the `assets` folder exists and contains the expected PNG files.

Also check that the PNG files have transparent backgrounds. The object difference needs PNG images with an alpha channel.

---

### Wrong click shows even when the difference looks correct

The click detection uses the centre point of each difference and a tolerance radius based on the difference box size.

If detection feels too strict or too loose, adjust this part in `game_controller.py`:

```python
radius = max(bw, bh) // 2 + 10
```

Increasing `+ 10` makes clicks easier to detect.

---

## Main Command

Use this command to run the final app:

```bash
python main.py
```

or:

```bash
python3 main.py
```
