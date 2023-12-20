from dataclasses import dataclass

from game_of_life.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class NodePosition(ValueObject[tuple[int, int]]):
    value: tuple[int, int]

    @property
    def x(self) -> int:
        return self.value[0]

    @property
    def y(self) -> int:
        return self.value[1]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NodePosition):
            return False

        return other.x == self.x and other.y == self.y

    def __str__(self) -> str:
        return "X: {0}, Y: {1}".format(self.x, self.y)
