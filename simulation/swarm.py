import pygame

from simulation.agent import Agent
from simulation.objects import Objects
from simulation.utils import dist

"""
General swarm class that defines general swarm properties, which are common across different swarm types
"""


class Swarm(pygame.sprite.Sprite):
    """
    Base class for the swarm of agents simulation. This class will contain the total amount of agents and obstacles
    which are present in the simulation. It will also handle the update and display of each element (agent or obstacle)
    for each frame of the GUI, as it extends the base class pygame.sprite.Sprite

    Attributes:
    ----------
         dist_temp:
         agents:
         screen:
         objects:
         points_to_plot:
         datapoints:

    """

    def __init__(self, screen_size, plot=None) -> None:
        """
        Args:
        ----
            screen_size:
            plot: Defaults to None
        """
        super(Swarm, self).__init__()
        self.dist_temp: dict = {}
        self.agents: list = []
        self.screen = screen_size
        self.objects: Objects = Objects()
        self.points_to_plot = plot
        self.rich_plot = plot
        self.poor_plot = plot
        self.datapoints: list = []
        self.poor_datapoints: list = []
        self.rich_datapoints: list = []

    def add_agent(self, agent: Agent) -> None:
        """
        Adds an agent to the pool of agents in the swarm

        Args:
        ----
            agent (Agent):

        """
        self.agents.append(agent)

    def compute_distance(self, a: Agent, b: Agent) -> float:
        """
        This method computes the euclidean distance between the considered agent and another agent of the swarm, and
        saves the result in a temporary dictionary, so the inverse (i.e. distance a-b is the same as distance b-a) does
        not need to be recomputed for this frame.

        Args:
        ----
            a (Agent): Agent in question that is performing the check of its surroundings
            b (Agent): Another of the swarm

        """
        indexes = (a.index, b.index)
        pair = (min(indexes), max(indexes))

        if pair not in self.dist_temp:
            self.dist_temp[pair] = dist(a.pos, b.pos)
        return self.dist_temp[pair]

    def find_neighbors(self, agent: Agent, radius: float) -> list:
        """
        Try to locate all the neighbors of the given agent, considering a specified radius, by computing the euclidean
        distance between the agent and any other member of the swarm

        Args:
        ----
            agent (Agent):
            radius (float):

        """
        #  Check that the each other agent is not our considered one, if the type is None or infected, and the distance
        return [neighbor for neighbor in self.agents if
                agent is not neighbor and
                neighbor.type in [None, "I"] and
                self.compute_distance(agent, neighbor) < radius]

    def remain_in_screen(self) -> None:
        """
        Before displaying everything on the next frame, check if every agent is withtin the screen (on the x or y axis).
        If it is outside of the screen, reposition it at the center.
        """
        for agent in self.agents:
            if agent.pos[0] > self.screen[0]:
                agent.pos[0] = 0.0
            if agent.pos[0] < 0:
                agent.pos[0] = float(self.screen[0])
            if agent.pos[1] < 0:
                agent.pos[1] = float(self.screen[1])
            if agent.pos[1] > self.screen[1]:
                agent.pos[1] = 0.0

    def add_point(self, lst) -> None:
        """
        Plots the number of infected and recovered

        Args:
        ----
            lst:

        """
        # Count current numbers
        values = {"S": 0, "I": 0, "R": 0, "D": 0}
        for state in lst:
            values[state] += 1

        for x in values.keys():
            self.points_to_plot[x].append(values[x])

    def add_rich_point(self, lst) -> None:
        # Count current numbers
        values = {"S": 0, "I": 0, "R": 0, "D": 0}
        for state in lst:
            values[state] += 1

        for x in values.keys():
            self.rich_plot[x].append(values[x])

    def add_poor_point(self, lst) -> None:
        # Count current numbers
        values = {"S": 0, "I": 0, "R": 0, "D": 0}
        for state in lst:
            values[state] += 1

        for x in values.keys():
            self.poor_plot[x].append(values[x])

    def update(self) -> None:
        """
        Updates every agent, and if there is any datapoint (i.e. any change in sane-infected-recovered) add it to the
        points to be plotted. Finally, check if every agent is within the screen.
        """
        # update the movement
        self.datapoints = []
        self.rich_datapoints = []
        self.poor_datapoints = []
        for agent in self.agents:
            agent.update_actions()
        if self.datapoints:
            self.add_point(self.datapoints)
        if self.rich_datapoints:
            self.add_rich_point(self.rich_datapoints)
        if self.poor_datapoints:
            self.add_poor_point(self.poor_datapoints)
        self.remain_in_screen()


    def display(self, screen: pygame.Surface) -> None:
        """
        Display the updated agents and objects for the next frame, and reset the temporary dictionary for finding
        the neighbors

        Args:
        ----
            screen (pygame.Surface):

        """
        for obstacle in self.objects.obstacles:
            obstacle.display(screen)

        for site in self.objects.sites:
            site.display(screen)

        for wall0 in self.objects.wall0:
            wall0.display(screen)

        for wall1 in self.objects.wall1:
            wall1.display(screen)

        for wall2 in self.objects.wall2:
            wall2.display(screen)

        for wall3 in self.objects.wall3:
            wall3.display(screen)

        for wall4 in self.objects.wall4:
            wall4.display(screen)

        for wall5 in self.objects.wall5:
            wall5.display(screen)

        for wall6 in self.objects.wall6:
            wall6.display(screen)

        for wall7 in self.objects.wall7:
            wall7.display(screen)

        for wall8 in self.objects.wall8:
            wall8.display(screen)

        for wall9 in self.objects.wall9:
            wall9.display(screen)

        for wall10 in self.objects.wall10:
            wall10.display(screen)

        for wall11 in self.objects.wall11:
            wall11.display(screen)

        for wall12 in self.objects.wall12:
            wall12.display(screen)

        for wall12 in self.objects.wall13:
            wall12.display(screen)

        for agent in self.agents:
            agent.update()
            agent.display(screen)
            agent.reset_frame()

        self.dist_temp = {}
