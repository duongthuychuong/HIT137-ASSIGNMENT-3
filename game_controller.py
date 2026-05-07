import math

class GameController:
    """
    Controls game logic such as scoring and click detection.
    """

    def __init__(self, difference_locations, max_mistakes=3):
        """
        Constructor for GameController.
        """
        self.differences = difference_locations  # List of dicts with x, y, center, found, etc.
        self.score = 0
        self.mistakes = 0
        self.max_mistakes = max_mistakes
        self.locked = False
        self.click_radius = 30  # Margin of error for clicks

    def get_remaining(self):
        """Returns the number of unfound differences."""
        return sum(1 for d in self.differences if not d["found"])

    def check_click(self, x, y):
        """
        Checks if click is correct or wrong.

        Returns:
            "correct", "wrong", or "locked"
        """
        if self.is_locked():
            return "locked"

        for diff in self.differences:
            if not diff["found"]:
                # Calculate distance between click and center of difference
                dist = math.sqrt((x - diff["center"][0])**2 + (y - diff["center"][1])**2)

                if dist <= self.click_radius:
                    diff["found"] = True
                    self.update_score()
                    return "correct"
        
        self.update_mistakes()
        if self.is_locked():
            return "locked"
        return "wrong"

    def update_score(self):
        """Updates player score."""
        self.score += 1

    def update_mistakes(self):
        """Updates mistake counter."""
        self.mistakes += 1
        if self.mistakes >= self.max_mistakes:
            self.locked = True

    def is_game_complete(self):
        """Checks if all differences are found."""
        return all(diff["found"] for diff in self.differences)

    def is_locked(self):
        """Checks if player exceeded mistake limit."""
        return self.locked
