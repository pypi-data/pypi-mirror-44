# Discriminant Ordering

## Intro

The Discriminant Ordering (DO) metric is an alternative method of measuring the "similarity" between 2 functions which aren't necessarily 1-to-1 mappings between one another. Rather than compute the correlation between two functions (f(x) vs g(x)), DO iteratively compares the ordering any all points in a space (i.e. x and x') after being mapped with the compared functions f(x) and g(x).

## Calculation Details

The DO metric considers the way two separate functions, f(x) and g(x), map the same dataset. For any pair of inputs from the space, x and x', we compare the "ordering" between f(x) and f(x') with that of g(x) and g(x'). The Heavi-side step function is then used to determine whether function f and function g map those two inputs with the same relative ordering. So the DO is can be written as

<p align="center"><img src="images/DO_equation.png" alt="DO" width="300px"/></p>

This can be thought of graphically by the diagram below

<p align="center"><img src="images/DO_calc_example.png" alt="DO_calc_example" width="600px"/></p>

When the two mappings are perfectly similiar or perfectly dissimilar (i.e. opposit ordering), summing all DO and normalizing to 1 yields the result 0 and 1, respectively. When the mappings are not at all related (i.e. the ordering is 50% similar and 50% dissimilar), summing over all DO-> 0.5. We can then map this to a more convenient scale by taking

<p align="center"><img src="images/DO_norm.png" alt="DO_norm" width="170px"/></p>

so, in the end,

<p align="center"><img src="images/DO_legend.png" alt="DO_legend" width="250px"/></p>

## Installing the discriminant ordering package

### From pip

The discriminant ordering calculation is available on pypi. To install,

```python
pip install discriminant_ordering
```

the discriminant ordering is designed to depend on numpy.

### Manual installation

Download the package from github

```
git clone https://github.com/tfaucett/discriminant_ordering.git
cd discriminant_ordering
```

and run the setup script

```python
python setup.py install
```

## Using discriminant_ordering

### General Usage

#### DO without stats
Import the package

```python
from discriminant_ordering import DO
```

The function requires 4 inputs:
- fx = The mapping for your first function (must be an array)
- gx = The mapping for your second function (must be an array)
- targets = target values (e.g. signal/background) (must be an array of the form [0 1 1 0 1 ...])
- n_data = The number of data_points you want to include in your calculation

```python
DO(fx=x, gx=y, target=targets, n_data=5000)
```

the output is a single floating point value of DO.

#### DO with stats
By default, DO will do a single calculation and output that DO value. An optional *stats* option will perform a bootstrap (i.e. multiple randomly selected calculations of DO) and compute the mean and standard deviation for your DO. To output *stats* for your DO, instead use the command

```python
DO(fx=x, gx=y, target=targets, n_data=5000, stats=True, boot_loops=100)
```

Where *boot_loops* allows you to specify how many times you want to loop through your data (i.e. how many calculations of DO you want to include in your mean and standard deviation). Including stats gives 2 floating point numbers as the output (i.e. mean, st_dev).

## Test Example

A simple test file is provided *test.py*. Using random numbers for fx, gx and the target values means we expect the DO to be approximately zero.

```python
import numpy as np
from discriminant_ordering import DO

n_data = 5000
n_calc = 500
x = np.random.rand(n_data)
y = np.random.rand(n_data)
targets = np.random.randint(2, size=n_data)

# DO calculated without statistics
print(DO(fx=x, gx=y, target=targets, n_data=n_calc))

# DO calculated with statistics (i.e. mean and stdev of DO)
print(DO(fx=x, gx=y, target=targets, n_data=n_calc, stats=True))

# DO example where you expect perfect similarity (i.e. compare x with x)
print(DO(fx=x, gx=x, target=targets, n_data=n_calc))
print(DO(fx=x, gx=x, target=targets, n_data=n_calc, stats=True))
```

which yields the expected result (note your results will differ as every time this test file is run, it generates a new set of random values)
```python
0.0009599999999998499
(0.030339066141999212, 0.024181331076012114)

1.0
(1.0, 8.881784197001253e-17)
```




