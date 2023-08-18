import pygame
import random
import math


pygame.init()
width, height = 2080, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aints")
font = pygame.font.Font('freesansbold.ttf', 32)
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
    def __init__(self, radius, position, ant_id, speed, area_radius, area_color, direction, points_obj, first_count, how_much_increase_every_step):
        self.radius = radius
        self.position = position
        self.ant_id = ant_id
        self.speed = speed
        self.area_radius = area_radius
        self.area_color = area_color

        self.points_obj = points_obj
        self.counter = {}
        self.first_count = first_count
        self.how_much_increase_every_step = how_much_increase_every_step

        self.get_target_point()

        self.get_direction_to_coords(direction)

        self.ant_obj = pygame.draw.circle(screen, BACKGROUND_COLOR, self.position, self.radius)
        self.area_obj = pygame.draw.circle(screen, BACKGROUND_COLOR, self.position, self.area_radius)

        self.set_color()
        # self.color = my_color.white

    def get_target_point(self, old_target_point=None):
        new_target_point = random.choice(list(self.points_obj.keys()))

        if old_target_point:
            while new_target_point == old_target_point:
                new_target_point = random.choice(list(self.points_obj.keys()))

        self.target_point = new_target_point

    def set_color(self):
        self.color = ant_colony.points[self.target_point].color

    def draw_self(self):
        self.ant_obj = pygame.draw.circle(screen, self.color, self.position, self.radius)
        self.area_obj = pygame.draw.circle(screen, self.area_color, self.position, self.area_radius, width=1)

    def calculate_next_position(self):
        self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
        if self.check_collision_window():
            self.calculate_next_position()

    def move_to_position(self):
        self.calculate_next_position()
        self.increase_points_dist()
        self.draw_self()

    def increase_points_dist(self):
        for point in self.points_obj:
            try:
                self.counter[point] += self.how_much_increase_every_step
            except KeyError:
                self.counter[point] = self.first_count

    def check_collision_window(self):
        ant_x, ant_y = self.position
        if not self.radius * 2 <= ant_x <= (width - self.radius * 2):
            self.direction[0] = -self.direction[0]
            # self.direction[1] = -self.direction[1]
            self.fix_position(ant_x=ant_x)
            return True
        if not self.radius * 2 <= ant_y <= (height - self.radius * 2):
            self.direction[1] = -self.direction[1]
            # self.direction[0] = -self.direction[0]
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

    def check_collision_points(self, points_list):
        self.points_obj = points_list
        points_obj = list(self.points_obj.values())
        collision = self.ant_obj.collidelist(points_obj)
        if collision != -1:
            collidet_point = self.find_point(points_obj[collision])
            self.counter[collidet_point] = 0
            self.direction[0] = -self.direction[0]
            self.direction[1] = -self.direction[1]

            if self.target_point == collidet_point:
                self.get_target_point(self.target_point)
                self.color = my_color.white
                # self.set_color()

                GLOBAL_COUNTER[collidet_point]["counter"] += 1
                if self.ant_id not in GLOBAL_COUNTER[collidet_point]["ants_id"]:
                    GLOBAL_COUNTER[collidet_point]["ants_id"].append(self.ant_id)

    def find_point(self, point_obj):
        for k, v in self.points_obj.items():
            if v == point_obj:
                return k

    def check_points_coords(self, other_ant):
        self.color = my_color.green
        for point_name in self.counter:
            if other_ant.counter[point_name] + other_ant.area_radius < self.counter[point_name]:
                self.counter[point_name] = other_ant.counter[point_name] + other_ant.area_radius
                if self.target_point == point_name:
                    self.get_direction(other_ant)
                    # self.get_direction_to_coords(other_ant.position)


