from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        # To do

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """

        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        # coordinates = generate_coordinates(self.screen)
        #
        # if config["population"]["obstacles"]:  # you need to define this variable
        #     for obj in self.objects.obstacles:
        #         rel_coordinate = relative(
        #             coordinates, (obj.rect[0], obj.rect[1])
        #         )
        #         try:
        #             while obj.mask.get_at(rel_coordinate):
        #                 coordinates = generate_coordinates(self.screen)
        #                 rel_coordinate = relative(
        #                     coordinates, (obj.rect[0], obj.rect[1])
        #                 )
        #         except IndexError:
        #             pass

        self.points_to_plot = {'S': [], 'I': [], 'R': []}

        if config["base"]["scenario"] == 'Z':
            self.objects.add_object(file="experiments/covid/images/box.png",
                                    pos=[500, 500],
                                    scale=config["base"]["scale"],
                                    obj_type="obstacle")
        elif config["base"]["scenario"] == 'A':
                self.objects.add_object(file="experiments/covid/images/2.png",
                                        pos=[500, 500],
                                        scale=config["base"]["scale"],
                                        obj_type="obstacle")
        elif config["base"]["scenario"] == 'B':
            self.objects.add_object(file="experiments/covid/images/2_partial.png",
                                    pos=[500, 500],
                                    scale=config["base"]["scale"],
                                    obj_type="obstacle")
        elif config["base"]["scenario"] == 'C':
            self.objects.add_object(file="experiments/covid/images/4.png",
                                    pos=[500, 500],
                                    scale=config["base"]["scale"],
                                    obj_type="obstacle")
        elif config["base"]["scenario"] == 'D':
            self.objects.add_object(file="experiments/covid/images/4_partial.png",
                                    pos=[500, 500],
                                    scale=config["base"]["scale"],
                                    obj_type="obstacle")
        elif config["base"]["scenario"] == 'E':
            self.objects.add_object(file="experiments/covid/images/6_partial.png",
                                    pos=[500, 500],
                                    scale=config["base"]["scale"],
                                    obj_type="obstacle")


        min_x, max_x = 550, 950
        min_y, max_y = 750, 950

        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            if index % 35 == 0:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, mode='infected'))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, mode='susceptible'))
