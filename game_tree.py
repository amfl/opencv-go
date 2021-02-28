import numpy as np

class GameNode:
    def __init__(self):
        self.state = None
        self.parent = None

    def difference_from_parent(self):
        try:
            diff = self.state - self.parent.state
        except AttributeError:
            # There is no parent for this state!
            return None
        changed_coords = np.nonzero(diff)

        # Convert coords into a list of moves
        # Format: [((2, 1), 'w')]
        moves = list(zip(changed_coords[0], changed_coords[1]))
        m = ['.', 'b', 'w']
        colors = [m[self.state[x[0], x[1]]] for x in moves]
        sgf_friendly_moves = list(zip(colors, moves))

        return sgf_friendly_moves

class GameTree:
    def __init__(self, size):
        # For quick access to all gamestates
        self.state_map = {}
        self.current_state = None

    def update(self, state):
        """Update the gametree.
        Returns:
            bool:     True if board state changed, False otherwise.
            GameNode: The current GameNode
        """

        # Convert state to something hashable
        hashable = str(state)

        # If this is the same as last time, no action required
        if self.current_state == hashable:
            return False, self.state_map[hashable]

        # If we have not seen this state before..
        if not (hashable in self.state_map):
            print("Unique state!")
            gn = GameNode()
            gn.state = state
            gn.parent = self.state_map.get(self.current_state, None)

            self.state_map[hashable] = gn
        else:
            print("Rollback!")

        # Keep track of the current state
        self.current_state = hashable

        return True, self.state_map[hashable]
