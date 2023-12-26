import logging

from game_of_life.domain.entities.field import Field


class FieldManager:
    fields: dict[int, tuple[Field, bool]]  # field, is_running

    def __init__(self):
        self.fields = {}

    def set(self, user_id: int, field: Field) -> None:
        self.fields[user_id] = (field, False)

    def get(self, user_id: int) -> Field:
        return self.fields[user_id][0]

    def remove(self, user_id: int) -> None:
        self.fields.pop(user_id)

    def is_running(self, user_id: int) -> bool:
        cell = self.fields.get(user_id, False)

        if cell:
            return cell[1]

        return cell

    def run(self, user_id: int) -> None:
        cell = self.fields[user_id]
        self.fields[user_id] = (cell[0], True)

        logging.info("Run evolve for user %d", user_id)

    def stop(self, user_id: int) -> None:
        cell = self.fields[user_id]

        self.fields[user_id] = (cell[0], False)
        logging.info("Stop evolve for user %d", user_id)
