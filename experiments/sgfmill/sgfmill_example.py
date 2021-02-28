from sgfmill import ascii_boards
from sgfmill import sgf
from sgfmill import sgf_moves

def print_game(game):
    try:
        board, plays = sgf_moves.get_setup_and_moves(game)
    except ValueError as e:
        raise Exception(str(e))

    for colour, move in plays:
        if move is None:
            continue
        row, col = move
        try:
            print(colour)
            board.play(row, col, colour)
        except ValueError:
            raise Exception("illegal move in sgf file")

    # # Try to make a move on the existing board
    # print(game.serialise())
    # board.play(3,3,"w")
    # board.play(5,5,"w")

    print(ascii_boards.render_board(board))


game = sgf.Sgf_game.from_string("(;FF[4]GM[1]SZ[9];B[ee];W[ge])")

# board is hashable, but this does not change with the internal state.
# (But you can `board.copy()`!)
# print(hash(board))

print(game.serialise())
print_game(game)

print('------------------------------------------------------')

game = sgf.Sgf_game(size=13)
for move_info in [('w', (1,1)), ('b', (2,2))]:
    node = game.extend_main_sequence()
    node.set_move(move_info[0], move_info[1])
    print("Adding node: {} ({})".format(node, hash(node)))
    # if move_info.comment is not None:
    #     node.set("C", move_info.comment)

# Confirm that the hashes remain the same regardless of changing the move
for node in game.get_main_sequence():
    node.set_move('w', (1,1))
    print("Existing node: {} ({})".format(node, hash(node)))

# print(game.serialise())
# print_game(game)

print('------------------------------------------------------')

states = [
"""
.........
.........
.........
.........
.........
.........
.........
.........
.........
""".strip(),
"""
.........
.........
..#......
.........
.........
.........
.........
.........
.........
""".strip(),
"""
.........
.........
..#o.....
.........
.........
.........
.........
.........
.........
""".strip(),
# This move is intentionally the same as the previous
"""
.........
.........
..#o.....
.........
.........
.........
.........
.........
.........
""".strip(),
"""
.........
.........
..#......
.........
.........
.........
.........
.........
.........
""".strip(),
"""
.........
.........
..#......
..o......
.........
.........
.........
.........
.........
""".strip(),
]

def populate_node_with_diff(old_state, new_state, node):
    """Populates the given node with the difference between the old and new state"""
    # Get diff, represented as moves
    diff = None

    if old_state == None:
        return

    moves = []
    i = 0
    j = 0
    for c in range(len(old_state)):
        if old_state[c] == '\n':
            j += 1
            i = 0
        elif old_state[c] != new_state[c]:
            print(f"DIFF at {i} {j}")
            move_col = {"o": "w", "#": "b"}[new_state[c]]
            move_loc = (i, j)
            moves.append((move_col, move_loc))
        i += 1

    # Only listen to the first node so far
    if len(moves) > 0:
        node.set_move(moves[0][0], moves[0][1])

game = sgf.Sgf_game(size=9)
print(game.get_last_node())
move_map = {}
old_state = None
for i, state in enumerate(states):
    print(i, state)

    if state == old_state:
        continue

    # If we have not seen this state before..
    if not (state in move_map):

        try:
            parent_node = move_map[old_state]['node']
        except KeyError:
            # This may be the first state recorded
            parent_node = game.get_last_node()
        node = parent_node.new_child()

        populate_node_with_diff(old_state, state, node)

        # stick it into the map
        move_map[state] = {
            'parent': old_state,
            'node': node,
        }

    # Remember the old state
    old_state = state

for k, v in move_map.items():
    print(hash(k), "->", hash(v['parent']))

print(game.serialise())
# print(move_map)
