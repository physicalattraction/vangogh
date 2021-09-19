import os
import random
from typing import List, Optional, Tuple

import math
from PIL import Image, ImageDraw

from config import MAX_GRID_SIZE
from grid_type import GridType

Coordinate = Tuple[float, float]  # With float value between -1 and 1
CoordinateOnCanvas = Tuple[float, float]  # With float value between 0 and width and between 0 and height
Color = Tuple[int, int, int]  # With integer values between 0 and 255

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}


class VanGogh:
    """
    Paint like the famous Dutch artist!
    """

    _src_dir = os.path.dirname(__file__)
    _root_dir = os.path.dirname(_src_dir)
    _img_dir = os.path.join(_root_dir, 'img')
    _input_dir = os.path.join(_img_dir, 'input')
    _output_dir = os.path.join(_img_dir, 'output')

    grid_size: int  # Number of points in one direction (up to a constant)
    output_width: int  # Number of pixels of the output image
    output_extension: str  # Extension of the output file

    _input_img: Image  # The image that serves as template
    _size: Optional[Tuple[int, int]]  # Size of the output image in pixels
    _width: Optional[int]
    _height: Optional[int]
    _img: Image  # The image we are drawing on
    _draw: ImageDraw

    def __init__(self, output_width: int, output_extension: str):
        assert output_extension in IMAGE_EXTENSIONS, f'Extension {output_extension} is in the ' \
                                                     f'valid extensions: {IMAGE_EXTENSIONS}'

        self.output_width = output_width
        self.output_extension = output_extension

        self._size = None
        self._width = None
        self._height = None

    @property
    def size(self):
        if not self._size:
            self._size = self._img.size
        return self._size

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

        search_path = os.path.join(input_dir or self._input_dir)
        list_imgs = [f for f in os.listdir(search_path)
                     if os.path.isfile(os.path.join(search_path, f))
                     and os.path.splitext(os.path.join(search_path, f))[-1].replace('.', '') in IMAGE_EXTENSIONS]
        return list_imgs

    def set_input_img(self, input_file: str, input_dir: str = None):
        """
        Open an image from a file in the img/input directory

        :param input_file: Filename including extension to set as original image
        :param input_dir: Optional, directory where the file is located. Default: img/input
        """

        full_filename_in = os.path.join(input_dir or self._input_dir, input_file)
        self._input_img = Image.open(full_filename_in)

    def set_grid_size(self, grid_size: int):
        """
        Set the grid size for the output image, defined as the number of pixels in one direction (up to a constant)
        """

        assert grid_size <= MAX_GRID_SIZE, f'Grid sizes larger than {MAX_GRID_SIZE} are not supported'
        self.grid_size = grid_size

    def pointillize_img(self, grid_type: GridType):
        width = self.output_width
        height = int(round(width * self._input_img.size[1] / self._input_img.size[0]))
        self._init_img(width, height)
        radius = self.width / (4 * self.grid_size * 1.05)

        if grid_type == GridType.HEX:
            grid = self._hex_grid()
        elif grid_type == GridType.SQUARE:
            grid = self._square_grid()
        elif grid_type == GridType.RANDOM:
            grid = self._random_grid()
        else:
            raise AssertionError('Unknown grid type')

        for point in grid:
            color = self._get_pixel(self._input_img, point)
            if color is not None:
                # Calculate the point on the canvas outside _draw_circle, to be able to use width and height
                # that are already in memory at this point, so no lookups required on this object.
                x_on_canvas = (point[0] + 1) / 2 * width
                y_on_canvas = (point[1] + 1) / 2 * height
                point_on_canvas = (x_on_canvas, y_on_canvas)
                self._draw_circle(center=point_on_canvas, radius=radius, fill_color=color, outline_color=None)

    def show(self):
        """
        Show the image to screen
        """

        self._img.show()

    def save(self, img_name: str, img_dir: str = None):
        """
        Save the image in the object to file

        :param img_name: Filename without extension
        :param img_dir: Optional, directory where to save the file. Default: img/output
        """

        if img_dir is None:
            img_dir = self._output_dir

        full_img_path = os.path.join(img_dir, f'{img_name}.{self.output_extension}')
        self._img.save(full_img_path, quality=95, optimize=False)

    def _hex_grid(self) -> List[Coordinate]:
        """
        Return a hexagonal grid

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

    def _square_grid(self, shuffle=True) -> List[Coordinate]:
        result = [
            (x / (2 * self.grid_size), y / (2 * self.grid_size))
            for x in range(-2 * self.grid_size, 2 * self.grid_size + 1)
            for y in range(-2 * self.grid_size, 2 * self.grid_size + 1)
        ]
        if shuffle:
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
        return self._square_grid(shuffle=False) + random_part

    def _init_img(self, width: int, height: int):
        size = (width, height)
        self._img = Image.new('RGB', size, (255, 255, 255))
        self._draw = ImageDraw.Draw(self._img)

    @staticmethod
    def _get_pixel(img: Image, coordinate: Coordinate) -> Color:
        """
        Return the pixel value at a given position

        :param img: Image object of which to determine the image
        :param coordinate: The coordinate, with (x,y) within the square between (-1,-1), (-1,1), (1,1) and (1,-1)
        :returns: The pixel value as tuple
        """

        width, height = img.size
        x = (coordinate[0] + 1) / 2 * width
        y = (coordinate[1] + 1) / 2 * height

        # Due to rounding errors or coordinates just outside the box, it could be that the
        # coordinate falls outside the given image. In that case, return the closest pixel
        if not 0 <= x < width:
            x = max(0, x)
            x = min(x, width - 1)
        if not 0 <= y < height:
            y = max(0, y)
            y = min(y, width - 1)

        return img.getpixel((x, y))

    def _draw_circle(self, center: CoordinateOnCanvas, radius, fill_color, outline_color):
        left = center[0] - radius
        right = center[0] + radius
        upper = center[1] - radius
        lower = center[1] + radius
        self._draw.ellipse((left, upper, right, lower), fill=fill_color, outline=outline_color)
