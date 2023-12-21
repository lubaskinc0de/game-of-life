from dataclasses import dataclass

from game_of_life.domain.value_objects.node_position import NodePosition


@dataclass
class Node:
    position: NodePosition
    neighbors: list["Node"]
    is_alive: bool = False

    @property
    def alive_neighbors(self) -> int:
        return len(list(filter(lambda n: n.is_alive, self.neighbors)))

    @property
    def is_able_to_survive(self) -> bool:
        return self.alive_neighbors == 2 or self.alive_neighbors == 3

    @property
    def is_able_to_born(self) -> bool:
        return self.alive_neighbors == 3

    def __bool__(self) -> bool:
        return self.is_alive

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.position.__str__()
