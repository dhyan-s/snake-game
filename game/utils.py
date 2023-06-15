from typing import Tuple, List

def center_of(coords: Tuple[int, int]):
    return sum(coords) / 2

def center_of_rect(x_coords: Tuple[int, int], y_coords: Tuple[int, int]) -> List[int]:
    return [center_of(x_coords), center_of(y_coords)]
