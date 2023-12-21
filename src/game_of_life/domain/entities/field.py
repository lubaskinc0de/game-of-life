from dataclasses import dataclass

from game_of_life.domain.entities.node import Node
from game_of_life.domain.value_objects.node_position import NodePosition


def to_node_position(coords: tuple[int, int]) -> NodePosition:
    return NodePosition(coords)


@dataclass
class Field:
    nodes: dict[NodePosition, Node]
    width: int = 100
    height: int = 100

    def get_node(self, position: NodePosition) -> Node:
        return self.nodes.get(position)

    def get_neighbors(self, position: NodePosition) -> list[Node]:
        neighbors = []

        for x in range(max(position.x - 1, 0), min(position.x + 2, self.width)):
            for y in range(max(position.y - 1, 0), min(position.y + 2, self.height)):
                neighbor_position = NodePosition((x, y))
                if neighbor_position != position:
                    neighbors.append(self.get_node(neighbor_position))

        return neighbors

    def next_generation(self) -> None:
        updated_state: dict[NodePosition, bool] = dict()

        for x in range(self.width):
            for y in range(self.height):
                position = NodePosition((x, y))
                node = self.get_node(position)

                if not node.is_alive:
                    if node.is_able_to_born != (node.is_alive):
                        updated_state[position] = node.is_able_to_born
                else:
                    if node.is_able_to_survive != node.is_alive:
                        updated_state[position] = node.is_able_to_survive

        for position in updated_state:
            node = self.get_node(position)

            node.is_alive = updated_state[position]

    @property
    def is_anyone_alive(self) -> bool:
        return any(list(self.nodes.values()))
