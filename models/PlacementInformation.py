from dataclasses import dataclass

@dataclass
class PlacementInformation():
    word: str
    coords: tuple[int, int]
    direction: dict[str, int]