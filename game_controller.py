class GameController:
    """
    Controls game logic such as scoring and click detection.
    """

    def __init__(self, difference_locations, max_mistakes=3):
        """
        Constructor for GameController.
        """
        pass

    def get_remaining(self):
        pass

    def check_click(self, x, y):
        """
        Checks if click is correct or wrong.

        Returns:
            "correct", "wrong", or "locked"
        """
        pass

    def update_score(self):
        """Updates player score."""
        pass

    def update_mistakes(self):
        """Updates mistake counter."""
        pass

    def is_game_complete(self):
        """Checks if all differences are found."""
        pass

    def is_locked(self):
        """Checks if player exceeded mistake limit."""
        pass