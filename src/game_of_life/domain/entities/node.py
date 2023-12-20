from dataclasses import dataclass

from game_of_life.domain.value_objects.node_position import NodePosition


@dataclass
class Node:
    position: NodePosition
    neighbors: list["Node"]
    is_alive: bool = False

    @property
    def is_able_to_survive(self) -> bool:
        return len(self.neighbors) == 2 or len(self.neighbors) == 3

    @property
    def is_able_to_born(self) -> bool:
        return len(self.neighbors) == 3

    def try_to_born(self) -> None:
        if self.is_able_to_born:
            self.is_alive = True

    def try_to_survive(self) -> None:
        if not self.is_able_to_survive:
            self.is_alive = False

    def __bool__(self) -> bool:
        return self.is_alive
