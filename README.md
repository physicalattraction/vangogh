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

## Profiling with cProfile

### How to use cProfile?

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

## Profiling with pyinstrument

### How to use pyinstrument?

Source of learning about pyinstrument: https://pythonspeed.com/articles/beyond-cprofile/ 

To profile the script, perform the following from the src directory:

- Profile the script. Note that the execution takes long in profile mode.
```shell script
python -m pyinstrument main.py
```
- We get a tree of what is going on, with only relevant (time-consuming) calls
```shell script
9.481 <module>  <string>:1
   [7 frames hidden]  <string>, runpy, <built-in>
      9.480 _run_code  runpy.py:64
      └─ 9.480 <module>  main.py:1
         └─ 9.384 pointillize_input_img  main.py:41
            ├─ 5.382 pointillize_img  van_gogh.py:89
            │  ├─ 2.382 _draw_circle  van_gogh.py:200
            │  │  ├─ 0.926 ellipse  PIL/ImageDraw.py:145
            │  │  │     [10 frames hidden]  PIL, <built-in>
            │  │  ├─ 0.722 [self]
            │  │  ├─ 0.371 width  van_gogh.py:49
            │  │  │  ├─ 0.208 [self]
            │  │  │  └─ 0.163 size  van_gogh.py:43
            │  │  └─ 0.363 height  van_gogh.py:53
            │  │     ├─ 0.204 [self]
            │  │     └─ 0.159 size  van_gogh.py:43
            │  ├─ 2.039 _get_pixel  van_gogh.py:177
            │  │  ├─ 0.918 getpixel  PIL/Image.py:1423
            │  │  │     [12 frames hidden]  PIL, <built-in>
            │  │  ├─ 0.622 [self]
            │  │  ├─ 0.226 max  <built-in>:0
            │  │  │     [2 frames hidden]  <built-in>
            │  │  └─ 0.197 min  <built-in>:0
            │  │        [2 frames hidden]  <built-in>
            │  ├─ 0.327 _random_grid  van_gogh.py:160
            │  │  ├─ 0.204 _square_grid  van_gogh.py:151
            │  │  │  └─ 0.158 shuffle  random.py:348
            │  │  │        [8 frames hidden]  random, <built-in>
            │  │  └─ 0.117 <listcomp>  van_gogh.py:166
            │  ├─ 0.263 [self]
            │  ├─ 0.225 _square_grid  van_gogh.py:151
            │  │  └─ 0.166 shuffle  random.py:348
            │  │        [8 frames hidden]  random, <built-in>
            │  └─ 0.117 _hex_grid  van_gogh.py:130
            │     └─ 0.113 [self]
            └─ 3.923 save  van_gogh.py:116
               └─ 3.923 save  PIL/Image.py:2153
                     [12 frames hidden]  PIL, <built-in>
                        3.874 ImagingEncoder.encode  <built-in>:0
```

### Learnings

