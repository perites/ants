import pygame
import random
import math
pygame.init()

width, height = 2080, 1080
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Aints")
exit = False


class myColor():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.light_blue = (0, 255, 255)


my_color = myColor()

BACKGROUND_COLOR = my_color.black


class Ant():
    def __init__(self, radius, position, target_point, speed, area_radius, area_color, points_coords, direction, ):
        self.radius = radius
        self.position = position
        self.target_point = target_point
        self.speed = speed
        self.area_radius = area_radius
        self.area_color = area_color
        self.points_coords = points_coords
        self.get_direction_to_coords(direction)

        self.rect_obj = pygame.draw.circle(screen, BACKGROUND_COLOR, self.position, self.radius)
        self.area_obj = pygame.draw.circle(screen, BACKGROUND_COLOR, self.position, self.area_radius)

        self.set_color()
        # self.color = my_color.white

    def set_color(self):
        if self.target_point == "pointA":
            self.color = my_color.blue
        elif self.target_point == "pointB":
            self.color = my_color.yellow

    def draw_self(self):
        self.rect_obj = pygame.draw.circle(screen, self.color, self.position, self.radius)
        self.area_obj = pygame.draw.circle(screen, self.area_color, self.position, self.area_radius, width=1)

    def calculate_next_position(self):
        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
        if self.check_collision_window():
            self.calculate_next_position()

    def move_to_position(self):
        self.calculate_next_position()
        self.points_coords["pointA"] += 0.1  # self.speed
        self.points_coords["pointB"] += 0.1  # self.speed
        self.draw_self()

    def check_collision_window(self):
        ant_x, ant_y = self.position
        if not self.radius * 2 <= ant_x <= (width - self.radius * 2):
            self.direction[0] = -self.direction[0]
            # self.direction[1] = -self.direction[1]
            # self.direction = random.choice(ant_colony.centers)
            self.fix_position(ant_x=ant_x)
            return True
        if not self.radius * 2 <= ant_y <= (height - self.radius * 2):
            self.direction[1] = -self.direction[1]
            # self.direction[0] = -self.direction[0]
            # self.direction = random.choice(ant_colony.centers)
            self.fix_position(ant_y=ant_y)
            return True
        return False

    def fix_position(self, ant_x=None, ant_y=None):

        position_list = []

        if ant_x:
            if ant_x < self.radius * 2:
                position_list.insert(0, self.radius * 2)
            elif ant_x > (width - self.radius * 2):
                position_list.insert(0, (width - self.radius * 3))

            position_list.insert(1, self.position[1])

        elif ant_y:
            if ant_y < self.radius * 2:
                position_list.insert(1, self.radius * 3)
            elif ant_y > (height - self.radius * 2):
                position_list.insert(1, (height - self.radius * 3))

            position_list.insert(0, self.position[0])

        self.position = position_list

    def get_direction_to_coords(self, coords):
        coords = [coords[0] - self.position[0], coords[1] - self.position[1]]
        k = math.sqrt(coords[0]**2 + coords[1]**2) / self.speed
        self.direction = [coords[0] / k, coords[1] / k]

    def get_direction(self, other_ant):
        self.direction = [-other_ant.direction[0], -other_ant.direction[1]]

    def check_collision_points(self, pointA, pointB):
        if self.rect_obj.colliderect(pointA):
            self.points_coords["pointA"] = 0
            self.direction[0] = -self.direction[0]
            self.direction[1] = -self.direction[1]

            if self.target_point == "pointA":
                self.target_point = "pointB"
                # self.set_color()
                self.color = my_color.white

        if self.rect_obj.colliderect(pointB):
            self.points_coords["pointB"] = 0
            self.direction[0] = -self.direction[0]
            self.direction[1] = -self.direction[1]

            if self.target_point == "pointB":
                self.target_point = "pointA"
                # self.set_color()
                self.color = my_color.white

    def check_points_coords(self, other_ant):
        other_ant_coord_a, other_ant_coord_b = other_ant.points_coords.values()

        other_ant_coord_a += self.area_radius
        other_ant_coord_b += self.area_radius

        if other_ant_coord_a < self.points_coords["pointA"]:
            self.points_coords["pointA"] = other_ant_coord_a
            if self.target_point == "pointA":

                self.get_direction(other_ant)

        if other_ant_coord_b < self.points_coords["pointB"]:
            self.points_coords["pointB"] = other_ant_coord_b
            if self.target_point == "pointB":
                self.get_direction(other_ant)


