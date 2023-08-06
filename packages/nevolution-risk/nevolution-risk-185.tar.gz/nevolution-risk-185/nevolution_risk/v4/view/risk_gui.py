"""
Author: Heinrich Sporys
"""

import os
import numpy as np
import pygame
import pygame.freetype

from pygame.cursors import load_xbm

from nevolution_risk.constants.colors import deep_pink, blue, black, dimgray, crimson, darkolivegreen, cadetblue, \
    chocolate, rosybrown, peachpuff, wood, water_blue
from nevolution_risk.constants.view_settings import width, height, radius, line_thickness, font_multiplier
from nevolution_risk.v4.view.utils import is_inside


class Gui(object):
    def __init__(self, graph, env):
        """
        creates a gui to allow the game to be displayed, sets up most important things to allow the rendering
        :param graph: graph, which is more like a gamestate, to use for the gui
        """
        self.graph = graph
        self.env = env
        self.game_display = None
        self.font = None
        self.rendering = True
        self.default_font = None
        self.font_init = False

        dir_name = os.path.dirname(os.path.realpath(__file__))
        self.sword = pygame.image.load(os.path.join(dir_name, '../../res', 'sword.png'))

        self.country_images = []

        for index in range(42):
            filename = str(index) + ".png"
            self.country_images.append(pygame.image.load(os.path.join(dir_name, '../../output', filename)))

            self.country_images[index].fill(self.graph.nodes[index].player.color, special_flags=pygame.BLEND_MIN)

        self.map = pygame.image.load(os.path.join(dir_name, '../../output', "blank.png"))

        for country in self.country_images:
            self.map.blit(country, (0, 0))

        self.grid = pygame.image.load(os.path.join(dir_name, '../../output', "grid.png"))
        self.map.blit(self.grid, (0, 0))

    def find_node(self, position):
        """
        finds the node at a given position in the gui, if there is one
        :param position: gui position coordinates of the point, near the node to find
        :return: integer, index in the nodes array of the matching node, 0 otherwise
        """
        for n in range(0, len(self.graph.nodes)):
            if is_inside(self.coordinates[n], position):
                return n
        return 0

    def update_country(self, country):
        self.country_images[country].fill((255, 255, 255), special_flags=pygame.BLEND_MAX)
        self.country_images[country].fill(self.graph.nodes[country].player.color, special_flags=pygame.BLEND_MIN)
        self.map.blit(self.country_images[country], (0, 0))
        self.map.blit(self.grid, (0, 0))

    def render(self, mode="human"):
        """
        renders the current state of the game saved in the graph, also opens the gui window on the first call
        :param mode: string, render mode, default is 'human' which does nothing special, 'rgb_array' causes the function
        to return a numpy array of the guis rgb-data as uint8s
        :return: a numpy array of the current gui if mode is 'rgb_array', None otherwise
        """
        if self.game_display is None:
            self.init()

        self.game_display.fill(water_blue)
        self.game_display.blit(self.map, (0, 0))
        for node in self.graph.nodes:
            self.draw_node(node)

        points1 = [(width - 150, 100), (width - 75, 0), (width, 100)]
        points2 = [(width - 150, 200), (width - 75, 300), (width, 200)]

        self.draw_text("stage: " + str(self.env.game_state), (width - 530, 630), 60)

        offset = 0
        self.env.gui.draw_text("cards", (200 - 170, 15), 60)
        for card in self.env.graph.players[0].cards:
            self.env.gui.draw_text(str(card.typ), (200 + offset, 15), 60)
            offset += 50
        self.env.gui.draw_text("troops: " + str(self.env.graph.players[0].troops), (width - 750, 15), 60)

        pygame.draw.rect(self.game_display, (255, 0, 0), ((width - 150, 0), (150, 100)))
        pygame.draw.polygon(self.game_display, dimgray, points1, 0)
        pygame.draw.rect(self.game_display, (0, 255, 0), ((width - 150, 200), (150, 100)))
        pygame.draw.polygon(self.game_display, dimgray, points2, 0)
        pygame.draw.rect(self.game_display, (0, 0, 255), ((width - 150, 300), (150, 100)))
        self.draw_text("exit", (width - 130, 320), 60)

        if mode == 'rgb_array':
            raw_pxarray = pygame.PixelArray(self.game_display)
            pxarray = []
            for row in raw_pxarray:
                row_px = []
                for pix in row:
                    tup = self.game_display.unmap_rgb(pix)
                    rgb = [tup[0], tup[1], tup[2]]
                    row_px.append(rgb)
                pxarray.append(row_px)
            return np.array(pxarray).astype(np.uint8)

        return None

    def init(self):
        """
        initializes pygame, the gui's font and creates a window to render to
        :return: None
        """
        pygame.init()
        self.game_display = pygame.display.set_mode((width, height))
        pygame.freetype.init()
        self.font = pygame.freetype.SysFont("bahnschrift", radius * font_multiplier, bold=True)

    def set_cursor_arrow(self):
        """
        makes the cursor visible
        :return: None
        """
        pygame.mouse.set_visible(True)

    def set_cursor_sword(self):
        """
        makes the cursor invisible allowing to draw another image (sword) at the cursors position
        :return:
        """
        pygame.mouse.set_visible(False)

    def draw_text(self, text, pos, size):
        """
        draws a text at a specified position in a specified size in the 'bahnschrift' font
        :param text: string to draw
        :param pos: position to draw at, in pixes coordinates, from the top left corner
        :param size: text font size
        :return: None
        """
        if not self.font_init:
            self.default_font = pygame.freetype.SysFont("bahnschrift", size)
            self.font_init = True

        self.default_font.render_to(self.game_display, pos, text)

    def draw_sword(self, pos1, pos2):
        """
        draws a sword at a given point and a line from the sword to another given point
        :param pos1: lines start position in  pixes coordinates, from the top left corner
        :param pos2: lines end position, also the position of the sword's point, pixes coordinates, from the top left
        :return: None
        """
        # en garde!
        pygame.draw.line(self.game_display, black, pos1, pos2, line_thickness)
        self.game_display.blit(self.sword, pos2)

    def draw_node(self, node):
        """
        draws a node in the countries graph, this draws a circle in a players color with background and the troop count
        as text
        :param node: Node, node to draw
        :return: None
        """
        pos = [0, 0]
        pos[0] = node.x
        pos[1] = node.y
        length = np.sqrt(2) * radius
        pos[0] = pos[0] - (length / 2) * 1.14
        pos[1] = pos[1] - (length / 2) * 0.8
        position = (int(pos[0]), int(pos[1]))

        if node.troops < 10:
            self.font.render_to(self.game_display, position, "0" + str(node.troops))
        else:
            self.font.render_to(self.game_display, position, str(node.troops))
