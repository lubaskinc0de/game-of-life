import time

import pygame as p
from pygame import QUIT

from game_of_life.domain.services.field import FieldService
from game_of_life.domain.value_objects.node_position import NodePosition

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    width = 100
    height = 100

    window_width = 400
    window_height = 400

    field_service = FieldService()
    field = field_service.random(width, height)

    block_size = window_width // width

    window = p.display.set_mode((window_width, window_height))
    p.display.set_caption("Жизнь")

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
