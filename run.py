import argparse
import config
import pygame

from gui import GUI
from model import CellStates, Environment
from qlearning import QLearning

def run_pygame(env, learner):
    pg = pygame.init()
    clock = pygame.time.Clock()
    running = True
    gui = GUI(pg, env)
    gui.draw(env)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.QUIT:
                running = False

        cur_state = env.grid[env.agent.pos[1]][env.agent.pos[0]]

        if cur_state.state == CellStates.GOAL or cur_state.state == CellStates.TRAP:
            learner.teleport_agent(env.start)
        else:
            action, _, _ = learner.get_greedy_action(cur_state)
            learner.move_agent(action)

        gui.draw(env)

        clock.tick(5)

def main(grid_file="grid.txt"):
    # Initialize environment and learner
    env = Environment(grid_file, config.rewards)
    learner = QLearning(env)
    print("Initial grid state:")
    env.print_grid_state()

    if config.offline:
        learner.learn_offline(config.n_episodes, config.max_timesteps, config.lr, config.disc, config.epsilon)

    run_pygame(env, learner)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--g', dest='grid_file', type=str, default='grid.txt')
    args = parser.parse_args()
    main(args.grid_file)

