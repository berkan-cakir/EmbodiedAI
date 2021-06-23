import numpy as np
import pygame
import math

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
        width = config["agent"]["width"]
        height = config["agent"]["height"]
        base_image, rect = image_with_rect(image, [height, width])
        self.rect = rect
        self.image = base_image
        self.inf_gen = 1 if self.mode == 'infected' else 0
        self.age = random.randint(20,89) # To keep ages between 20 to 90
        self.p_death = config['person']['p_death'][int(self.age/10) - 2]
        self.separation_strength = 1
        if config['person']['groups']:
            self.group = random.choice(config['person']['category'])
            self.separation_strength = config[self.group]['separation_strength']
            self.p_infection = config[self.group]['p_infection']
        if self.mode == 'infected': self.change_mode('infected')

    def update_actions(self) -> None:
        neighbours = self.population.find_neighbors(self, self.view_radius)
        self.timer += 1
        if config['base']['social_distancing']:
            self.social_distancing()
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        if True:
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

            for wall5 in self.population.objects.wall5:
                collide = pygame.sprite.collide_mask(self, wall5)
                if bool(collide):
                    self.avoid_obstacle()

            for wall6 in self.population.objects.wall6:
                collide = pygame.sprite.collide_mask(self, wall6)
                if bool(collide):
                    self.avoid_obstacle()

            for wall7 in self.population.objects.wall7:
                collide = pygame.sprite.collide_mask(self, wall7)
                if bool(collide):
                    self.avoid_obstacle()

            for wall8 in self.population.objects.wall8:
                collide = pygame.sprite.collide_mask(self, wall8)
                if bool(collide):
                    self.avoid_obstacle()

            for wall9 in self.population.objects.wall9:
                collide = pygame.sprite.collide_mask(self, wall9)
                if bool(collide):
                    self.avoid_obstacle()

            for wall10 in self.population.objects.wall10:
                collide = pygame.sprite.collide_mask(self, wall10)
                if bool(collide):
                    self.avoid_obstacle()

            for wall11 in self.population.objects.wall11:
                collide = pygame.sprite.collide_mask(self, wall11)
                if bool(collide):
                    self.avoid_obstacle()

            for wall12 in self.population.objects.wall12:
                collide = pygame.sprite.collide_mask(self, wall12)
                if bool(collide):
                    self.avoid_obstacle()

            for wall13 in self.population.objects.wall12:
                collide = pygame.sprite.collide_mask(self, wall13)
                if bool(collide):
                    self.avoid_obstacle()

        if self.timer % 50 == 0:
            for neighbour in neighbours:
                if config['base']['variable_infection']:
                    distance = dist(self.pos, neighbour.pos)
                    p_infection = 1/math.exp(distance)
                else:
                    p_infection = self.p_infection

                if neighbour.mode == 'infected' and self.mode == 'susceptible' and p_infection < np.random.rand():
                    self.change_mode('infected')
                    self.inf_gen = neighbour.inf_gen + 1
                    self.update_r0(self.inf_gen)
                    self.data_update()
                    self.timer = 0

        if self.timer > 300 and self.mode == 'infected':
            if self.p_death > np.random.rand():
                self.change_mode('dead')
                self.v = [0, 0]
            else:
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
        elif mode == 'dead':
            self.mode = 'dead'
            self.image = "experiments/covid/images/dead.png"
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
            elif person.mode == 'dead':
                self.population.datapoints.append('D')

    def update_r0(self, index):
        if index in self.population.r0.keys():
            self.population.r0[index] += 1
        else:
            self.population.r0[index] = 1

    def social_distancing(self):
        if self.mode != 'dead':
            neighbours = self.population.find_neighbors(self, config["agent"]["radius"])
            separate = np.zeros(2)
            if neighbours:
                for neigh in neighbours:
                    difference = (self.pos - neigh.pos)
                    difference /= norm(difference)
                    separate += difference
                separate = separate/len(neighbours)
            else:
                separate = (np.zeros(2))

            self.steering += truncate(
                separate*self.separation_strength / self.mass, config["agent"]["max_force"]
            )
        else:
            separate = (np.zeros(2))

            self.steering += truncate(
                10 * separate * self.separation_strength / self.mass, config["agent"]["max_force"]
            )
            self.v = 0