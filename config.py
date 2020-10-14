from model import CellStates

n_episodes = 1000
max_timesteps = 100

lr = 0.1
disc = 1.0
epsilon = 0.1

rewards = {
    CellStates.EMPTY: -1,
    CellStates.GOAL: 25,
    CellStates.TRAP: -25
}

# If set to True, perform all learning before visualization
offline = True