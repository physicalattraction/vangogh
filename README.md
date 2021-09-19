# Van Gogh pointillism
Turn your photos into Van Gogh paintings in pointillism style! 

## Execution notes

In order to pointillize your image, do the following:
- Install all requirements
```shell script
pip install -r requirements/local.txt
```
- Place all images you want to pointillize in the folder `img/input`
- Run the script, e.g.
```shell script
python -m main --grid_sizes 1 2 5 --grid_types hex square
```
- To find all options of the script explained, run
```shell script
python -m main --help
```
- Find all pointillized images in the folder `img/output`

Running the code requires Python 3.8 or up. 

Example input:
![Example input](example/input/wolf.jpg)

Example output with hexagonal grids:
![Example output hex 2p](example/output/wolf_hex_2p.png) ![Example output hex 10p](example/output/wolf_hex_10p.png) ![Example output hex 25p](example/output/wolf_hex_25p.png)

Example output with square grids:
![Example output square 2p](example/output/wolf_square_2p.png) | ![Example output square 10p](example/output/wolf_square_10p.png) | ![Example output square 25p](example/output/wolf_square_25p.png)

Example output with random grids:
![Example output random 2p](example/output/wolf_random_2p.png) | ![Example output random 10p](example/output/wolf_random_10p.png) | ![Example output random 25p](example/output/wolf_random_25p.png)

## TODOs
- [ ] Profile the script, and optimize where possible
