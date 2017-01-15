class athlete:

    """Generic class to represent an athelete

    """

    def __init__(self):
        self.activities = []

    def add_activity(self, act):
        self.activities.append(act)

        # Recalculate all form metrics (e.g. endurance) after adding a new activity

    def __str__(self):
        return "Athlete xxx with {} activities".format(len(self.activities))
