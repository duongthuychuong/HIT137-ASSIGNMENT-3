class GameController:
    """
    Controls game logic such as scoring and click detection.
    """

    def __init__(self, difference_locations, max_mistakes=3):
        """
        Constructor for GameController.
        """
        # Store maximum allowed mistakes
        self.max_mistakes = max_mistakes

        # Initialize score and mistakes
        self.score = 0
        self.mistakes = 0

        # Normalize difference data: ensure each difference has a `found` flag and a `center`
        self.differences = []
        if difference_locations:
            for d in difference_locations:
                diff = dict(d)  # shallow copy
                diff.setdefault("found", False)
                if "center" not in diff:
                    # compute center from x,y,width,height if present
                    if all(k in diff for k in ("x", "y", "width", "height")):
                        diff["center"] = (diff["x"] + diff["width"] // 2, diff["y"] + diff["height"] // 2)
                    else:
                        diff["center"] = (0, 0)
                self.differences.append(diff)
        else:
            self.differences = []

    def get_remaining(self):
        """Return the number of differences not yet found."""
        return sum(1 for d in self.differences if not d.get("found", False))

    def update_score(self):
        """Updates player score."""
        self.score += 1
        return self.score

    def update_mistakes(self):
        """Updates mistake counter."""
        self.mistakes += 1
        return self.mistakes

    def is_game_complete(self):
        """Checks if all differences are found."""
        return self.get_remaining() == 0

    def is_locked(self):
        """Checks if player exceeded mistake limit."""
        return self.mistakes >= self.max_mistakes

    def check_click(self, x, y):
        """
        Handle a click at image coordinates (x, y).

        Returns:
            'correct' if a new difference was found,
            'wrong' if the click missed,
            'locked' if the player exceeded mistake limit.
        """

        if self.is_locked():
            return "locked"

        # Check each unfound difference for a hit
        for diff in self.differences:
            if diff.get("found"):
                continue

            cx, cy = diff.get("center", (0, 0))
            # Accept hits within a radius relative to the box size
            bw = diff.get("width", 30)
            bh = diff.get("height", 30)
            radius = max(bw, bh) // 2 + 10

            dx = x - cx
            dy = y - cy
            if dx * dx + dy * dy <= radius * radius:
                diff["found"] = True
                self.update_score()
                return "correct"

        # Missed all differences
        self.update_mistakes()
        if self.is_locked():
            return "locked"
        return "wrong"