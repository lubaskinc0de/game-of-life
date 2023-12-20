from dataclasses import dataclass

from game_of_life.domain.entities.node import Node
from game_of_life.domain.value_objects.node_position import NodePosition


@dataclass
class Field:
    nodes: dict[NodePosition, Node]
    width: int = 100
    height: int = 100

    def get_node(self, position: NodePosition) -> Node:
        return self.nodes.get(position)

    def get_neighbors(self, position: NodePosition) -> list[Node]:
        positions = {
            "top_y": (position.x, max(0, position.y - 1)),
            "bottom_y": (position.x, min(self.height, position.y + 1)),
            "left_x": (max(0, position.x - 1), position.y),
            "right_x": (min(self.width, position.x + 1), position.y),
            "top_left": (max(0, position.x - 1), max(0, position.y - 1)),
            "top_right": (min(self.width, position.x + 1), max(0, position.y - 1)),
            "bottom_left": (max(0, position.x - 1), min(self.height, position.y + 1)),
            "bottom_right": (min(self.width, position.x + 1), min(self.height, position.y + 1)),
        }

        neighbors: list[Node] = []

        for x, y in positions.values():
            neighbor_position = NodePosition((x, y))
            neighbor = self.get_node(neighbor_position)

            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def append(self, position: NodePosition):
        self.nodes[position] = Node(
            neighbors=self.get_neighbors(position),
            position=position,
        )

    def next_generation(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                position = NodePosition((x, y))
                node = self.get_node(position)
                neighbors = self.get_neighbors(position)

                node.neighbors = neighbors

                if not node.is_alive:
                    node.try_to_born()
                if node.is_alive:
                    node.try_to_survive()

    @property
    def is_anyone_alive(self) -> bool:
        return any(list(self.nodes.values()))