class AntsManager():
    def __init__(self, amount, ants_radius, ants_speed, area_radius, area_color, points, first_count, how_much_increase_every_step):
        self.ants = []
        self.amount = amount

        self.ants_radius = ants_radius
        self.ants_speed = ants_speed
        self.area_radius = area_radius
        self.area_color = area_color

        self.first_count = first_count
        self.how_much_increase_every_step = how_much_increase_every_step

        self.points = {}
        self.points_obj = {}
        self.create_points(points)

    def set_centres(self):
        return [(random.randint(self.ants_radius * 3, width - (self.ants_radius * 3)),
                 random.randint(self.ants_radius * 3, height - (self.ants_radius * 3))) for x in range(self.amount)]
        # return [(width / 2, height / 2)]

    def create_points(self, points):
        for point in points:
            self.points[point.name] = point
            self.points_obj[point.name] = point.point_obj

    def create_ants(self):
        centers = self.set_centres()
        for x in range(0, amount - 1):
            self.ants.append(Ant(self.ants_radius, centers[x], ant_id=x,
                                 speed=self.ants_speed,
                                 area_radius=self.area_radius,
                                 area_color=self.area_color,
                                 direction=random.choice(self.set_centres()),
                                 points_obj=self.points_obj,
                                 first_count=self.first_count,
                                 how_much_increase_every_step=self.how_much_increase_every_step
                                 ))

        self.check_collision_ants()

    def check_collision_ants(self):
        ok_ants = []
        ants_obj = [ant.ant_obj for ant in self.ants.copy()]
        for ant in self.ants:
            ant_obj = ant.ant_obj
            ants_obj.remove(ant_obj)
            if ant_obj.collidelist(ants_obj) == -1:
                ok_ants.append(ant)

        self.ants = ok_ants

    def draw_points(self):
        for point in self.points:
            self.points[point].draw_self_point()

    def draw_ants(self):
        for ant in self.ants:
            ant.draw_self()

    def find_ant(self, ant_area_obj):
        for ant in self.ants:
            if ant.area_obj == ant_area_obj:
                return ant

    # def listen(self):
    #     ants_area_obj = [ant.area_obj for ant in self.ants]

    #     for ant in self.ants:
    #         ant_area_obj = ant.area_obj
    #         ants_area_obj.remove(ant_area_obj)
    #         collision = ant_area_obj.collidelist(ants_area_obj)

    #         if collision != -1:
    #             collided_ant = self.find_ant(ants_area_obj[collision])
    #             ant.check_points_coords(collided_ant)

    #     ants_area_obj.append(ant_area_obj)
    def check_collision(self):
        raise NotImplementedError

    def listen(self):
        ants_area_obj = [ant.area_obj for ant in self.ants]

        for ant in self.ants:
            ant_obj = ant.ant_obj
            ants_area_obj.remove(ant.area_obj)
            collision = ant_obj.collidelist(ants_area_obj)
            # collision = self.check_collision()
            if collision != -1:
                collided_ant = self.find_ant(ants_area_obj[collision])
                ant.check_points_coords(collided_ant)

        ants_area_obj.append(ant.area_obj)


class Point():
    def __init__(self, name, color, center, radius):
        self.name = name
        self.color = color
        self.center = center
        self.radius = radius
        self.point_obj = pygame.draw.circle(screen, self.color, self.center, self.radius)

    def draw_self_point(self):
        self.point_obj = pygame.draw.circle(screen, self.color, self.center, self.radius)


points = [Point(name="pointBlue", color=my_color.blue, center=(400, 400), radius=20),
          Point(name="pointYellow", color=my_color.yellow, center=(1500, 800), radius=20), ]
# Point(name="pointLblue", color=my_color.light_blue, center=(1000, 300), radius=20),
# Point(name="pointRed", color=my_color.red, center=(1800, 200), radius=20)]


amount = 2000
ants_radius = 2
area_radius = 6
first_count = 10000

ant_colony = AntsManager(amount=amount, ants_radius=ants_radius, ants_speed=random.uniform(3, 10),
                         area_radius=area_radius, area_color=my_color.black,
                         points=points, first_count=first_count, how_much_increase_every_step=0.01)
ant_colony.create_ants()
GLOBAL_COUNTER = {point.name: {"counter": 0, "ants_id": []} for point in points}


class RenderManager():
    def __init__(self, fps_amount):
        self.fps = pygame.time.Clock()
        self.fps_amount = fps_amount
        self.paused = False

    def update(self):
        ant_colony.listen()
        for ant in ant_colony.ants:
            ant.move_to_position()
            ant.check_collision_points(ant_colony.points_obj)

    def prepare_text(self):
        text = ""
        for point_name in GLOBAL_COUNTER:
            try:
                original_ratio = round(GLOBAL_COUNTER[point_name]["counter"] / len(GLOBAL_COUNTER[point_name]["ants_id"]), 5)
                original_ants = len(GLOBAL_COUNTER[point_name]["ants_id"])
                text += f' {point_name} : {GLOBAL_COUNTER[point_name]["counter"]} ; {original_ants} ; { original_ratio} '
            except ZeroDivisionError:
                text += f'\n{point_name} : {GLOBAL_COUNTER[point_name]["counter"]} ; {0} '
        self.text = font.render(text, False, my_color.white)

    def render(self):
        screen.fill(BACKGROUND_COLOR)

        ant_colony.draw_points()
        self.update()

        self.prepare_text()
        screen.blit(self.text, (0, 0))

        pygame.display.update()
        self.fps.tick(self.fps_amount)


rm = RenderManager(fps_amount=120)
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                rm.paused = not rm.paused

    if not rm.paused:
        rm.render()
