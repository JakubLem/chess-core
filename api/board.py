from api import labels


class Field:
    def __init__(self) -> None:
        self.field = None

    def set_field(self, label):
        self.field = label


class Board:
    def __init__(self) -> None:
        self.arr = [[Field() for _ in range(8)] for _ in range(8)]
        self.labels = labels.Labels()
        self.set_pieces()

    def set_pieces(self):
        for pawn_row in [1, 6]:
            for i in range(8):
                self.arr[pawn_row][i].set_field(self.labels.PAWN_LABEL)

    def json(self):
        ...
