import os
import random
from enum import Enum
from typing import List, Tuple

import math
from PIL import Image, ImageDraw

from config import MAX_GRID_SIZE, OUTPUT_WIDTH

Coordinate = Tuple[float, float]  # With float value between -1 and 1
Color = Tuple[int, int, int]  # With integer values between 0 and 255


class GridType(Enum):
    HEX = 'hex'
    SQUARE = 'square'
    RANDOM = 'random'


class VanGogh:
    """
    Paint like the famous Dutch artist!
    """

    src_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(src_dir)
    img_dir = os.path.join(root_dir, 'img')
    input_dir = os.path.join(img_dir, 'input')
    output_dir = os.path.join(img_dir, 'output')

    input_img: Image  # The image that serves as template
    grid_size: int  # Number of pixels in one direction (up to a constant)
    size: Tuple[int, int]  # The size in pixels of the output image
    img: Image  # The image we are drawing on
    draw: ImageDraw

    def __init__(self, grid_size=50):
        self.set_grid_size(grid_size)

    @property
    def size(self):
        return self.img.size

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def get_input_images(self, input_dir: str = None) -> List[str]:
        """
        Return a list of filenames of image files in the input directory

        :param input_dir: Optional, directory to search in. Default: img/input
        """

        search_path = os.path.join(input_dir or self.input_dir)
        list_imgs = [f for f in os.listdir(search_path)
                     if os.path.isfile(os.path.join(search_path, f))
                     and os.path.splitext(os.path.join(search_path, f))[-1] in {'.jpg', '.jpeg', '.png'}]
        return list_imgs

    def set_input_img(self, input_file: str, input_dir: str = None) -> Image:
        """
        Open an image from a file in the img/input directory

        :param input_file: Filename including extension to set as original image
        :param input_dir: Optional, directory where the file is located. Default: img/input
        """

        full_filename_in = os.path.join(input_dir or self.input_dir, input_file)
        self.input_img = Image.open(full_filename_in)

    def set_grid_size(self, grid_size: int):
        """
        Set the grid size for the output image, defined as the number of pixels in one direction (up to a constant)
        """

        assert grid_size <= MAX_GRID_SIZE, f'Grid sizes larger than {MAX_GRID_SIZE} are not supported until ' \
                                           f'performance has been improved'
        self.grid_size = grid_size

    def pointillize_img(self, grid_type: GridType):
        width = OUTPUT_WIDTH
        height = int(round(width * self.input_img.size[1] / self.input_img.size[0]))
        self._init_img(width, height)
        radius = 1 / (2 * self.grid_size * 1.05)

        if grid_type == GridType.HEX:
            grid = self._hex_grid()
        elif grid_type == GridType.SQUARE:
            grid = self._square_grid()
        elif grid_type == GridType.RANDOM:
            grid = self._random_grid()
        else:
            raise AssertionError('Unknown grid type')

        for point in grid:
            color = self._get_pixel(self.input_img, point)
            if color is not None:
                self._draw_circle(point, radius=radius, fill_color=color, outline_color=None)

    def show(self):
        """
        Show the image to screen
        """

        self.img.show()

    def save(self, img_name: str, img_dir: str = None):
        """
        Save the image in the object as .png to file

        :param img_name: Filename without extension
        :param img_dir: Optional, directory where to save the file. Default: img/output
        """

        if img_dir is None:
            img_dir = self.output_dir

        full_img_path = os.path.join(img_dir, f'{img_name}.png')
        self.img.save(full_img_path, quality=95, optimize=True)

    def _hex_grid(self) -> List[Coordinate]:
        """
        Return a hexagonal grid

            __
         __/  \__
        /  \__/  \
        \__/  \__/
        /  \__/  \
        \__/  \__/
           \__/

        Note: In principle, we should return coordinates within the box [-1, 1]. However, we also
        return coordinates a distance 2/grid_size away from this, in order to also fill pixels near
        the edges (center outside the box, but pixel itself visible within the box)
        """

        grid = []
        ei = (1, 0)  # Base vector in horizontal direction
        ej = (math.cos(math.radians(60)), math.sin(math.radians(60)))  # Base vector at 60 degrees
        limit = 1 + 2 / self.grid_size
        for i in range(-2 * self.grid_size, 2 * self.grid_size + 1):
            for j in range(-2 * self.grid_size, 2 * self.grid_size + 1):
                x = (ei[0] * i + ej[0] * j) / self.grid_size
                y = (ei[1] * i + ej[1] * j) / self.grid_size
                if -limit <= x < limit and -limit <= y < limit:
                    grid.append((x, y))
        return grid

    def _square_grid(self) -> List[Coordinate]:
        result = [
            (x / (2 * self.grid_size), y / (2 * self.grid_size))
            for x in range(-2 * self.grid_size, 2 * self.grid_size + 1)
            for y in range(-2 * self.grid_size, 2 * self.grid_size + 1)
        ]
        random.shuffle(result)
        return result

    def _random_grid(self) -> List[Coordinate]:
        """
        Return a randomized grid
        """

        factor = int(math.ceil(math.sqrt(self.grid_size)))
        random_part = [
            (random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(factor * self.grid_size * self.grid_size)
        ]
        return self._square_grid() + random_part

    def _init_img(self, width: int, height: int):
        size = (width, height)
        self.img = Image.new('RGBA', size, (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)

    @staticmethod
    def _get_pixel(img: Image, coordinate: Coordinate) -> Color:
        """
        Return the pixel value at a given position

        :param img: Image object of which to determine the image
        :param coordinate: The coordinate, with (x,y) within the square between (-1,-1), (-1,1), (1,1) and (1,-1)
        :returns: The pixel value as tuple
        """

        width, height = img.size
        x = int(round((coordinate[0] + 1) / 2 * width))
        y = int(round((coordinate[1] + 1) / 2 * height))

        # Due to rounding errors or coordinates just outside the box, it could be that the
        # coordinate falls outside the given image. In that case, return the closest pixel
        x = max(0, x)
        x = min(x, width - 1)
        y = max(0, y)
        y = min(y, width - 1)

        return img.getpixel((x, y))

    def _draw_circle(self, center: Coordinate, radius, fill_color, outline_color):
        radius *= self.width / 2
        left = int(round((center[0] + 1) / 2 * self.width - radius))
        right = int(round((center[0] + 1) / 2 * self.width + radius))
        upper = int(round((center[1] + 1) / 2 * self.height - radius))
        lower = int(round((center[1] + 1) / 2 * self.height + radius))
        self.draw.ellipse((left, upper, right, lower), fill=fill_color, outline=outline_color)
