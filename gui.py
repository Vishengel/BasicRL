import pygame

from model import CellStates

class GUI():

    def __init__(self, pg, env):
        self.pg = pg
        pygame.font.init()
        pygame.display.set_caption("RL Sim")
        self.screen_dim = (600,600)
        self.screen = pygame.display.set_mode(self.screen_dim)

        self.cell_size = 50
        self.grid_disp_size = (len(env.grid[0])*self.cell_size, len(env.grid)*self.cell_size)
        self.grid_disp = pygame.Surface(self.grid_disp_size)

        self.cell_colors ={
            CellStates.GOAL: (0, 255, 0),
            CellStates.TRAP: (255, 0, 0),
            CellStates.WALL: (0, 0, 0)
        }

    def draw(self, env):
        # Draw white background
        self.screen.fill((77,77,77))
        #self.grid_disp.fill((100,100,50))

        for row in env.grid:
            cell_y = row[0].pos[1] * self.cell_size
            for cell in row:
                cell_x = cell.pos[0] * self.cell_size

                if cell.occupied:
                    color = (0, 0, 255)
                elif cell.state in self.cell_colors.keys():
                    color = self.cell_colors[cell.state]
                else:
                    color = (255,255,255)

                pygame.draw.rect(self.grid_disp, (0, 0, 0), pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.grid_disp, color, pygame.Rect(cell_x+1, cell_y+1, self.cell_size-2, self.cell_size-2))

        self.screen.blit(self.grid_disp, (0 + self.screen_dim[0] / 2 - self.grid_disp_size[0] / 2,
                                          0 + self.screen_dim[1] / 2 - self.grid_disp_size[1] / 2))
        pygame.display.flip()
