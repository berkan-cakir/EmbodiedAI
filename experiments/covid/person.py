import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *


class Person(Agent):
    def __init__(self, pos, v, population, index: int, mode, color='blue', image: str = "experiments/covid/images/susceptible.png") -> None:
        super(Person, self).__init__(
            pos,
            v,
            color=color,
            index=index,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
        )

        self.population = population
        self.timer = 0
        self.view_radius = config['agent']['radius']
        self.mode = mode
        self.p_infection = 0.1
        base_image, rect = image_with_rect(image, [10, 10])
        self.rect = rect
        self.image = base_image

    def update_actions(self) -> None:
        neighbours = self.population.find_neighbors(self, self.view_radius)
        self.timer += 1

        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        for wall0 in self.population.objects.wall0:
            collide = pygame.sprite.collide_mask(self, wall0)
            if bool(collide):
                self.avoid_obstacle()

        for wall1 in self.population.objects.wall1:
            collide = pygame.sprite.collide_mask(self, wall1)
            if bool(collide):
                self.avoid_obstacle()

        for wall2 in self.population.objects.wall2:
            collide = pygame.sprite.collide_mask(self, wall2)
            if bool(collide):
                self.avoid_obstacle()

        for wall3 in self.population.objects.wall3:
            collide = pygame.sprite.collide_mask(self, wall3)
            if bool(collide):
                self.avoid_obstacle()

        for wall4 in self.population.objects.wall4:
            collide = pygame.sprite.collide_mask(self, wall4)
            if bool(collide):
                self.avoid_obstacle()

        if self.timer % 50 == 0:
            for neighbour in neighbours:
                if neighbour.mode == 'infected' and self.mode == 'susceptible' and self.p_infection < np.random.rand():
                    self.change_mode('infected')
                    self.data_update()
                    self.timer = 0
        if self.timer > 300 and self.mode == 'infected':
            self.change_mode('removed')
            self.data_update()
            self.timer = 0

    def change_mode(self, mode):
        if mode == 'infected':
            self.mode = 'infected'
            self.image = "experiments/covid/images/infected.png"
        elif mode == 'removed':
            self.mode = 'removed'
            self.image = "experiments/covid/images/removed.png"
        else:
            self.mode = 'susceptible'
            self.image = "experiments/covid/images/susceptible.png"

        width = config["agent"]["width"]
        height = config["agent"]["height"]
        base_image, rect = image_with_rect(self.image, [width, height])
        self.image = base_image


    def data_update(self):
        self.population.datapoints = []
        for person in self.population.agents:
            if person.mode == 'susceptible':
                self.population.datapoints.append('S')
            elif person.mode == 'infected':
                self.population.datapoints.append('I')
            elif person.mode == 'removed':
                self.population.datapoints.append('R')