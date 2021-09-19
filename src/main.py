import argparse
import os.path
from typing import List, Tuple

from config import DEFAULT_OUTPUT_EXTENSION, DEFAULT_GRID_SIZES, DEFAULT_GRID_TYPES, DEFAULT_OUTPUT_WIDTH, MAX_GRID_SIZE
from grid_type import GridType
from van_gogh import IMAGE_EXTENSIONS, VanGogh

help_grid_sizes = 'The various grid sizes (space separated) to create images for. ' \
                  f'Each grid size must be a integer between [1, {MAX_GRID_SIZE}]. ' \
                  f'Optional, if none are given, the default is used: {DEFAULT_GRID_SIZES}'
help_grid_types = 'The various grid types (space separated) to create images for. ' \
                  f'Valid grid types are {GridType.HEX.value}, {GridType.SQUARE.value} and {GridType.RANDOM.value}.' \
                  f'Optional, if none are given, the default is used: {DEFAULT_GRID_TYPES}'
help_output_width = 'Width of the output image in pixels. The height is determined by the ratio of the input image. ' \
                    f'Optional, if not given, the default is used: {DEFAULT_OUTPUT_WIDTH}'
help_extension = f'The extension of the output images. ' \
                 f'Valid extensions are: {IMAGE_EXTENSIONS}. ' \
                 f'Optional, if not given, the default is used: {DEFAULT_OUTPUT_EXTENSION}'


def parse_args() -> Tuple[List[int], List[GridType], int, str]:
    parser = argparse.ArgumentParser()
    parser.description = 'Turn your pictures into marvels of wonder from the Dutch master Vincent van Gogh himself!'
    parser.add_argument('--grid_sizes', type=int, nargs='+', help=help_grid_sizes)
    parser.add_argument('--grid_types', type=str, nargs='+', help=help_grid_types)
    parser.add_argument('--output_width', type=int, help=help_output_width)
    parser.add_argument('--output_extension', type=str, help=help_extension)
    args = parser.parse_args()

    # Fill in defaults for missing arguments
    if not args.grid_sizes:
        args.grid_sizes = DEFAULT_GRID_SIZES
    if not args.grid_types:
        args.grid_types = DEFAULT_GRID_TYPES
    if not args.output_width:
        args.output_width = DEFAULT_OUTPUT_WIDTH
    if not args.output_extension:
        args.output_extension = DEFAULT_OUTPUT_EXTENSION

    # Convert values to GridType enum objects
    args.grid_types = [GridType(grid_type) for grid_type in args.grid_types]

    return args.grid_sizes, args.grid_types, args.output_width, args.output_extension


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
    _grid_sizes, _grid_types, _output_width, _output_extension = parse_args()
    vincent = VanGogh(_output_width, _output_extension)
    for input_filename in vincent.get_input_images():
        pointillize_input_img(_grid_sizes, _grid_types)
