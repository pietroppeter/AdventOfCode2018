# Advent of Code 2018

Forked from [narimiran's AoC 2017](https://github.com/narimiran/AdventOfCode2017), I plan to progressively fill in my solution for [Advent of Code 2018](https://adventofcode.com/2018).

My goal is to have fun and learn [Nim](https://nim-lang.org/). Since I know better Python, I will try first to solve the puzzle using Python. Then port the code to Nim. Since I really want to learn Nim, I will not submit a solution until the Nim code works.

&nbsp;

Task | Python solution | Nim solution | Learning Notes
--- | --- | --- | ---
[Day 1: Chronal Calibration](http://adventofcode.com/2018/day/1) | [day01.py](python/day01.py) | [day01.nim](nim/day01.nim) | At first I was not able to get Nim as fast as Python, still have to check exact times (remember to use d:release flag for nim)
[Day 2: Inventory Management System](http://adventofcode.com/2018/day/2) | [day02.py](python/day02.py) | [day02.nim](nim/day02.nim) | Had some hard time finding out an issue with CountTable in proc (see mega thread in forum), in the end my solution was more correct than the python one
[Day 3: No Matter How You Slice It](http://adventofcode.com/2018/day/3) | [day03.py](python/day03.py) | [day03.nim](nim/day03.nim) | Learned about objects and custom types in nim, code with a lot of parallelism between python and nim (I did not use numpy and arraymancer, but I should later on)
