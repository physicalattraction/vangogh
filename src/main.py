import argparse
import os.path
from typing import List, Tuple

from van_gogh import GridType, VanGogh

default_grid_sizes = [1, 2, 5, 10, 15, 20, 25, 50, 75]
default_grid_types = [GridType.HEX.value, GridType.SQUARE.value, GridType.RANDOM.value]
help_grid_sizes = 'The various grid sizes (space separated) to create images for. ' \
                  'Each grid size must be a integer between [0, 100]. ' \
                  f'Optional, if none are given the default is used: {default_grid_sizes}'
help_grid_types = 'The various grid types (space separated) to create images for. ' \
                  f'Valid grid types are {GridType.HEX.value}, {GridType.SQUARE.value} and {GridType.RANDOM.value}.' \
                  f'Optional, if none are given the default is used: {default_grid_types}'


def parse_args() -> Tuple[List[int], List[GridType]]:
    parser = argparse.ArgumentParser()
    parser.description = 'Turn your pictures into marvels of wonder from the Dutch master Vincent van Gogh himself!'
    parser.add_argument('--grid_sizes', type=int, nargs='+', help=help_grid_sizes)
    parser.add_argument('--grid_types', type=str, nargs='+', help=help_grid_types)
    args = parser.parse_args()

    # Fill in defaults for missing arguments
    if not args.grid_sizes:
        args.grid_sizes = default_grid_sizes
    if not args.grid_types:
        args.grid_types = default_grid_types

    # Convert values to GridType enum objects
    args.grid_types = [GridType(grid_type) for grid_type in args.grid_types]

    return args.grid_sizes, args.grid_types


def pointillize_input_img(grid_sizes: List[int], grid_types: List[GridType]):
    vincent.set_input_img(input_filename)
    filename_base, _ = os.path.splitext(input_filename)

    for grid_size in grid_sizes:
        vincent.set_grid_size(grid_size)
        print(f'Pointillizing {filename_base} with grid size {grid_size}')
        for grid_type in grid_types:
            vincent.pointillize_img(grid_type)
            output_filename = f'{filename_base}_{grid_type.value}_{grid_size}p'
            vincent.save(output_filename)


if __name__ == '__main__':
    _grid_sizes, _grid_types = parse_args()
    vincent = VanGogh()
    for input_filename in vincent.get_input_images():
        pointillize_input_img(_grid_sizes, _grid_types)
