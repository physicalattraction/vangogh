# Van Gogh pointillism
Turn your photos into Van Gogh paintings in pointillism style! 

## Execution notes

In order to pointillize your image, do the following:
- Install all requirements
```shell script
pip install -r requirements/local.txt
```
- Place all images you want to pointillize in the folder `img/input`
- Run the script from the src directory, e.g.
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

## Efficiency notes

### Profiling

To profile the script, perform the following from the src directory:

- Profile the script. Note that the execution takes long in profile mode.
```shell script
python -m cProfile -o ../tmp/profile.txt main.py
```
- Open the pstats console (textual profile viewer).
```shell script
python3 -m pstats ../tmp/profile.txt
```
- To order all function calls by their cumulative time and show them in the console, run:
```shell script
profile.txt% sort cumtime
profile.txt% reverse
profile.txt% stats
```

I also used the decorator `measure_time()`, defined in this repository, to quickly measure and print the execution time of a block of code, e.g.
```python
with measure_time() as t:
    vincent.save(output_filename)
print(t)
```

### Learnings

- Saving a PNG of high resolution takes a long time, regardless of the contents. Times on my Macbook Pro 2017:
    - Saving a   250 x   250 image: 0.01 seconds
    - Saving a 1,000 x 1,000 image: 0.10-0.14 seconds 
    - Saving a 4,000 x 4,000 image: 1.60-1.85 seconds
- Based on this knowledge, I have reduced the default output width to 1,000
- When calculating all images, we get the following if we `int(round(x))` all values `x` (`left`, `right`, `upper` and `lower`).
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   432359    1.365    0.000    4.335    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:192(_draw_circle)
```
- I initially though that Pillow would raise an error if the numbers were not integers, but that is not true. If we remove those functions, the time for this is reduced.
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   432359    1.042    0.000    3.666    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:192(_draw_circle)
```  
- When fetching the size image lazily every time it's needed, we spend a lot of time doing this.
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   864718    0.242    0.000    0.629    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:44(height)
  1297077    0.385    0.000    1.011    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:40(width)
  2161795    0.691    0.000    1.013    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:36(size)
```
- When storing the size in a variable called `_size`, this time is reduced.
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  2161795    0.396    0.000    0.396    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:39(size)
   864718    0.251    0.000    0.403    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:49(height)
  1297077    0.386    0.000    0.629    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:45(width)
```
- By also making use of local variables `_width` and `_height`, this time is further reduced, although not by much. I suspect that these times are only so high since there a lot of function calls, and the profiler itself slows that down. I therefore do not add the additional variables to the code (for simplicity).
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   864718    0.165    0.000    0.165    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:55(height)
  1297077    0.251    0.000    0.251    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:49(width)
```
- Most time is now in the function `_get_pixel()`, of which around half of it in PIL's `getpixel()`.
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   432359    0.339    0.000    1.100    0.000 /Users/erwin/.virtualenvs/vangogh/lib/python3.9/site-packages/PIL/Image.py:1423(getpixel)
   432359    0.992    0.000    2.739    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:182(_get_pixel)
```
- Also here, I had `int(round(x))` around the calculations for `x` and `y`. They can be removed, leading to shorter time.
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   432359    0.358    0.000    1.113    0.000 /Users/erwin/.virtualenvs/vangogh/lib/python3.9/site-packages/PIL/Image.py:1423(getpixel)
   432359    0.829    0.000    2.487    0.000 /Users/erwin/git/vangogh/src/van_gogh.py:178(_get_pixel)
```
- After all improvements, creating the images with all defaults (9 grid sizes 1 - 75), 3 grid types and output width 1000, it takes 7.39 seconds to generate 27 images. 
