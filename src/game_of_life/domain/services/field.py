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

        for x in range(width):
            for y in range(height):
                position = NodePosition((x, y))
                node = Node(position, [])

                if position in alive_nodes:
                    node.is_alive = True

                nodes[position] = node

        field = Field(width=width, height=height, nodes=nodes)

        return field
