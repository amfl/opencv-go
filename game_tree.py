class GameNode:
    def __init__(self):
        self.state = None
        self.parent = None

class GameTree:
    def __init__(self, size):
        # For quick access to all gamestates
        self.state_map = {}
        self.current_state = None

    def update(self, state):
        """Update the gametree.
        Returns:
            bool: True if board state changed, False otherwise.
        """

        # Convert state to something hashable
        hashable = str(state)

        # If this is the same as last time, no action required
        if self.current_state == hashable:
            return False

        # If we have not seen this state before..
        if not (hashable in self.state_map):
            print("Unique state!")
            gn = GameNode()
            gn.state = state
            gn.parent = self.current_state

            self.state_map[hashable] = gn
        else:
            print("Rollback!")

        # Keep track of the current state
        self.current_state = hashable

        return True
