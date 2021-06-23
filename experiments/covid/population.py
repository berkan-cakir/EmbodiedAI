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
        self.r0 = {1: config['base']['inf_index']}
        self.points_to_plot = {'S': [], 'I': [], 'R': [], 'D':[]}

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


        if config["base"]["scenario"] == 'E':
            cities = [
                (55, 450, 55, 250),(450, 945, 55, 250),
                (55, 450, 350, 650),(550, 950, 350, 650),
                (55, 450, 750, 950),(550, 950, 750, 950),
            ]
        else:
            min_x, max_x = 550, 950
            min_y, max_y = 100, 950

        num_infected = config['base']['inf_index']
        infected_agents = [random.randint(0,num_agents) for i in range(num_infected)]
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            if config["base"]["scenario"] == 'E':
                min_x, max_x, min_y, max_y = random.choice(cities)
            while (
                    coordinates[0] >= max_x
                    or coordinates[0] <= min_x
                    or coordinates[1] >= max_y
                    or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            if index in infected_agents:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, mode='infected'))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, mode='susceptible'))
