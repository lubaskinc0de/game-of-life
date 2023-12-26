import random
from typing import Optional

from game_of_life.domain.entities.field import Field
from game_of_life.domain.entities.node import Node
from game_of_life.domain.value_objects.node_position import NodePosition


class FieldService:
    def create(self,
               width: Optional[int] = None,
               height: Optional[int] = None,
               alive_nodes: Optional[list[NodePosition]] = None,
               ) -> Field:
        nodes: dict[NodePosition, Node] = dict()

        for x in range(width + 1):
            for y in range(height + 1):
                position = NodePosition((x, y))
                node = Node(position, [])

                if position in alive_nodes:
                    node.is_alive = True

                nodes[position] = node

        field = Field(width=width, height=height, nodes=nodes)

        for node_position, node in nodes.items():
            node.neighbors = field.get_neighbors(node_position)

        return field

    def random(self,
               width: Optional[int] = None,
               height: Optional[int] = None,
               ):
        alive_nodes: list[NodePosition] = []

        for y in range(height):
            for x in range(width):
                if random.random() < 0.4:
                    alive_nodes.append(NodePosition((x, y)))

        field = self.create(width=width, height=height, alive_nodes=alive_nodes)

        return field