class AntsManager():
    def __init__(self, amount, ants_radius, ants_speed, area_radius, area_color, points):
        self.ants = []
        self.amount = amount
        self.ants_radius = ants_radius
        self.ants_speed = ants_speed

        self.area_radius = area_radius
        self.area_color = area_color

        self.points = points

    def set_centres(self):
        return [(random.randint(self.ants_radius * 3, width - (self.ants_radius * 3)),
                 random.randint(self.ants_radius * 3, height - (self.ants_radius * 3))) for x in range(self.amount)]
        # return [(width / 2, height / 2)]

    def create_ants(self):
        for center in self.set_centres():
            self.ants.append(Ant(self.ants_radius, center,
                                 random.choice(["pointA", "pointB"]),
                                 speed=random.uniform(10, 11),
                                 area_radius=self.area_radius,
                                 points_coords={"pointA": random.randint(1, self.amount), "pointB": random.randint(1, self.amount)},
                                 direction=random.choice(self.set_centres()),
                                 area_color=self.area_color))

        self.check_collision_ants()

    def check_collision_ants(self):
        ok_ants = []
        ants_obj = [ant.rect_obj for ant in self.ants.copy()]
        for ant in self.ants:
            ant_obj = ant.rect_obj
            ants_obj.remove(ant_obj)
            if ant_obj.collidelist(ants_obj) == -1:
                ok_ants.append(ant)

        self.ants = ok_ants

    def draw_ants(self):
        for ant in self.ants:
            ant.draw_self()

    def find_ant(self, ant_area_obj):
        for ant in self.ants:
            if ant.area_obj == ant_area_obj:
                return ant

    def listen(self):
        ants_area_obj = [ant.area_obj for ant in self.ants]
        for ant in self.ants:
            ant_area_obj = ant.area_obj
            ants_area_obj.remove(ant_area_obj)
            collision = ant_area_obj.collidelist(ants_area_obj)

            if collision != -1:

                collided_ant = self.find_ant(ants_area_obj[collision])
                ant.check_points_coords(collided_ant)

        ants_area_obj.append(ant_area_obj)


point_radius = 20
pointA_center = (500, 500)
pointB_center = (1500, 800)
pointA_color = my_color.blue
pointB_color = my_color.yellow


ant_colony = AntsManager(amount=2000, ants_radius=2, ants_speed=random.uniform(10, 11), area_radius=10, area_color=my_color.black, points=[])
ant_colony.create_ants()


class RenderManager(AntsManager):
    def __init__(self, fps_amount):
        self.fps = pygame.time.Clock()
        self.fps_amount = fps_amount
        self.paused = False

    def update(self):
        for ant in ant_colony.ants:
            ant.move_to_position()
            ant.check_collision_points(self.pointA, self.pointB)
        ant_colony.listen()

        # ant_colony.ants[1].get_direction(ant_colony.ants[0].position)

        # ant_colony.ants[1].move_to_position()
        # ant_colony.ants[0].move_to_position()

        # ant.get_direction(ant_colony.ants)
        # ant.get_direction(self.pointA, self.pointB)
        # print(ant.target_point)

        # print(ant.target_point)
        # print(ant.points_coords)
        # print(ant.direction)

        # print()

    def render(self):
        screen.fill(BACKGROUND_COLOR)
        self.draw_points()
        self.update()

        pygame.display.update()
        # self.fps.tick(self.fps_amount)

    def draw_points(self):
        self.pointA = pygame.draw.circle(screen, pointA_color, pointA_center, point_radius)
        self.pointB = pygame.draw.circle(screen, pointB_color, pointB_center, point_radius)


rm = RenderManager(fps_amount=60)
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                rm.paused = not rm.paused

    if not rm.paused:
        rm.render()
