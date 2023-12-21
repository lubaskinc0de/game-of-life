import random
import time

import pygame as p
from pygame import QUIT

from game_of_life.domain.entities.field import Field
from game_of_life.domain.services.field import FieldService
from game_of_life.domain.value_objects.node_position import NodePosition

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def generate_random_field(width, height) -> Field:
    alive_nodes: list[NodePosition] = []

    for y in range(height):
        for x in range(width):
            if random.random() < 0.5:
                alive_nodes.append(NodePosition((x, y)))

    field_service = FieldService()
    field = field_service.create(width=width, height=height, alive_nodes=alive_nodes)

    return field


def main():
    width = 50
    height = 50

    window_width = 400
    window_height = 400

    field = generate_random_field(width, height)

    block_size = window_width // width

    window = p.display.set_mode((window_width, window_height))

    while True:
        window.fill(WHITE)

        for x in range(0, window_width, block_size):
            for y in range(0, window_height, block_size):
                rect = p.Rect(x, y, block_size, block_size)

                position = NodePosition((x // block_size, y // block_size))
                node = field.get_node(position)

                if not node:
                    p.draw.rect(window, BLACK, rect, 1)
                else:
                    p.draw.rect(window, BLACK, rect)

        for i in p.event.get():
            if i.type == QUIT:
                quit()

        field.next_generation()

        p.display.update()

        time.sleep(1 / 10)


if __name__ == "__main__":
    main()