- We still see a lot of time is spent on accessing self.width and self.height.
```shell script
            ├─ 5.382 pointillize_img  van_gogh.py:89
            │  ├─ 2.382 _draw_circle  van_gogh.py:200
            │  │  ├─ 0.926 ellipse  PIL/ImageDraw.py:145
            │  │  │     [10 frames hidden]  PIL, <built-in>
            │  │  ├─ 0.722 [self]  <-- Calculations
            │  │  ├─ 0.371 width  van_gogh.py:49  <-- Accessing data from object
            │  │  │  ├─ 0.208 [self]
            │  │  │  └─ 0.163 size  van_gogh.py:43
            │  │  └─ 0.363 height  van_gogh.py:53  <-- Accessing data from object
            │  │     ├─ 0.204 [self]
            │  │     └─ 0.159 size  van_gogh.py:43
```
- By moving the calculation from Coordinate to CoordinateOnCanvas outside self._draw_circle, we can optimize this.
```shell script
            ├─ 4.563 pointillize_img  van_gogh.py:90
            │  ├─ 1.266 _draw_circle  van_gogh.py:206
            │  │  ├─ 0.981 ellipse  PIL/ImageDraw.py:145
            │  │  │     [10 frames hidden]  PIL, <built-in>
            │  │  └─ 0.284 [self]
            │  ├─ 0.471 [self]  <-- Calculation now moved to pointillize_img
```
- Inside `_get_pixel()`, we were doing a lot of `min()` and `max()` calls
```shell script
            │  ├─ 2.110 _get_pixel  van_gogh.py:183
            │  │  ├─ 0.951 getpixel  PIL/Image.py:1423
            │  │  │     [12 frames hidden]  PIL, <built-in>
            │  │  ├─ 0.649 [self]
            │  │  ├─ 0.238 max  <built-in>:0
            │  │  │     [2 frames hidden]  <built-in>
            │  │  └─ 0.210 min  <built-in>:0
            │  │        [2 frames hidden]  <built-in>
```
- They were only necessary to update a handful of values. By wrapping them inside an if statement, they are most of the time skipped.
```shell script
               ├─ 1.491 _get_pixel  van_gogh.py:183
               │  ├─ 0.892 getpixel  PIL/Image.py:1423
               │  │     [12 frames hidden]  PIL, <built-in>
               │  └─ 0.541 [self]
``` 
- To further reduce the saving time of images, I made it optional to switch between saving to PNG and saving to JPG, and made JPG the default.
```shell script
            ├─ 4.038 save  van_gogh.py:122
            │  └─ 4.038 save  PIL/Image.py:2153
            │        [14 frames hidden]  PIL, <built-in>
            │           4.018 ImagingEncoder.encode  <built-in>:0
```
```shell script
            └─ 0.706 save  van_gogh.py:122
               └─ 0.705 save  PIL/Image.py:2153
                     [14 frames hidden]  PIL, <built-in>, posixpath
```
- We shuffle the square grid that is underlying the random grid. This is not necessary, since these points should be hardly visible anyway. Removing this removes another 0.15 seconds. 
- After all improvements, creating the images with all defaults (9 grid sizes 1 - 75), 3 grid types, output width 1000 and output extension jpg, it takes 4.38 seconds to generate 27 images.
```
4.377 <module>  <string>:1
   [7 frames hidden]  <string>, runpy, <built-in>
      4.375 _run_code  runpy.py:64
      └─ 4.375 <module>  main.py:1
         ├─ 4.310 pointillize_input_img  main.py:47
         │  ├─ 3.557 pointillize_img  van_gogh.py:97
         │  │  ├─ 1.404 _get_pixel  van_gogh.py:191
         │  │  │  ├─ 0.835 getpixel  PIL/Image.py:1423
         │  │  │  │     [12 frames hidden]  PIL, <built-in>
         │  │  │  ├─ 0.512 [self]
         │  │  │  └─ 0.056 size  PIL/Image.py:556
         │  │  │        [2 frames hidden]  PIL
         │  │  ├─ 1.251 _draw_circle  van_gogh.py:216
         │  │  │  ├─ 0.931 ellipse  PIL/ImageDraw.py:145
         │  │  │  │     [10 frames hidden]  PIL, <built-in>
         │  │  │  └─ 0.319 [self]
         │  │  ├─ 0.414 [self]
         │  │  ├─ 0.203 _square_grid  van_gogh.py:164
         │  │  │  ├─ 0.150 shuffle  random.py:348
         │  │  │  │     [8 frames hidden]  random, <built-in>
         │  │  │  └─ 0.053 <listcomp>  van_gogh.py:165
         │  │  ├─ 0.158 _random_grid  van_gogh.py:174
         │  │  │  ├─ 0.109 <listcomp>  van_gogh.py:180
         │  │  │  │  └─ 0.067 uniform  random.py:503
         │  │  │  │        [4 frames hidden]  random, <built-in>
         │  │  │  └─ 0.048 _square_grid  van_gogh.py:164
         │  │  │     └─ 0.048 <listcomp>  van_gogh.py:165
         │  │  └─ 0.112 _hex_grid  van_gogh.py:143
         │  │     └─ 0.108 [self]
         │  └─ 0.701 save  van_gogh.py:129
         │     └─ 0.701 save  PIL/Image.py:2153
         │           [13 frames hidden]  PIL, <built-in>, abc
         └─ 0.061 <module>  van_gogh.py:1
```