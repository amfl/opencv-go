# sgfmill

Ensure you can go:
  camera -> board hash -> `sgf.Tree_node`
Nothing on "my side" of the program needs to understand move history. It just needs map what it sees right now to sgfmill data structures.
From there, sgfmill ensures you can go:
  `Tree_node` -> `Sgf_game`
  `Tree_node` -> parent `Tree_node` to determine move history

Question: What is the difference between a `Tree_node` and a `move` (as returned by `sgf_moves.get_setup_and_moves`)?
Answer: Moves are simpler. Don't contain branching. You obtain a move list by processing Tree nodes.

Thinking:

Probably want to make my own class which has:
- A string version of an entire board state for simplicity
- A ref to a Tree node, if possible
Then store them in a big ol' set which uses `__eq__` and `__hash__` to look at the string board state

Problems with this approach: Relying on sgf for the tree structure to record move history will break down when someone makes an invalid move (playing A, playing B, removing A)
