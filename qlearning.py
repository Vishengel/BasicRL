import random

from model import Agent, CellStates

class QLearning():

    def __init__(self, env):
        self.env = env
        self.init_agent()
        self.init_qtable()

    def init_agent(self):
        if self.env.agent:
            self.teleport_agent(self.env.start)
        else:
            self.env.agent = Agent(self.env.start)
            self.set_occupation(self.env.agent.pos, True)


    def move_agent(self, dir):
        self.set_occupation(self.env.agent.pos, False)
        x = self.env.agent.pos[0]
        y = self.env.agent.pos[1]

        if dir == "UP":
            new_pos = (x, y-1)

        elif dir == "RIGHT":
            new_pos = (x+1, y)

        elif dir == "DOWN":
            new_pos = (x, y+1)

        elif dir == "LEFT":
            new_pos = (x-1, y)

        else:
            new_pos = (x,y)
            print("Error: invalid direction")
            exit(0)

        self.env.agent.pos = new_pos
        self.set_occupation(self.env.agent.pos, True)

    def teleport_agent(self, pos):
        self.set_occupation(self.env.agent.pos, False)
        self.env.agent.pos = pos
        self.set_occupation(self.env.agent.pos, True)

    def update_cell(self, pos, state):
        x = pos[0]
        y = pos[1]
        self.env.grid[y][x].state = state

    def set_occupation(self, pos, occupied):
        x = pos[0]
        y = pos[1]
        self.env.grid[y][x].occupied = occupied

    def init_qtable(self):
        self.qtable = {}

        for row in self.env.grid:
            for cell in row:
                x = cell.pos[0]
                y = cell.pos[1]

                for action in cell.actions:
                    key = "{}{}{}".format(x, y, action)
                    self.qtable[key] = 0.0

    def learn_offline(self, n_episodes, max_timesteps, lr, disc, epsilon):
        for ep in range(n_episodes):
            t = 0
            stop_condition = False
            self.init_agent()

            while not stop_condition:
                cur_pos = self.env.agent.pos
                cur_state = self.env.get_cell(cur_pos)

                if random.random() < epsilon:
                    action = random.choice(cur_state.actions)
                    cur_key = "{}{}{}".format(cur_pos[0], cur_pos[1], action)
                    cur_q = self.qtable[cur_key]
                else:
                    action, cur_q, cur_key = self.get_greedy_action(cur_state)

                self.move_agent(action)
                new_pos = self.env.agent.pos
                new_state = self.env.get_cell(new_pos)
                reward = new_state.reward

                _, new_state_best_q, _ = self.get_greedy_action(new_state)

                new_q = cur_q + lr*(reward + disc*new_state_best_q - cur_q)
                self.qtable[cur_key] = new_q

                t += 1

                if t == max_timesteps or new_state.state == CellStates.GOAL or new_state.state == CellStates.TRAP:
                    stop_condition = True


    def get_greedy_action(self, state):
        best_q = float("-inf")
        best_a = ""
        best_key = ""

        for a in state.actions:
            key = "{}{}{}".format(state.pos[0], state.pos[1], a)
            q = self.qtable[key]

            if q > best_q:
                best_q = q
                best_a = a
                best_key = key

        return best_a, best_q, best_key

    def print_policy(self):
        for row in self.env.grid:
            for cell in row:
                if len(cell.actions) > 0:
                    best_action, _, _ = self.get_greedy_action(cell)

                    if best_action == "UP":
                        print('^', end='')
                    if best_action == "RIGHT":
                        print('>', end='')
                    if best_action == "DOWN":
                        print('V', end='')
                    if best_action == "LEFT":
                        print('<', end='')

                else:
                    print(self.env.state_to_char[cell.state], end='')

            print()