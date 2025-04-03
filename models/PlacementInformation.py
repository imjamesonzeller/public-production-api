class PlacementInformation():
    def __init__(self, word, coords, direction):
        self.word: str = word
        self.coords: tuple[int, int] = coords
        self.direction: dict[str, int] = direction