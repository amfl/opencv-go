from sgfmill import sgf
import numpy as np

class GameNode:
    def __init__(self):
        self.state = None
        self.parent = None
        self.sgf_node = None

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
        self.sgf_game = sgf.Sgf_game(size=size)

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

            sgf_node = None
            if gn.parent:
                diffs = gn.difference_from_parent()
                if len(diffs) == 1 and gn.parent.sgf_node is not None:
                    # This could be a valid sgf move.
                    node = gn.parent.sgf_node.new_child()
                    try:
                        # Can throw an error if this move is invalid.
                        node.set_move(diffs[0][0], diffs[0][1])
                        sgf_node = node
                    except ValueError:
                        print("ERROR: Invalid move.")
                        print("Further moves on this branch not recordable.")
                        node.delete()
            else:
                # This is the first move!
                print("made the first move.")
                sgf_node = self.sgf_game.get_last_node()

            gn.sgf_node = sgf_node

            self.state_map[hashable] = gn
        else:
            print("Rollback!")

        # Keep track of the current state
        self.current_state = hashable

        return True, self.state_map[hashable]
