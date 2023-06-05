from typing import Tuple, List

def center_of(x_coords: Tuple[int, int], y_coords: Tuple[int, int]) -> List[int]:
    return [sum(x_coords) / 2, sum(y_coords) / 2]
