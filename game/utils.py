from typing import Tuple, List

def center_of(coords: Tuple[int, int]) -> float:
    """
    Calculate the center point of the given coordinates.
    
    Parameters:
        coords (Tuple[int, int]): A tuple containing the x and y coordinates.
    """
    return sum(coords) / 2

def center_of_rect(x_coords: Tuple[int, int], y_coords: Tuple[int, int]) -> List[int]:
    """
    Calculate the center point of a rectangle given its x and y coordinates.
    
    Parameters:
        x_coords (Tuple[int, int]): The start_x, end_x of the rectangle.
        y_coords (Tuple[int, int]): The start_y, end_y of the rectangle.
    """
    return [center_of(x_coords), center_of(y_coords)]
