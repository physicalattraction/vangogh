import os.path

from van_gogh import GridType, VanGogh

if __name__ == '__main__':
    vincent = VanGogh()
    for output_filename in vincent.get_input_images():
        vincent.set_input_img(output_filename)
        filename_base, _ = os.path.splitext(output_filename)

        grid_sizes = [1, 2, 5, 10, 15, 20, 25, 50, 75]
        grid_types = [GridType.HEX, GridType.SQUARE, GridType.RANDOM]

        for grid_size in grid_sizes:
            vincent.set_grid_size(grid_size)
            print(f'Pointillizing {filename_base} with grid size {grid_size}')

            for grid_type in grid_types:
                vincent.pointillize_img(grid_type)
                output_filename = f'{filename_base}_{grid_type.value}_{grid_size}p'
                vincent.save(output_filename)
