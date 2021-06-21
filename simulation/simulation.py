import sys
import time

import matplotlib.pyplot as plt
import pygame

from typing import Union, Tuple

from experiments.aggregation.aggregation import Aggregations
from experiments.covid.population import Population
from experiments.flocking.flock import Flock

from experiments.covid.config import config


def _plot_covid(data) -> None:
    """
    Plot the data related to the covid experiment. The plot is based on the number of Susceptible,
    Infected and Recovered agents

    Args:
    ----
        data:

    """
    output_name = "experiments/covid/plots/Covid-19-SIR%s.png" % time.strftime(
        "-%m.%d.%y-%H:%M", time.localtime()
    )
    fig = plt.figure()
    plt.plot(data["S"], label="Susceptible", color=(1, 0.5, 0))  # Orange
    plt.plot(data["I"], label="Infected", color=(1, 0, 0))  # Red
    plt.plot(data["R"], label="Recovered", color=(0, 1, 0))  # Green
    plt.title("Covid-19 Simulation S-I-R")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.legend()
    fig.savefig(output_name)
    plt.show()


def _plot_flock() -> None:
    """Plot the data related to the flocking experiment. TODO"""
    pass


def _plot_aggregation() -> None:
    """Plot the data related to the aggregation experiment. TODO"""
    pass


"""
General simulation pipeline, suitable for all experiments 
"""


class Simulation:
    """
    This class represents the simulation of agents in a virtual space.
    """

    def __init__(
            self,
            num_agents: int,
            screen_size: Union[Tuple[int, int], int],
            swarm_type: str,
            iterations: int):
        """
        Args:
        ----
            num_agents (int):
            screen_size (Union[Tuple[int, int], int]):
            swarm_type (str):
            iterations (int):
        """
        # general settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = pygame.Color("gray21")
        self.iter = iterations
        self.swarm_type = swarm_type

        # swarm settings
        self.num_agents = num_agents
        if self.swarm_type == "flock":
            self.swarm = Flock(screen_size)

        elif self.swarm_type == "aggregation":
            self.swarm = Aggregations(screen_size)

        elif self.swarm_type == "covid":
            self.swarm = Population(screen_size)

        else:
            print("None of the possible swarms selected")
            sys.exit()

        # update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True

    def plot_simulation(self) -> None:
        """Depending on the type of experiment, plots the final data accordingly"""
        if self.swarm_type == "covid":
            _plot_covid(self.swarm.points_to_plot)
        elif self.swarm_type == "flock":
            _plot_flock()
        elif self.swarm_type == "aggregation":
            _plot_aggregation()

    def initialize(self) -> None:
        """Initialize the swarm, specifying the number of agents to be generated"""

        # initialize a swarm type specific environment
        self.swarm.initialize(self.num_agents)

    def simulate(self) -> None:
        """Here each frame is computed and displayed"""
        self.screen.fill(self.sim_background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if config["base"]["dynamic"]:
            self.dynamic_map_update()

        self.swarm.update()
        self.swarm.display(self.screen)

        pygame.display.flip()

    def dynamic_map_update(self):
        agents_infected_pos = []
        for person in self.swarm.agents:
            if person.mode == 'infected':
                agents_infected_pos.append(person.pos)

        if config["base"]["scenario"] == 'B':
            sector_infected1 = 0
            sector_infected2 = 0

            for pos in agents_infected_pos:
                if self.in_pos(pos, 0, 499, 0, 1000):
                    sector_infected1 += 1
                elif self.in_pos(pos, 500, 1000, 0, 1000):
                    sector_infected2 += 1

            if sector_infected1 > config["base"]["n_lockdown"] or sector_infected2 > config["base"]["n_lockdown"]:
                if len(self.swarm.objects.wall0.sprites()) == 0:
                    self.swarm.objects.add_object(file="experiments/covid/images/wall.png",
                                                  pos=[500, 500],
                                                  scale=[46, 800],
                                                  obj_type="wall0")
            else:
                if len(self.swarm.objects.wall0.sprites()) > 0:
                    self.swarm.objects.wall0.sprites()[0].kill()

        elif config["base"]["scenario"] == 'D':
            sector_infected1 = 0
            sector_infected2 = 0
            sector_infected3 = 0
            sector_infected4 = 0

        # for object in self.swarm.objects.obstacles.sprites():
        #     object.kill()
        #
        # for person in self.swarm.agents:
        #     print(person.pos)
        #     print(person.mode)

    def in_pos(self, pos, x1, x2, y1, y2):
        pos_x = int(pos[0])
        pos_y = int(pos[1])

        if x1 < pos_x < x2 and y1 < pos_y < y2:
            return True
        else:
            return False



    def run(self) -> None:
        """
        Main cycle where the initialization and the frame-by-frame computation is performed.
        The iteration con be infinite if the parameter iter was set to -1, or with a finite number of frames
        (according to iter)
        When the GUI is closed, the resulting data is plotted according to the type of the experiment.
        """
        # initialize the environment and agent/obstacle positions
        self.initialize()
        # the simulation loop, infinite until the user exists the simulation
        # finite time parameter or infinite

        if self.iter == float("inf"):

            while self.running:
                # init = time.time()
                self.simulate()
                # print(time.time() - init)

            self.plot_simulation()
        else:
            for i in range(self.iter):
                self.simulate()
            self.plot_simulation()
