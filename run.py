import config

from model import Environment
from qlearning import QLearning

def main(grid_file="grid.txt"):
    env = Environment(grid_file, config.rewards)
    learner = QLearning(env)
    print("Initial grid state:")
    env.print_grid_state()
    learner.learn(config.n_episodes, config.max_timesteps, config.lr, config.disc, config.epsilon)

if __name__ == "__main__":
    main()
