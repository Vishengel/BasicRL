# GridworldRL
Implementation of Q-learning for simple grid worlds.

Run with:
python run.py --g "gridfile.txt"
Where gridfile.txt consists of a character-based grid in a rectangular shape.

Example:          Legend:
WWWWWWWW          C = Cell (empty grid cell)
WCCTCCGW          W = Wall (inaccessible by agent)
WCCWWWCW          T = Trap (forces the agent to restart)
WCCCCWCW          S = Starting position (only one possible)
WCCWCWCW          G = Goal (multiple possible)
WCCWCWCW
WSCWCCCW
WWWWWWWW

The walls around the grid are optional, as the boundary condition is non-periodic.

The learning parameters can be set in config.py. Currently, the agent learns for the set amount of episodes before the visualization starts. Setting the "offline" parameter to False currently does not work.
