from dataclasses import dataclass

from game_of_life.domain.entities.node import Node
from game_of_life.domain.value_objects.node_position import NodePosition


def to_node_position(coords: tuple[int, int]) -> NodePosition:
    return NodePosition(coords)


@dataclass
class Field:
    nodes: dict[NodePosition, Node]
    width: int
    height: int

    def get_node(self, position: NodePosition) -> Node:
        x, y = position.x % self.width, position.y % self.height

        return self.nodes[NodePosition((x, y))]

    def get_neighbors(self, position: NodePosition) -> list[Node]:
        neighbors = []

        for x in range(position.x - 1, position.x + 2):
            for y in range(position.y - 1, position.y + 2):
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
                    if node.is_able_to_born != node.is_alive:
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

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "Field with {} nodes".format(len(self.nodes))
