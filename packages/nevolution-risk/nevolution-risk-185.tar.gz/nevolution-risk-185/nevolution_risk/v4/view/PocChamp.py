# Proof of concept goes here
import os
from random import randint
from time import sleep

import numpy as np
import pygame
import pygame.freetype
import pygame.freetype
from pygame.cursors import load_xbm

from nevolution_risk.constants.colors import blue, black, deep_pink, water_blue
from nevolution_risk.constants.view_settings import coordinates, radius, width, height
from nevolution_risk.v4.logic import Graph
from PIL import Image

graph = [[], [2, 3, 5], [1, 3, 4], [1, 2, 7], [2, 5, 6], [1, 4, 6], [4, 5, 7], [3, 6, 9], [9, 10], [7, 8, 10], [8, 9]]
graph1 = Graph((1, 2))


def poc_render(surface, grid):
    surface.fill(deep_pink)

    for edge in grid:
        pygame.draw.line(surface, blue, edge[0], edge[1], 10)

    n = 0
    for position in coordinates:
        pygame.draw.circle(surface, graph1.nodes[n].player.color, position, radius)
        n = n + 1


def is_inside(pos1, pos2):
    square = (pos1[0] - pos2[0]) * (pos1[0] - pos2[0]) + (pos1[1] - pos2[1]) * (pos1[1] - pos2[1])
    if square < radius * radius:
        return True
    else:
        return False


def find_node(position):
    for n in range(1, 11):
        if is_inside(coordinates[n], position):
            return n

    return 0


def render_tests():
    pygame.init()
    display = pygame.display.set_mode((width, height))
    running = True
    loop = True
    current_player = 1

    grid = []
    for n in range(1, 10):
        for adjacent in graph1.nodes[n].adj_list:
            grid.append((coordinates[n], coordinates[adjacent.id]))

    node1 = 0
    pos1 = (0, 0)
    pos2 = (0, 0)
    mouse_pressed = False

    dir_name = os.path.dirname(os.path.realpath(__file__))
    void_path = os.path.join(dir_name, '../res', 'void.xbm')
    void_mask_path = os.path.join(dir_name, '../res', 'void-mask.xbm')

    void_cursor = load_xbm(void_path, void_mask_path)
    sword = pygame.image.load(os.path.join(dir_name, '../res', 'sword.png'))

    while running:
        if graph1.is_conquered():
            print("done")
            running = False

        pos2 = pygame.mouse.get_pos()
        poc_render(surface=display, grid=grid)

        if mouse_pressed:
            pygame.draw.line(display, black, pos1, pos2, 10)
            display.blit(sword, pos2)

        sleep(1 / 100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if not mouse_pressed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos1 = pygame.mouse.get_pos()
                        node1 = find_node(pos1)
                        mouse_pressed = True
                        pygame.mouse.set_cursor(*void_cursor)

            if mouse_pressed:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        node2 = find_node(pos2)
                        if current_player == 1:
                            if (node1 != 0) and (node2 != 0):
                                graph1.attack(node1, node2, graph1.player1)
                                current_player = 2
                        else:
                            if (node1 != 0) and (node2 != 0):
                                graph1.attack(node1, node2, graph1.player2)
                                current_player = 1

                    mouse_pressed = False
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


def playground():
    pygame.init()
    pygame.freetype.init()

    display = pygame.display.set_mode((width, height))
    running = True

    dir_name = os.path.dirname(os.path.realpath(__file__))
    country_images = []

    for index in range(42):
        filename = str(index) + ".png"
        country_images.append(pygame.image.load(os.path.join(dir_name, '../../output', filename)))

        country_images[index].fill((0, 0, 0), special_flags=pygame.BLEND_MIN)

    map = pygame.image.load(os.path.join(dir_name, '../../output', "blank.png"))

    for country in country_images:
        map.blit(country, (0, 0))

    grid = pygame.image.load(os.path.join(dir_name, '../../output', "grid.png"))
    map.blit(grid, (0, 0))

    picture_matrix = []
    for i in range(width):
        picture_matrix.append([-2] * height)

    for index in range(len(country_images)):
        for x in range(len(picture_matrix)):
            for y in range(len(picture_matrix[0])):
                if country_images[index].get_at((x, y))[3] > 0:
                    picture_matrix[x][y] = index

    while running:
        test_draw(display, map)
        pygame.display.update()
        pos1 = pygame.mouse.get_pos()

        x = pos1[0]
        y = pos1[1]

        alpha = picture_matrix[x][y]

        print(alpha)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


mult = 1.56
r = 30


def test_draw_node(surface, font):
    pos = [400, 400]
    length = np.sqrt(2) * r
    pos[0] = pos[1] - (length / 2) * 1.14
    pos[1] = pos[1] - (length / 2) * 0.8
    position = (int(pos[0]), int(pos[1]))
    pygame.draw.circle(surface, (255, 255, 255), (400, 400), r)

    font.render_to(surface, position, "75")


def test_draw(surface, picture):
    surface.fill(water_blue)
    surface.blit(picture, (0, 0))


def refine_images():
    for number in range(42):
        filename = str(number) + ".png"

        dir_name = os.path.dirname(os.path.realpath(__file__))
        image = Image.open(os.path.join(dir_name, '../../res/raw', filename))
        pixelMap = image.load()
        print(pixelMap[0, 3])
        print(image.size[0])

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if pixelMap[i, j][0] > 127 and pixelMap[i, j][1] > 127 and pixelMap[i, j][2] > 127:
                    pixelMap[i, j] = (255, 255, 255, 255)
                else:
                    pixelMap[i, j] = (0, 0, 0, 0)

        image = image.resize((1280, 720))

        image.show()

        output_path = os.path.join(dir_name, '../../output', filename)
        image.save(output_path)

        image.close()


def refine_grid():
    filename = "grid.png"

    dir_name = os.path.dirname(os.path.realpath(__file__))
    image = Image.open(os.path.join(dir_name, '../../res/raw', filename))
    pixelMap = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pixelMap[i, j][3] > 0:
                pixelMap[i, j] = (0, 0, 0, 255)
            else:
                pixelMap[i, j] = (255, 255, 255, 0)

    image = image.resize((1280, 720))

    image.show()

    output_path = os.path.join(dir_name, '../../output', filename)
    image.save(output_path)

    image.close()


if __name__ == '__main__':
    refine_grid()
